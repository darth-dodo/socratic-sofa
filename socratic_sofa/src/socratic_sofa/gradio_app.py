#!/usr/bin/env python
"""
Socratic Sofa - Gradio Web Interface
A philosophical dialogue system powered by CrewAI and the Socratic method
"""

import gradio as gr
from datetime import datetime
from socratic_sofa.crew import SocraticSofa
import os


def run_socratic_dialogue(topic: str = None) -> tuple:
    """
    Run the Socratic dialogue crew and return all outputs

    Args:
        topic: Optional custom topic. If None, the AI will propose one.

    Returns:
        Tuple of (topic_output, proposition_output, opposition_output, judgment_output)
    """
    # Prepare inputs
    inputs = {
        'topic': topic if topic else '',
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

        return topic_output, proposition_output, opposition_output, judgment_output

    except Exception as e:
        error_msg = f"Error running dialogue: {str(e)}"
        return error_msg, error_msg, error_msg, error_msg


# Create the Gradio interface
with gr.Blocks(
    title="Socratic Sofa - Philosophical Dialogue"
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

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown(
                """
                ### How It Works
                1. **Propose Topic**: Enter a topic or let the AI suggest one
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

            topic_input = gr.Textbox(
                label="Philosophical Topic (Optional)",
                placeholder="E.g., 'What is justice?' or leave empty for AI to propose",
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

    with gr.Row():
        with gr.Column():
            gr.Markdown("### ❓ First Line of Inquiry")
            proposition_output = gr.Markdown(
                label="Proposition",
                show_label=False
            )

        with gr.Column():
            gr.Markdown("### 🔄 Alternative Line of Inquiry")
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
        [View Source](https://github.com/anthropics/claude-code)
        """
    )

    # Connect the button to the function
    run_button.click(
        fn=run_socratic_dialogue,
        inputs=[topic_input],
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
