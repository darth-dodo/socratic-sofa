#!/usr/bin/env python
"""
Socratic Sofa - Gradio Web Interface
A philosophical dialogue system powered by CrewAI and the Socratic method
"""

import random
import time
from datetime import datetime
from pathlib import Path
from queue import Queue
from threading import Thread

import gradio as gr
import yaml

from socratic_sofa.content_filter import (
    get_alternative_suggestions,
    get_rejection_guidelines,
    is_topic_appropriate,
)
from socratic_sofa.crew import SocraticSofa
from socratic_sofa.logging_config import get_logger
from socratic_sofa.schemas import (
    InquiryOutput,
    JudgmentOutput,
    TopicOutput,
    format_inquiry_output,
    format_judgment_output,
    format_topic_output,
)

# Module logger
logger = get_logger(__name__)


def format_task_output(task_output, task_name: str) -> str:
    """
    Format task output using Pydantic models if available, falling back to raw output.

    Args:
        task_output: The CrewAI task output object
        task_name: Name of the task (propose_topic, propose, oppose, judge_task)

    Returns:
        Formatted markdown string
    """
    try:
        # Try to use Pydantic output if available
        if hasattr(task_output, "pydantic") and task_output.pydantic is not None:
            pydantic_obj = task_output.pydantic

            if task_name == "propose_topic" and isinstance(pydantic_obj, TopicOutput):
                return format_topic_output(pydantic_obj)
            elif task_name == "propose" and isinstance(pydantic_obj, InquiryOutput):
                return format_inquiry_output(pydantic_obj, "First Line of Inquiry", "🔵")
            elif task_name == "oppose" and isinstance(pydantic_obj, InquiryOutput):
                return format_inquiry_output(pydantic_obj, "Alternative Line of Inquiry", "🟢")
            elif task_name == "judge_task" and isinstance(pydantic_obj, JudgmentOutput):
                return format_judgment_output(pydantic_obj)

        # Fall back to raw output with headers
        raw = task_output.raw if hasattr(task_output, "raw") else str(task_output)

        if task_name == "propose":
            return "## 🔵 First Line of Inquiry\n\n" + raw
        elif task_name == "oppose":
            return "## 🟢 Alternative Line of Inquiry\n\n" + raw
        else:
            return raw

    except Exception as e:
        logger.warning(
            "Failed to format Pydantic output, using raw",
            extra={"task_name": task_name, "error": str(e)},
        )
        raw = task_output.raw if hasattr(task_output, "raw") else str(task_output)
        if task_name == "propose":
            return "## 🔵 First Line of Inquiry\n\n" + raw
        elif task_name == "oppose":
            return "## 🟢 Alternative Line of Inquiry\n\n" + raw
        return raw


# Load topics from YAML
def load_topics_data():
    """Load topic library from topics.yaml and return structured data."""
    topics_file = Path(__file__).parent / "topics.yaml"
    try:
        with open(topics_file) as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.warning(
            "Error loading topics file", extra={"error": str(e), "file": str(topics_file)}
        )
        return {
            "fallback": {
                "name": "Philosophy",
                "topics": ["What is justice?", "What is happiness?", "What is truth?"],
            }
        }


def get_topics_flat(topics_data: dict) -> list[str]:
    """Flatten topics into a list with category labels."""
    all_topics = []
    for category_data in topics_data.values():
        category_name = category_data["name"]
        for topic in category_data["topics"]:
            all_topics.append(f"[{category_name}] {topic}")
    return all_topics


def get_categories(topics_data: dict) -> list[str]:
    """Get list of category names."""
    return ["All Categories"] + [data["name"] for data in topics_data.values()]


def get_topics_by_category(topics_data: dict, category: str) -> list[str]:
    """Get topics filtered by category."""
    if category == "All Categories":
        return ["✨ Let AI choose"] + get_topics_flat(topics_data)

    for data in topics_data.values():
        if data["name"] == category:
            return ["✨ Let AI choose"] + [f"[{category}] {t}" for t in data["topics"]]

    return ["✨ Let AI choose"] + get_topics_flat(topics_data)


def get_random_topic(topics_data: dict) -> str:
    """Get a random topic from the library."""
    all_topics = get_topics_flat(topics_data)
    return random.choice(all_topics) if all_topics else "What is justice?"  # noqa: S311


# Load topics data
TOPICS_DATA = load_topics_data()
TOPICS = get_topics_flat(TOPICS_DATA)
CATEGORIES = get_categories(TOPICS_DATA)


# Progress indicator stages
PROGRESS_STAGES = [
    ("Topic Selection", "🎯"),
    ("First Inquiry", "🔵"),
    ("Alternative Inquiry", "🟢"),
    ("Evaluation", "⚖️"),
]


def create_progress_html(current_stage: int, start_time: float = None) -> str:
    """
    Generate HTML for progress indicator.

    Args:
        current_stage: Current stage index (0-4, where 4 means complete)
        start_time: Start time for elapsed calculation

    Returns:
        HTML string for progress display
    """
    elapsed = time.time() - start_time if start_time else 0
    avg_stage_time = 37.5  # Average of 30-45 seconds per stage
    total_estimated = avg_stage_time * len(PROGRESS_STAGES)
    time_remaining = max(0, total_estimated - elapsed)
    progress_percent = min(100, (current_stage / len(PROGRESS_STAGES)) * 100)

    stages_html = ""
    for idx, (stage_name, icon) in enumerate(PROGRESS_STAGES):
        if idx < current_stage:
            stage_class = "completed"
            stage_icon = "✓"
        elif idx == current_stage:
            stage_class = "active"
            stage_icon = icon
        else:
            stage_class = "pending"
            stage_icon = "○"

        stages_html += f'<span class="stage {stage_class}">{stage_icon} {stage_name}</span>'

    if current_stage >= len(PROGRESS_STAGES):
        status_text = "✅ Complete!"
    else:
        status_text = f"⏱️ ~{int(time_remaining)}s remaining"

    return f"""
<div class="progress-container">
    <div class="progress-stages">{stages_html}</div>
    <div class="progress-bar-container">
        <div class="progress-bar-fill" style="width: {progress_percent}%"></div>
    </div>
    <div class="progress-status">{status_text}</div>
</div>
"""


def handle_topic_selection(dropdown_value: str = None, textbox_value: str = None) -> str:
    """
    Handle topic selection from dropdown or textbox.
    Textbox takes priority if filled, otherwise use dropdown.
    """
    # If user typed something, use that (priority 1)
    if textbox_value and str(textbox_value).strip():
        return str(textbox_value).strip()

    # If no dropdown value, return empty
    if not dropdown_value:
        return ""

    # If dropdown is "Let AI choose", return empty
    if dropdown_value == "✨ Let AI choose":
        return ""

    # Extract topic from "[Category] Topic" format
    if "] " in dropdown_value:
        return dropdown_value.split("] ", 1)[1]

    return dropdown_value


def run_socratic_dialogue_streaming(dropdown_topic: str, custom_topic: str):
    """
    Run the Socratic dialogue crew with streaming output.

    Uses a generator to yield progressive results as each task completes.

    Args:
        dropdown_topic: Topic selected from dropdown
        custom_topic: Custom topic entered by user

    Yields:
        Tuple of (progress_html, topic_output, proposition_output, opposition_output, judgment_output)
    """
    # Track start time for progress indicator
    start_time = time.time()

    # Determine which topic to use
    final_topic = handle_topic_selection(dropdown_topic, custom_topic)

    # Debug logging
    logger.debug(
        "Topic selection",
        extra={
            "dropdown_topic": dropdown_topic,
            "custom_topic": custom_topic,
            "final_topic": final_topic,
        },
    )

    # Content moderation check
    is_appropriate, rejection_reason = is_topic_appropriate(final_topic)
    if not is_appropriate:
        # Create a friendlier rejection message with info/warning styling
        error_msg = "## 💭 Let's Explore Something Different\n\n"
        error_msg += f"We couldn't proceed with this topic. {rejection_reason}\n\n"
        error_msg += "### 🌟 Try These Related Topics Instead\n\n"

        # Get thematically related suggestions
        suggestions = get_alternative_suggestions(final_topic)
        for suggestion in suggestions[:5]:  # Show top 5 suggestions
            error_msg += f"- {suggestion}\n"

        error_msg += "\n---\n\n"
        error_msg += "<details>\n"
        error_msg += (
            "<summary><strong>📖 Why was this rejected? (Click to expand)</strong></summary>\n\n"
        )
        error_msg += get_rejection_guidelines()
        error_msg += "\n</details>"

        # Return empty progress (no stages completed) and error message
        yield "", error_msg, error_msg, error_msg, error_msg
        return

    # Initialize outputs with loading states
    outputs = {
        "topic": "⏳ *Preparing philosophical inquiry...*",
        "proposition": "⏳ *Waiting for topic selection...*",
        "opposition": "⏳ *Waiting for first inquiry...*",
        "judgment": "⏳ *Waiting for dialogues to complete...*",
    }
    current_stage = 0

    # Queue for receiving task completions
    task_queue = Queue()

    def task_callback(output):
        """Callback function called when each task completes"""
        task_queue.put(output)

    # Prepare inputs
    inputs = {"topic": final_topic, "current_year": str(datetime.now().year)}

    # Yield initial loading state with progress indicator
    progress_html = create_progress_html(current_stage, start_time)
    yield (
        progress_html,
        outputs["topic"],
        outputs["proposition"],
        outputs["opposition"],
        outputs["judgment"],
    )

    try:
        logger.info(
            "Starting Socratic dialogue",
            extra={"topic": final_topic, "topic_length": len(final_topic) if final_topic else 0},
        )

        # Create the crew with callback
        crew_instance = SocraticSofa()
        crew_instance.task_callback = task_callback
        crew = crew_instance.crew()

        # Run crew in a separate thread so we can stream updates
        result_container = {"result": None, "error": None}

        def run_crew():
            try:
                result_container["result"] = crew.kickoff(inputs=inputs)
            except Exception as e:
                result_container["error"] = e

        crew_thread = Thread(target=run_crew)
        crew_thread.start()

        # Track which tasks have completed
        task_names = ["propose_topic", "propose", "oppose", "judge_task"]
        task_index = 0

        # Poll for updates while crew is running
        while crew_thread.is_alive() or not task_queue.empty():
            try:
                # Check for completed tasks (non-blocking with timeout)
                task_output = task_queue.get(timeout=0.5)

                # Determine which task just completed based on order
                if task_index < len(task_names):
                    task_name = task_names[task_index]

                    if task_name == "propose_topic":
                        outputs["topic"] = format_task_output(task_output, task_name)
                        outputs["proposition"] = "🔄 *First line of inquiry in progress...*"
                        current_stage = 1
                    elif task_name == "propose":
                        outputs["proposition"] = format_task_output(task_output, task_name)
                        outputs["opposition"] = "🔄 *Alternative inquiry in progress...*"
                        current_stage = 2
                    elif task_name == "oppose":
                        outputs["opposition"] = format_task_output(task_output, task_name)
                        outputs["judgment"] = "🔄 *Evaluating dialogues...*"
                        current_stage = 3
                    elif task_name == "judge_task":
                        outputs["judgment"] = format_task_output(task_output, task_name)
                        current_stage = 4

                    task_index += 1

                    # Yield updated outputs with progress
                    progress_html = create_progress_html(current_stage, start_time)
                    yield (
                        progress_html,
                        outputs["topic"],
                        outputs["proposition"],
                        outputs["opposition"],
                        outputs["judgment"],
                    )

            except Exception:
                # Queue timeout - continue polling
                pass

        # Wait for thread to complete
        crew_thread.join()

        # Check for errors
        if result_container["error"]:
            raise result_container["error"]

        # Get final results from task objects to ensure we have all outputs
        tasks = crew.tasks
        task_names_final = ["propose_topic", "propose", "oppose", "judge_task"]
        if len(tasks) >= 4:
            if tasks[0].output:
                outputs["topic"] = format_task_output(tasks[0].output, task_names_final[0])
            if tasks[1].output:
                outputs["proposition"] = format_task_output(tasks[1].output, task_names_final[1])
            if tasks[2].output:
                outputs["opposition"] = format_task_output(tasks[2].output, task_names_final[2])
            if tasks[3].output:
                outputs["judgment"] = format_task_output(tasks[3].output, task_names_final[3])

        # Final yield with complete results and finished progress
        elapsed = time.time() - start_time
        logger.info(
            "Dialogue completed successfully",
            extra={"topic": final_topic, "elapsed_seconds": round(elapsed, 2)},
        )

        progress_html = create_progress_html(4, start_time)  # All 4 stages complete
        yield (
            progress_html,
            outputs["topic"],
            outputs["proposition"],
            outputs["opposition"],
            outputs["judgment"],
        )

    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(
            "Dialogue failed",
            extra={
                "topic": final_topic,
                "elapsed_seconds": round(elapsed, 2),
                "error": str(e),
                "error_type": type(e).__name__,
            },
        )
        error_msg = f"❌ Error running dialogue: {str(e)}"
        yield "", error_msg, error_msg, error_msg, error_msg


# CSS for warm cream, orange and peach design
CUSTOM_CSS = """
        /* Warm cream, orange and peach color palette */
        :root {
            --orange: #F47D31;
            --orange-dark: #E06820;
            --coral: #FF8C69;
            --peach: #FFB088;
            --peach-light: #FFDAB9;
            --peach-cream: #FFF0E5;
            --cream: #FFF8F0;
            --warm-white: #FFFBF5;
            --soft-peach: #F5E6DA;
            --text: #5C3D2E;
            --text-light: #8B6B5C;
            --glass-bg: rgba(255, 248, 240, 0.85);
            --glass-border: rgba(255, 200, 150, 0.4);
            --glass-shadow: rgba(180, 100, 50, 0.08);
        }

        /* Dark mode with warm orange/peach tones */
        @media (prefers-color-scheme: dark) {
            :root {
                --orange: #FF9A5C;
                --orange-dark: #E8854A;
                --coral: #FFB088;
                --peach: #FFCAAA;
                --peach-light: #3D2A20;
                --peach-cream: #2A1E18;
                --cream: #1F1714;
                --warm-white: #2A1E18;
                --soft-peach: #3D2A20;
                --text: #FFE4D6;
                --text-light: #D4B8A8;
                --glass-bg: rgba(45, 30, 22, 0.9);
                --glass-border: rgba(255, 150, 100, 0.2);
                --glass-shadow: rgba(0, 0, 0, 0.3);
            }
        }

        /* Gradient background */
        .gradio-container {
            background: linear-gradient(135deg, var(--cream) 0%, var(--peach-cream) 25%, var(--peach-light) 50%, var(--peach-cream) 75%, var(--cream) 100%) !important;
            background-size: 400% 400% !important;
            animation: gradientShift 20s ease infinite !important;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif !important;
            min-height: 100vh;
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Progress indicator */
        .progress-container {
            margin: 24px 0;
            padding: 24px;
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 28px;
            box-shadow: 0 8px 32px var(--glass-shadow), inset 0 1px 1px var(--glass-border);
            border: 1px solid var(--glass-border);
        }

        .progress-stages {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 20px;
        }

        .progress-stages .stage {
            flex: 1 1 auto;
            text-align: center;
            padding: 12px 18px;
            border-radius: 50px;
            font-size: 0.85rem;
            white-space: nowrap;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            font-weight: 500;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }

        .progress-stages .stage.completed {
            background: linear-gradient(135deg, var(--peach) 0%, var(--coral) 100%);
            color: var(--text);
            box-shadow: 0 4px 15px rgba(255, 176, 136, 0.4);
        }

        .progress-stages .stage.active {
            background: linear-gradient(135deg, var(--orange) 0%, var(--coral) 100%);
            color: white;
            font-weight: 600;
            animation: breathe 3s ease-in-out infinite;
            box-shadow: 0 6px 20px rgba(244, 125, 49, 0.4);
        }

        .progress-stages .stage.pending {
            background: var(--peach-cream);
            color: var(--text-light);
            border: 1px solid var(--glass-border);
        }

        @keyframes breathe {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.03); opacity: 0.92; }
        }

        .progress-bar-container {
            width: 100%;
            height: 8px;
            background: var(--peach-cream);
            border-radius: 4px;
            overflow: hidden;
            backdrop-filter: blur(5px);
        }

        .progress-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--orange) 0%, var(--coral) 50%, var(--peach) 100%);
            transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            border-radius: 4px;
            box-shadow: 0 0 10px rgba(244, 125, 49, 0.5);
        }

        .progress-status {
            text-align: center;
            margin-top: 14px;
            font-size: 0.9em;
            color: var(--text-light);
            font-weight: 500;
        }

        /* Buttons */
        button.primary {
            background: linear-gradient(135deg, var(--orange) 0%, var(--coral) 100%) !important;
            border: none !important;
            border-radius: 50px !important;
            font-weight: 600 !important;
            letter-spacing: 0.3px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 6px 20px rgba(244, 125, 49, 0.35), inset 0 1px 1px rgba(255,255,255,0.3) !important;
        }

        button.primary:hover {
            transform: translateY(-3px) scale(1.02) !important;
            box-shadow: 0 10px 30px rgba(244, 125, 49, 0.45), inset 0 1px 1px rgba(255,255,255,0.3) !important;
        }

        button.secondary {
            background: linear-gradient(135deg, var(--peach) 0%, var(--coral) 100%) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 50px !important;
            color: var(--text) !important;
            font-weight: 500 !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }

        button.secondary:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(255, 176, 136, 0.4) !important;
        }

        /* Input fields */
        .gr-textbox textarea, .gr-textbox input {
            border-radius: 18px !important;
            border: 1px solid var(--glass-border) !important;
            padding: 16px 20px !important;
            transition: all 0.3s ease !important;
            background: var(--glass-bg) !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
        }

        .gr-textbox textarea:focus, .gr-textbox input:focus {
            border-color: var(--orange) !important;
            box-shadow: 0 0 0 4px rgba(244, 125, 49, 0.15), 0 8px 25px var(--glass-shadow) !important;
        }

        /* Dropdown */
        .gr-dropdown {
            border-radius: 18px !important;
            background: var(--glass-bg) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid var(--glass-border) !important;
        }

        /* Card sections */
        .gr-box, .gr-panel {
            border-radius: 24px !important;
            border: 1px solid var(--glass-border) !important;
            background: var(--glass-bg) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            box-shadow: 0 8px 32px var(--glass-shadow), inset 0 1px 1px rgba(255,255,255,0.4) !important;
        }

        /* Typography */
        .prose h1, .prose h2, .prose h3 {
            color: var(--text) !important;
            font-weight: 600 !important;
        }

        .prose p, .prose li {
            color: var(--text) !important;
            line-height: 1.75 !important;
        }

        .prose {
            max-width: 100%;
            padding: 10px 0;
        }

        /* Blockquotes */
        .prose blockquote {
            border-left: 4px solid var(--orange) !important;
            background: var(--peach-cream) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 0 16px 16px 0 !important;
            padding: 14px 20px !important;
            margin: 14px 0 !important;
            font-style: normal !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        }

        /* Tables */
        .prose table {
            border-radius: 16px !important;
            overflow: hidden !important;
            border: 1px solid var(--glass-border) !important;
            background: var(--glass-bg) !important;
            backdrop-filter: blur(10px) !important;
        }

        .prose th {
            background: var(--peach-cream) !important;
            color: var(--text) !important;
            font-weight: 600 !important;
        }

        .prose td, .prose th {
            padding: 14px 18px !important;
            border-color: var(--soft-peach) !important;
        }

        .prose tr:hover td {
            background: var(--cream) !important;
        }

        /* Mobile responsive */
        @media (max-width: 768px) {
            .gradio-container {
                padding: 12px !important;
            }

            .gr-row {
                flex-direction: column !important;
            }

            .gr-column {
                width: 100% !important;
                max-width: 100% !important;
                margin-bottom: 16px !important;
            }

            .prose h1 { font-size: 1.5rem !important; }
            .prose h2 { font-size: 1.25rem !important; }
            .prose h3 { font-size: 1.1rem !important; }

            button {
                width: 100% !important;
                padding: 16px !important;
                margin: 8px 0 !important;
            }

            .progress-stages {
                flex-direction: column;
                gap: 10px;
            }

            .progress-stages .stage {
                width: 100%;
            }
        }

        /* Touch-friendly */
        button {
            min-height: 54px;
            font-weight: 500;
        }

        /* Spacing */
        .gr-form {
            gap: 18px;
        }

        .gr-row {
            margin-bottom: 1.5rem;
        }

        /* Example suggestions */
        .example-suggestions {
            opacity: 0.85;
            margin-top: -4px !important;
            margin-bottom: 18px !important;
            color: var(--text-light);
        }

        .example-suggestions small {
            font-size: 0.9rem;
        }

        /* Smooth transitions */
        .gr-box, button, .gr-textbox textarea, .gr-dropdown {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* Soft focus */
        *:focus {
            outline: none !important;
        }

        /* Subtle glow on hover for interactive elements */
        .gr-box:hover {
            box-shadow: 0 12px 40px var(--glass-shadow), inset 0 1px 1px rgba(255,255,255,0.5) !important;
        }
    """

# Create the Gradio interface
with gr.Blocks(
    title="Socratic Sofa - Philosophical Dialogue",
) as demo:
    gr.Markdown(
        """
        # 🏛️ Socratic Sofa
        ## AI-Powered Philosophical Dialogue Using the Socratic Method

        Experience authentic philosophical inquiry where AI explores topics through
        systematic questioning rather than assertions. The Socratic method reveals
        contradictions, challenges assumptions, and guides toward deeper understanding.
        """
    )

    # Input Section - Single column for better mobile support
    with gr.Column():
        gr.Markdown(
            """
            ### How It Works
            1. **Choose Topic**: Pick from library, get a random one, or write your own
            2. **First Inquiry**: Explore through Socratic questions
            3. **Alternative Inquiry**: Examine from a different angle
            4. **Evaluation**: Judge the quality of philosophical inquiry
            """
        )

        # Category filter
        category_dropdown = gr.Dropdown(
            choices=CATEGORIES,
            value="All Categories",
            label="🏷️ Filter by Category",
            info="Narrow down topics by philosophical domain",
        )

        # Topic selection with filtered choices
        topic_dropdown = gr.Dropdown(
            choices=["✨ Let AI choose"] + TOPICS,
            value="✨ Let AI choose",
            label="📚 Topic Library",
            info="Pick a classic question or choose your own below",
        )

        # Random topic button
        random_button = gr.Button("🎲 Random Topic", variant="secondary", size="sm")

        # Custom topic input
        topic_input = gr.Textbox(
            label="✍️ Or Enter Your Own Topic",
            placeholder="E.g., 'Should we colonize Mars?' or 'What is the nature of time?'",
            lines=2,
            max_lines=4,
        )

        # Example suggestions
        gr.Markdown(
            """
            <small>**Try these:** "Is consciousness an illusion?" • "Can AI be creative?" • "What makes life meaningful?"</small>
            """,
            elem_classes=["example-suggestions"],
        )

        run_button = gr.Button("🧠 Begin Socratic Dialogue", variant="primary", size="lg")

        gr.Markdown(
            """
            ---
            **Note**: Each dialogue takes 2-3 minutes to complete.
            Results will stream progressively as each stage completes.
            """
        )

    # Event handlers for input improvements
    def update_topics_by_category(category):
        """Update topic dropdown based on category selection."""
        topics = get_topics_by_category(TOPICS_DATA, category)
        return gr.update(choices=topics, value="✨ Let AI choose")

    def select_random_topic():
        """Select a random topic and reset to all categories."""
        random_topic = get_random_topic(TOPICS_DATA)
        all_topics = ["✨ Let AI choose"] + get_topics_flat(TOPICS_DATA)
        return (
            gr.update(value="All Categories"),  # Reset category filter
            gr.update(choices=all_topics, value=random_topic),  # Update dropdown with all topics
            "",  # Clear custom input
        )

    def clear_custom_on_dropdown_change(dropdown_value):
        """Clear custom input when dropdown is explicitly selected."""
        if dropdown_value and dropdown_value != "✨ Let AI choose":
            return ""
        return gr.update()

    # Connect event handlers
    category_dropdown.change(
        fn=update_topics_by_category,
        inputs=[category_dropdown],
        outputs=[topic_dropdown],
    )

    random_button.click(
        fn=select_random_topic,
        inputs=[],
        outputs=[category_dropdown, topic_dropdown, topic_input],
    )

    topic_dropdown.change(
        fn=clear_custom_on_dropdown_change,
        inputs=[topic_dropdown],
        outputs=[topic_input],
    )

    # Progress indicator
    progress_display = gr.HTML(value="", label="Progress")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📜 Proposed Topic")
            topic_output = gr.Markdown(label="Topic", show_label=False)

    # Use Row for desktop, but CSS will stack on mobile
    with gr.Row(equal_height=False):
        with gr.Column():
            proposition_output = gr.Markdown(label="Proposition", show_label=False)

        with gr.Column():
            opposition_output = gr.Markdown(label="Opposition", show_label=False)

    with gr.Row():
        with gr.Column():
            gr.Markdown("### ⚖️ Dialectic Evaluation")
            judgment_output = gr.Markdown(label="Judgment", show_label=False)

    gr.Markdown(
        """
        ---
        ### About This System

        **Socratic Sofa** uses CrewAI agents trained in the Socratic method:
        - **Socratic Philosopher**: Guides inquiry through probing questions
        - **Dialectic Moderator**: Evaluates authenticity and effectiveness of questioning

        The system emphasizes intellectual humility, systematic questioning, and
        philosophical depth over arriving at definitive conclusions.

        Built with [CrewAI](https://crewai.com) and [Claude](https://claude.ai) |
        [View Source](https://github.com/darth-dodo/socratic-sofa)
        """
    )

    # Connect the button to the streaming function
    run_button.click(
        fn=run_socratic_dialogue_streaming,
        inputs=[topic_dropdown, topic_input],
        outputs=[
            progress_display,
            topic_output,
            proposition_output,
            opposition_output,
            judgment_output,
        ],
    )


def main():
    """Launch the Gradio web interface"""
    demo.launch(
        server_name="0.0.0.0",  # nosec B104 - Required for HF Spaces deployment
        server_port=7860,
        share=False,
        css=CUSTOM_CSS,
        theme=gr.themes.Soft(
            primary_hue="orange",
            secondary_hue="orange",
        ),
    )


if __name__ == "__main__":
    main()
