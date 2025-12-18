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
- ⚖️ **Dialectic Moderator** - Evaluates the authenticity and effectiveness of Socratic inquiry
- 📚 **100 Curated Topics** - Philosophical questions across ethics, metaphysics, epistemology, politics, and mind
- 🌐 **Mobile-Responsive UI** - Beautiful, touch-friendly interface that works on all devices
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

## 📚 Learn More

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
