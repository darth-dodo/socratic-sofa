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

from socratic_sofa.logging_config import get_logger, log_timing

from socratic_sofa.content_filter import (
    get_alternative_suggestions,
    get_rejection_guidelines,
    is_topic_appropriate,
)
from socratic_sofa.crew import SocraticSofa

# Module logger
logger = get_logger(__name__)


# Load topics from YAML
def load_topics_data():
    """Load topic library from topics.yaml and return structured data."""
    topics_file = Path(__file__).parent / "topics.yaml"
    try:
        with open(topics_file) as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.warning("Error loading topics file", extra={"error": str(e), "file": str(topics_file)})
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
                        outputs["topic"] = task_output.raw
                        outputs["proposition"] = "🔄 *First line of inquiry in progress...*"
                        current_stage = 1
                    elif task_name == "propose":
                        outputs["proposition"] = "## 🔵 First Line of Inquiry\n\n" + task_output.raw
                        outputs["opposition"] = "🔄 *Alternative inquiry in progress...*"
                        current_stage = 2
                    elif task_name == "oppose":
                        outputs["opposition"] = (
                            "## 🟢 Alternative Line of Inquiry\n\n" + task_output.raw
                        )
                        outputs["judgment"] = "🔄 *Evaluating dialogues...*"
                        current_stage = 3
                    elif task_name == "judge_task":
                        outputs["judgment"] = task_output.raw
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
        if len(tasks) >= 4:
            if tasks[0].output:
                outputs["topic"] = tasks[0].output.raw
            if tasks[1].output:
                outputs["proposition"] = "## 🔵 First Line of Inquiry\n\n" + tasks[1].output.raw
            if tasks[2].output:
                outputs["opposition"] = (
                    "## 🟢 Alternative Line of Inquiry\n\n" + tasks[2].output.raw
                )
            if tasks[3].output:
                outputs["judgment"] = tasks[3].output.raw

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


# CSS for mobile responsive design
CUSTOM_CSS = """
        /* Progress indicator styles */
        .progress-container {
            margin: 20px 0;
            padding: 15px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        .progress-stages {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 15px;
        }

        .progress-stages .stage {
            flex: 1 1 auto;
            text-align: center;
            padding: 8px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            white-space: nowrap;
            transition: all 0.3s ease;
        }

        .progress-stages .stage.completed {
            background: #d4edda;
            color: #155724;
        }

        .progress-stages .stage.active {
            background: #cce5ff;
            color: #004085;
            font-weight: bold;
            animation: pulse 1.5s infinite;
        }

        .progress-stages .stage.pending {
            background: #e9ecef;
            color: #6c757d;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        .progress-bar-container {
            width: 100%;
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
        }

        .progress-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.5s ease;
        }

        .progress-status {
            text-align: center;
            margin-top: 10px;
            font-size: 0.9em;
            color: #6c757d;
        }

        /* Mobile responsive styles */
        @media (max-width: 768px) {
            .gradio-container {
                padding: 10px !important;
            }

            /* Stack columns vertically on mobile */
            .gr-row {
                flex-direction: column !important;
            }

            .gr-column {
                width: 100% !important;
                max-width: 100% !important;
                margin-bottom: 16px !important;
            }

            /* Typography adjustments */
            .prose h1 {
                font-size: 1.5rem !important;
                margin-bottom: 0.5rem !important;
            }
            .prose h2 {
                font-size: 1.2rem !important;
                margin-top: 1rem !important;
                margin-bottom: 0.5rem !important;
            }
            .prose h3 {
                font-size: 1rem !important;
                margin-top: 0.75rem !important;
                margin-bottom: 0.5rem !important;
            }

            .prose p {
                font-size: 0.95rem !important;
                line-height: 1.5 !important;
            }

            /* Button improvements */
            button {
                width: 100% !important;
                font-size: 1rem !important;
                padding: 12px !important;
                margin: 8px 0 !important;
            }

            /* Component spacing */
            .gr-box {
                border-radius: 8px !important;
                margin-bottom: 12px !important;
            }

            /* Dropdown and input fields */
            .gr-dropdown,
            .gr-textbox {
                width: 100% !important;
            }
        }

        /* Touch-friendly button sizing for all screens */
        button {
            min-height: 48px;
            font-weight: 500;
        }

        /* Better spacing for forms */
        .gr-form {
            gap: 12px;
        }

        /* Improve markdown readability */
        .prose {
            max-width: 100%;
        }

        /* Better spacing between sections */
        .gr-row {
            margin-bottom: 1.5rem;
        }

        /* Streaming status indicators */
        .streaming-status {
            color: #6366f1;
            font-style: italic;
        }

        /* Example suggestions styling */
        .example-suggestions {
            opacity: 0.7;
            margin-top: -8px !important;
            margin-bottom: 12px !important;
        }

        .example-suggestions small {
            font-size: 0.85rem;
        }

        /* Random button styling */
        .secondary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        }
    """

# Create the Gradio interface
with gr.Blocks(title="Socratic Sofa - Philosophical Dialogue") as demo:
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
        """Select a random topic and update the dropdown."""
        random_topic = get_random_topic(TOPICS_DATA)
        return gr.update(value=random_topic), ""

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
        outputs=[topic_dropdown, topic_input],
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
            primary_hue="indigo",
            secondary_hue="purple",
        ),
    )


if __name__ == "__main__":
    main()
