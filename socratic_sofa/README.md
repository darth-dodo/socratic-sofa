# 🏛️ Socratic Sofa

A philosophical dialogue system powered by [CrewAI](https://crewai.com) that uses the authentic Socratic method to explore ideas through systematic questioning rather than assertions.

## Overview

**Socratic Sofa** implements the classical Socratic method using AI agents that:
- Guide inquiry through probing questions (not declarative arguments)
- Use elenchus (refutation through questioning) to test beliefs
- Expose contradictions and challenge assumptions
- Maintain intellectual humility while guiding toward deeper understanding

### What Makes This Unique

Unlike traditional debate systems, Socratic Sofa follows the authentic philosophical method where:
- **No direct assertions** - Only questions that reveal truth
- **Progressive inquiry** - Questions build: definition → assumption → contradiction → insight
- **Intellectual humility** - The questioner professes ignorance
- **Focus on process** - Success is measured by quality of questioning, not conclusions reached

## Features

- 🤔 **Socratic Philosopher Agent** - Masters the art of philosophical questioning
- ⚖️ **Dialectic Moderator** - Evaluates authenticity and effectiveness of inquiry
- 📜 **Four-Stage Dialogue** - Topic, Proposition, Opposition, Judgment
- 🌐 **Web Interface** - Beautiful Gradio UI for interactive dialogues
- 📁 **Structured Outputs** - Each stage saved to separate markdown files

## Installation

### Prerequisites

- Python >=3.10 <3.14
- [UV](https://docs.astral.sh/uv/) package manager

### Setup

1. Clone the repository and navigate to the project:

```bash
cd socratic_sofa
```

2. Install uv if you haven't already:

```bash
pip install uv
```

3. Install dependencies:

```bash
uv sync
```

4. Configure your API key:

Create a `.env` file with your Anthropic API key:

```bash
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

### Web Interface (Recommended)

Launch the Gradio web interface:

```bash
uv run socratic_web
```

This will start a local server at http://localhost:7860 where you can:
- Enter a custom philosophical topic or let the AI propose one
- Watch the Socratic dialogue unfold in real-time
- View all four stages: Topic, Proposition, Opposition, Judgment

### Command Line

Run a Socratic dialogue from the command line:

```bash
uv run socratic_sofa
```

This executes the full dialogue and saves outputs to the `outputs/` directory:
- `01_topic.md` - Proposed philosophical topic
- `02_proposition.md` - First line of Socratic inquiry
- `03_opposition.md` - Alternative line of inquiry
- `04_judgment.md` - Dialectic evaluation

## How It Works

### The Socratic Method

1. **Topic Proposal** - AI suggests a philosophically rich question
2. **First Inquiry** (Proposition) - Explores topic through 5-7 questions that:
   - Clarify definitions and concepts
   - Probe foundational assumptions
   - Reveal potential contradictions
   - Guide toward deeper understanding

3. **Alternative Inquiry** (Opposition) - Examines from a different angle with:
   - Different assumptions and perspectives
   - Alternative tensions and contradictions
   - Complementary insights

4. **Dialectic Evaluation** - Moderator assesses:
   - Question Quality (40%)
   - Elenctic Effectiveness (25%)
   - Philosophical Insight (20%)
   - Socratic Fidelity (15%)

### Agent Configuration

**Socratic Philosopher**:
- Role: Master of Socratic questioning
- Goal: Guide discovery through questions, never assertions
- Method: Definition → Assumption → Contradiction → Insight

**Dialectic Moderator**:
- Role: Expert in Socratic dialectic
- Goal: Evaluate authenticity and effectiveness of questioning
- Focus: Process quality over philosophical positions

## Deployment

### Local Development

```bash
uv run socratic_web
```

### Deploy to Hugging Face Spaces

1. Create a new Space at https://huggingface.co/new-space
2. Select Gradio as SDK
3. Upload your code or connect your GitHub repository
4. Add your `ANTHROPIC_API_KEY` to Space secrets
5. Your app will be live at `https://huggingface.co/spaces/YOUR_USERNAME/socratic-sofa`

### Deploy to Render/Railway/Fly.io

1. Create a `Procfile`:
```
web: uv run socratic_web
```

2. Set environment variable `ANTHROPIC_API_KEY`
3. Deploy using their respective CLI tools

## Project Structure

```
socratic_sofa/
├── src/socratic_sofa/
│   ├── config/
│   │   ├── agents.yaml      # Socratic agents configuration
│   │   └── tasks.yaml       # Dialogue workflow tasks
│   ├── crew.py              # CrewAI orchestration
│   ├── main.py              # CLI entry point
│   └── gradio_app.py        # Web interface
├── outputs/                 # Generated dialogue files
├── pyproject.toml          # Project dependencies
└── README.md
```

## Example Dialogue

**Topic**: "What is the nature of knowledge?"

**First Inquiry** (7 questions exploring epistemology):
1. What do we mean by "knowledge"? How does it differ from belief?
2. What are the primary sources of knowledge? Senses, reason, authority?
3. How can we determine if something constitutes genuine knowledge?
...

**Alternative Inquiry** (7 questions from different angle):
1. If knowledge isn't just perception, from what other sources might it arise?
2. How do social and cultural contexts shape what counts as knowledge?
3. Whose perspectives should be centered in our understanding of knowledge?
...

**Evaluation**: Second inquiry scored 100% for superior depth, engagement with power dynamics, and commitment to epistemic pluralism.

## Customization

### Modify Agents

Edit `src/socratic_sofa/config/agents.yaml` to adjust:
- Agent roles and goals
- Socratic principles and approach
- Evaluation criteria

### Modify Tasks

Edit `src/socratic_sofa/config/tasks.yaml` to change:
- Number of questions per inquiry
- Output formats
- Task descriptions

### Modify Crew Logic

Edit `src/socratic_sofa/crew.py` to:
- Add new agents
- Change task sequence
- Modify output file paths

## Technical Details

- **Framework**: CrewAI 1.7.0
- **LLM**: Claude Sonnet 4.5 via Anthropic API
- **UI**: Gradio 6.1.0
- **Format**: CrewAI YAML configuration
- **Outputs**: Structured markdown files

## Support & Resources

- **CrewAI Documentation**: https://docs.crewai.com
- **Gradio Documentation**: https://gradio.app/docs
- **Claude Code**: https://claude.ai/code
- **Issues**: Please report bugs via GitHub issues

## License

MIT License - See LICENSE file for details

---

*Built with [CrewAI](https://crewai.com) and [Claude](https://claude.ai) | Inspired by classical Socratic philosophy*
