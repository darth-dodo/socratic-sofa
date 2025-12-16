#!/usr/bin/env python
"""
Socratic Sofa - Gradio Web Interface
A philosophical dialogue system powered by CrewAI and the Socratic method
"""

import gradio as gr
from datetime import datetime
from socratic_sofa.crew import SocraticSofa
from socratic_sofa.content_filter import is_topic_appropriate, get_alternative_suggestions
import os
import yaml
from pathlib import Path


# Load topics from YAML
def load_topics():
    """Load topic library from topics.yaml"""
    topics_file = Path(__file__).parent / "topics.yaml"
    try:
        with open(topics_file, 'r') as f:
            topics_data = yaml.safe_load(f)

        # Flatten topics into a list with category labels
        all_topics = []
        for category_key, category_data in topics_data.items():
            category_name = category_data['name']
            for topic in category_data['topics']:
                all_topics.append(f"[{category_name}] {topic}")

        return all_topics
    except Exception as e:
        print(f"Error loading topics: {e}")
        return ["What is justice?", "What is happiness?", "What is truth?"]


TOPICS = load_topics()


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


def run_socratic_dialogue(dropdown_topic: str, custom_topic: str) -> tuple:
    """
    Run the Socratic dialogue crew and return all outputs

    Args:
        dropdown_topic: Topic selected from dropdown
        custom_topic: Custom topic entered by user

    Returns:
        Tuple of (topic_output, proposition_output, opposition_output, judgment_output)
    """
    # Determine which topic to use
    final_topic = handle_topic_selection(dropdown_topic, custom_topic)

    # Debug output
    print(f"🔍 Topic Selection Debug:")
    print(f"   Dropdown: {repr(dropdown_topic)}")
    print(f"   Custom: {repr(custom_topic)}")
    print(f"   Final: {repr(final_topic)}")

    # Content moderation check
    is_appropriate, rejection_reason = is_topic_appropriate(final_topic)
    if not is_appropriate:
        error_msg = f"⚠️ {rejection_reason}\n\n"
        error_msg += "**Suggested topics:**\n"
        for suggestion in get_alternative_suggestions():
            error_msg += f"- {suggestion}\n"
        return error_msg, error_msg, error_msg, error_msg

    # Prepare inputs
    inputs = {
        'topic': final_topic,
        'current_year': str(datetime.now().year)
    }

    try:
        # Run the crew
        crew = SocraticSofa().crew()
        result = crew.kickoff(inputs=inputs)

        # Read the output files
        outputs_dir = "outputs"

        with open(f"{outputs_dir}/01_topic.md", 'r') as f:
            topic_output = f.read()

        with open(f"{outputs_dir}/02_proposition.md", 'r') as f:
            proposition_output = f.read()

        with open(f"{outputs_dir}/03_opposition.md", 'r') as f:
            opposition_output = f.read()

        with open(f"{outputs_dir}/04_judgment.md", 'r') as f:
            judgment_output = f.read()

        # Add headers to distinguish the sections clearly
        proposition_output = "## 🔵 First Line of Inquiry\n\n" + proposition_output
        opposition_output = "## 🟢 Alternative Line of Inquiry\n\n" + opposition_output

        return topic_output, proposition_output, opposition_output, judgment_output

    except Exception as e:
        error_msg = f"Error running dialogue: {str(e)}"
        return error_msg, error_msg, error_msg, error_msg


# Create the Gradio interface
with gr.Blocks(
    title="Socratic Sofa - Philosophical Dialogue",
    css="""
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
    """
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
            1. **Choose Topic**: Pick from library or write your own
            2. **First Inquiry**: Explore through Socratic questions
            3. **Alternative Inquiry**: Examine from a different angle
            4. **Evaluation**: Judge the quality of philosophical inquiry

            ### The Socratic Method
            - Uses questions to stimulate critical thinking
            - Exposes contradictions through elenchus
            - Maintains intellectual humility
            - Progresses: definition → assumption → contradiction → insight
            """
        )

        topic_dropdown = gr.Dropdown(
            choices=["✨ Let AI choose"] + TOPICS,
            value="✨ Let AI choose",
            label="📚 Topic Library",
            info="Pick a classic question or choose your own below"
        )

        topic_input = gr.Textbox(
            label="Or Enter Your Own Topic",
            placeholder="E.g., 'Should we colonize Mars?' (leave empty to use dropdown selection)",
            lines=2
        )

        run_button = gr.Button(
            "🧠 Begin Socratic Dialogue",
            variant="primary",
            size="lg"
        )

        gr.Markdown(
            """
            ---
            **Note**: Each dialogue takes 2-3 minutes to complete.
            The AI will generate thoughtful questions following authentic Socratic method.
            """
        )

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📜 Proposed Topic")
            topic_output = gr.Markdown(
                label="Topic",
                show_label=False
            )

    # Use Row for desktop, but CSS will stack on mobile
    with gr.Row(equal_height=False):
        with gr.Column():
            proposition_output = gr.Markdown(
                label="Proposition",
                show_label=False
            )

        with gr.Column():
            opposition_output = gr.Markdown(
                label="Opposition",
                show_label=False
            )

    with gr.Row():
        with gr.Column():
            gr.Markdown("### ⚖️ Dialectic Evaluation")
            judgment_output = gr.Markdown(
                label="Judgment",
                show_label=False
            )

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

    # Connect the button to the function
    run_button.click(
        fn=run_socratic_dialogue,
        inputs=[topic_dropdown, topic_input],
        outputs=[topic_output, proposition_output, opposition_output, judgment_output]
    )


def main():
    """Launch the Gradio web interface"""
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        theme=gr.themes.Soft(
            primary_hue="indigo",
            secondary_hue="purple",
        )
    )


if __name__ == "__main__":
    main()
