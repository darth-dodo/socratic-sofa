#!/usr/bin/env python3
"""
Hugging Face Space Entry Point for Socratic Sofa

This file serves as the entry point for deploying Socratic Sofa on Hugging Face Spaces.
It configures the path and launches the Gradio interface.
"""
import sys
from pathlib import Path

# Add socratic_sofa source to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import the Gradio demo
from socratic_sofa.gradio_app import demo

if __name__ == "__main__":
    # Launch the Gradio interface
    # Hugging Face Spaces automatically handles the server configuration
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
