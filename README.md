---
title: Socratic Sofa
emoji: 🏛️
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: "6.1.0"
app_file: app.py
pinned: false
license: mit
---

# 🏛️ Socratic Sofa

**AI-Powered Philosophical Dialogue Using the Authentic Socratic Method**

Experience deep philosophical inquiry where AI explores topics through systematic questioning rather than assertions. Built with CrewAI and Claude, Socratic Sofa follows the classical Socratic method to reveal contradictions, challenge assumptions, and guide toward deeper understanding.

## ✨ Features

- 🤔 **Socratic Philosopher Agent** - Masters the art of philosophical questioning following authentic elenchus
- ⚖️ **Dialectic Moderator** - Evaluates the authenticity and effectiveness of Socratic inquiry with differentiation scoring
- 📚 **100 Curated Topics** - Philosophical questions across 7 categories: classics, ethics, mind, society, modern, fun, and personal
- 🌍 **Multiple Philosophical Traditions** - Questions draw from Greek, Eastern, Modern Western, and Contemporary philosophy
- 🛡️ **Content Moderation** - AI-powered filtering for appropriate philosophical discourse
- 🌐 **Mobile-Responsive UI** - Beautiful, touch-friendly interface that works on all devices
- 🔄 **Streaming Output** - Real-time dialogue generation with progress feedback
- 📜 **Four-Stage Dialogue** - Topic → Proposition → Opposition → Judgment

## 🎯 How It Works

### The Socratic Method

Unlike traditional debate systems, Socratic Sofa uses **questions, not assertions**:

1. **Questions Only** - No direct claims about truth, only questions that reveal it
2. **Elenchus** (Refutation) - Exposes contradictions through systematic questioning
3. **Intellectual Humility** - The questioner professes ignorance
4. **Progressive Inquiry** - Definition → Assumption → Contradiction → Insight

### Using Socratic Sofa

1. **Choose a Topic**:
   - Select from 100 curated philosophical questions
   - Enter your own philosophical topic
   - Let the AI propose a topic

2. **First Inquiry**: Watch as the AI explores the topic through 5-7 Socratic questions

3. **Alternative Inquiry**: A second line of questioning from a different perspective

4. **Evaluation**: The Dialectic Moderator assesses both inquiries on:
   - Question Quality (40%)
   - Elenctic Effectiveness (25%)
   - Philosophical Insight (20%)
   - Socratic Fidelity (15%)
   - Differentiation Quality (bonus +10% for second inquiry)

## 📖 Example Topics

**Ethics & Morality**

- What is justice?
- Can we justify civil disobedience?
- What constitutes a good life?

**Epistemology**

- What is the nature of knowledge?
- Can we know anything with certainty?
- How do we distinguish truth from opinion?

**Contemporary Issues**

- Should AI have rights?
- What is the ethics of AI-generated art?
- What are our obligations to future generations?

## 🔧 Technical Details

- **Framework**: CrewAI 1.7.0 for multi-agent orchestration
- **LLM**: Claude Sonnet 4.5 via Anthropic API
- **Interface**: Gradio 6.1.0 with mobile-responsive design
- **Method**: Sequential task execution following philosophical dialogue structure
- **Package Manager**: UV for fast dependency management
- **Testing**: 80%+ code coverage with pytest
- **CI/CD**: GitHub Actions with automated deployment to HuggingFace Spaces
- **Content Safety**: Claude-powered content moderation

## 🚀 Getting Started

### Prerequisites

- Python 3.10+ (but less than 3.14)
- UV package manager (`pip install uv`)
- Anthropic API key ([get one here](https://console.anthropic.com/))

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/darth-dodo/socratic-sofa.git
cd socratic-sofa

# Install dependencies with UV
uv sync

# Configure API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Run the web interface
uv run socratic_web

# Or run the CLI
uv run socratic_sofa
```

The web interface will be available at `http://localhost:7860`

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=src/socratic_sofa --cov-report=term-missing

# Current coverage: 80%+
```

## 🏗️ Architecture Overview

### Core Components

- **`crew.py`**: CrewAI orchestration with socratic_questioner and judge agents
- **`gradio_app.py`**: Web interface with topic selection and streaming output
- **`content_filter.py`**: Content moderation using Claude API for safety
- **`config/agents.yaml`**: Agent configurations with philosophical traditions
- **`config/tasks.yaml`**: Task definitions with differentiation requirements
- **`topics.yaml`**: 100 curated topics organized by 7 categories

### Agent Workflow

```
User Topic → Content Filter → Propose Topic
                                    ↓
                            First Inquiry (5-7 questions)
                                    ↓
                            Second Inquiry (different angle)
                                    ↓
                            Judge Evaluation (with differentiation scoring)
```

### Recent Improvements

- **Differentiation Scoring**: Second inquiry receives bonus points (up to +10%) for exploring genuinely different philosophical angles
- **Markdown Output**: Judge provides formatted evaluation with tables and emoji indicators
- **Philosophical Traditions**: Agents draw from Greek, Eastern, Modern Western, and Contemporary philosophy
- **Repetition Penalty**: Judge penalizes overlapping questions or themes (up to -15%)
- **Category Filtering**: Topics organized by category with random selection within categories
- **Streaming Interface**: Real-time output display during dialogue generation

## 🛠️ Development

### Pre-commit Hooks

This project uses pre-commit hooks for code quality:

```bash
# Install hooks (one-time setup)
make precommit-install

# Run all checks manually
make precommit

# Run security checks only
make security
```

**Included hooks:**

- **Formatting**: isort, ruff-format
- **Linting**: ruff (pycodestyle, pyflakes, bugbear, security)
- **Security**: bandit, detect-secrets
- **Quality**: vulture (dead code), large file check
- **Dev Experience**: trailing whitespace, YAML/JSON validation, prettier

## 🌐 Deployment

### HuggingFace Spaces

Live demo available at: [https://huggingface.co/spaces/darth-dodo/socratic-sofa](https://huggingface.co/spaces/darth-dodo/socratic-sofa)

Deployment is automated via GitHub Actions:

- Push to `main` branch triggers CI tests
- Successful tests trigger deployment to HuggingFace Spaces
- Space configuration: Gradio SDK 6.1.0, Python 3.12

### Local Docker Deployment

```bash
# Build the image
docker build -t socratic-sofa .

# Run with environment variable
docker run -p 7860:7860 -e ANTHROPIC_API_KEY=your_key socratic-sofa
```

## 📚 Learn More

- **Live Demo**: [HuggingFace Spaces](https://huggingface.co/spaces/darth-dodo/socratic-sofa)
- **GitHub**: [socratic-sofa](https://github.com/darth-dodo/socratic-sofa)
- **Documentation**: [Full Docs](https://github.com/darth-dodo/socratic-sofa/tree/main/docs)
- **Socratic Method**: [Stanford Encyclopedia](https://plato.stanford.edu/entries/socrates/)

## 🤝 Contributing

Contributions welcome! See the [GitHub repository](https://github.com/darth-dodo/socratic-sofa) for:

- Feature requests
- Bug reports
- Documentation improvements
- New philosophical topics

## 📄 License

MIT License - See [LICENSE](https://github.com/darth-dodo/socratic-sofa/blob/main/LICENSE) for details

---

_"The unexamined life is not worth living." - Socrates_

Built with [CrewAI](https://crewai.com) and [Claude](https://claude.ai) | Inspired by classical Socratic philosophy
