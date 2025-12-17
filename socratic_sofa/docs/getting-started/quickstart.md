# Quickstart Guide

Get started with Socratic Sofa in 5 minutes! This guide will help you run your first philosophical dialogue using the Socratic method.

## Prerequisites Check

Before starting, ensure you've completed the [installation guide](./installation.md). You should have:

- ✅ Python 3.10+ installed
- ✅ UV package manager installed
- ✅ Project dependencies installed (`uv sync`)
- ✅ Anthropic API key configured in `.env`

Quick verification:
```bash
cd socratic-sofa/socratic_sofa
make check-api
```

## Choose Your Interface

Socratic Sofa offers two ways to run philosophical dialogues:

1. **Web Interface** (Recommended for beginners) - Beautiful Gradio UI
2. **Command Line** - Fast and scriptable

### Option 1: Web Interface (Recommended)

The web interface is the easiest way to get started. It provides an interactive experience where you can choose topics and watch the dialogue unfold in real-time.

#### Launch the Web Interface

```bash
# Make sure you're in the project directory
cd socratic-sofa/socratic_sofa

# Launch the web interface
uv run socratic_web

# Or use the Makefile shortcut
make web
```

**Expected output**:
```
Running on local URL:  http://127.0.0.1:7860
```

#### Open in Your Browser

1. Open your web browser
2. Navigate to: `http://localhost:7860`
3. You should see the Socratic Sofa interface

**Interface preview**:
```
┌─────────────────────────────────────┐
│  🏛️ Socratic Sofa                   │
│  AI-Powered Philosophical Dialogue  │
├─────────────────────────────────────┤
│  📚 Topic Library                   │
│  [✨ Let AI choose ▼]              │
│                                     │
│  Or Enter Your Own Topic           │
│  [_________________________]       │
│                                     │
│  [🧠 Begin Socratic Dialogue]      │
└─────────────────────────────────────┘
```

#### Run Your First Dialogue

1. **Choose a topic** using one of these methods:
   - **Let AI decide**: Keep "✨ Let AI choose" selected
   - **Pick from library**: Select a topic like "[Ethics] What is justice?"
   - **Enter your own**: Type a question in the text box

2. **Click "🧠 Begin Socratic Dialogue"**
   - Processing takes 2-3 minutes
   - Watch as each section appears:
     - 📜 Proposed Topic
     - 🔵 First Line of Inquiry
     - 🟢 Alternative Line of Inquiry
     - ⚖️ Dialectic Evaluation

3. **Review the results**:
   - Each section shows the AI's Socratic questioning
   - Questions follow the pattern: definition → assumption → contradiction → insight
   - The evaluation scores both lines of inquiry

#### Example Web Session

**Input**: "What is happiness?"

**Output sections**:
- **Topic**: Philosophical question about the nature of happiness
- **First Inquiry**: 7 questions exploring hedonistic vs eudaimonic happiness
- **Alternative Inquiry**: 7 questions examining cultural and temporal aspects
- **Evaluation**: Scores and comparison of both approaches

### Option 2: Command Line Interface

The CLI is perfect for automation, scripting, or when you prefer the terminal.

#### Run a Dialogue

```bash
# Run with default topic
uv run socratic_sofa

# Or use the Makefile
make dev
```

**What happens**:
1. The system starts processing the dialogue
2. You'll see verbose output from CrewAI agents
3. Results are saved to the `outputs/` directory
4. Process takes 2-3 minutes

**Expected output**:
```
🏛️ Running Socratic dialogue (CLI)...

[Agent: Socratic Philosopher]
Proposing topic...

[Task: propose_topic]
✓ Topic: What is the nature of knowledge?

[Task: propose]
✓ First inquiry complete (7 questions)

[Task: oppose]
✓ Alternative inquiry complete (7 questions)

[Task: judge_task]
✓ Evaluation complete

✅ Dialogue complete! Results saved to outputs/
```

#### View the Results

Results are automatically saved to markdown files:

```bash
# View all outputs using make command
make outputs

# Or view individual files
cat outputs/01_topic.md        # Proposed topic
cat outputs/02_proposition.md  # First line of inquiry
cat outputs/03_opposition.md   # Alternative inquiry
cat outputs/04_judgment.md     # Evaluation and scores
```

**Example output structure**:
```
outputs/
├── 01_topic.md         # "What is the nature of knowledge?"
├── 02_proposition.md   # 7 questions exploring empiricism
├── 03_opposition.md    # 7 questions exploring rationalism
└── 04_judgment.md      # Scores and evaluation
```

## Understanding the Output

Every Socratic dialogue consists of four stages:

### Stage 1: Topic Proposal (01_topic.md)

The philosophical question to explore.

**Example**:
```markdown
What is the relationship between knowledge and truth?
```

### Stage 2: First Inquiry - Proposition (02_proposition.md)

5-7 Socratic questions exploring one perspective.

**Example**:
```markdown
1. When we claim to possess knowledge, what exactly distinguishes
   it from mere belief or opinion?

2. If knowledge requires truth, how do we determine whether
   something is genuinely true?

3. Can we have knowledge of something that later turns out
   to be false, or does that retrospectively show we never
   had knowledge at all?

[... 4 more questions]
```

### Stage 3: Alternative Inquiry - Opposition (03_opposition.md)

5-7 questions from a different angle or perspective.

**Example**:
```markdown
1. Rather than viewing knowledge as requiring absolute truth,
   might it be better understood as justified belief within
   particular contexts?

2. How do social and cultural factors shape what counts as
   knowledge in different communities?

[... 5 more questions]
```

### Stage 4: Dialectic Evaluation - Judgment (04_judgment.md)

Scores and comparison of both inquiries.

**Example**:
```markdown
## Evaluation

**First Inquiry**
- Question Quality: 4/5 (40%)
- Elenctic Effectiveness: 3/5 (25%)
- Philosophical Insight: 4/5 (20%)
- Socratic Fidelity: 4/5 (15%)
- **Total: 88%**

**Alternative Inquiry**
- Question Quality: 5/5 (40%)
- Elenctic Effectiveness: 5/5 (25%)
- Philosophical Insight: 5/5 (20%)
- Socratic Fidelity: 5/5 (15%)
- **Total: 100%**

**Winner**: Alternative Inquiry

The second line of questioning demonstrates superior engagement
with epistemic pluralism and contextual factors...
```

## Quick Tips

### Choosing Good Topics

**Great topics** for Socratic dialogue:
- ✅ "What is justice?"
- ✅ "Can we know anything with certainty?"
- ✅ "Should we colonize Mars?"
- ✅ "What makes art valuable?"

**Avoid**:
- ❌ "What is 2+2?" (not philosophically rich)
- ❌ "Tell me about Python" (not a question)
- ❌ Inappropriate or offensive content (filtered automatically)

### Reading the Questions

The Socratic method asks questions, never makes assertions:
- Look for question marks at the end
- Questions should challenge assumptions
- They reveal contradictions rather than state positions
- Build progressively: simple → complex

### Understanding Scores

The evaluation uses weighted criteria:
- **Question Quality (40%)**: Clarity, depth, logical flow
- **Elenctic Effectiveness (25%)**: Success revealing contradictions
- **Philosophical Insight (20%)**: Depth of inquiry
- **Socratic Fidelity (15%)**: True to Socratic method

Scores of 80%+ indicate high-quality Socratic dialogue.

## Common Quickstart Issues

### Issue: "API key not found"

**Solution**:
```bash
# Create .env file
echo "ANTHROPIC_API_KEY=your_actual_key" > .env

# Verify
make check-api
```

### Issue: "Module not found"

**Solution**:
```bash
# Reinstall dependencies
uv sync

# Use uv run prefix
uv run socratic_web
```

### Issue: Web interface won't open

**Solution**:
```bash
# Check if port 7860 is in use
lsof -i :7860

# Use different port
uv run python -c "from socratic_sofa.gradio_app import demo; demo.launch(server_port=7861)"
```

### Issue: Dialogue takes too long

**Expected behavior**: 2-3 minutes is normal for quality output.

**If longer than 5 minutes**:
- Check your internet connection
- Verify API key has sufficient credits
- Check Anthropic API status at status.anthropic.com

## Next Steps

Now that you've run your first dialogue:

1. **Dive deeper**: Read the [first dialogue tutorial](./first-dialogue.md) for detailed explanations
2. **Customize**: Learn to modify agents and tasks in the main README
3. **Deploy**: Share your instance on Hugging Face Spaces
4. **Experiment**: Try different philosophical topics and observe the questioning patterns

## Quick Reference Commands

```bash
# Web interface
make web             # Launch Gradio interface
uv run socratic_web  # Alternative command

# Command line
make dev             # Run CLI dialogue
uv run socratic_sofa # Alternative command

# View results
make outputs         # Display all results
cat outputs/*.md     # View all files

# Utilities
make check-api       # Verify API configuration
make clean           # Clear output files
make help            # Show all commands
```

## Example Topics to Try

Here are some philosophical questions perfect for Socratic dialogue:

**Ethics**:
- What is the good life?
- Is morality objective or subjective?
- Can we justify civil disobedience?

**Epistemology**:
- What is the nature of knowledge?
- How do we distinguish truth from opinion?
- Can we trust our senses?

**Metaphysics**:
- What is consciousness?
- Do we have free will?
- What is the nature of time?

**Contemporary**:
- Should AI have rights?
- What are our obligations to future generations?
- Is privacy a fundamental right in the digital age?

## Resources

- **Full Documentation**: See main [README.md](../../README.md)
- **Installation Help**: [installation.md](./installation.md)
- **Detailed Tutorial**: [first-dialogue.md](./first-dialogue.md)
- **CrewAI Docs**: [docs.crewai.com](https://docs.crewai.com)
- **Report Issues**: GitHub Issues

---

**Congratulations!** You've successfully run your first Socratic dialogue. Continue to the [detailed tutorial](./first-dialogue.md) to understand how the system works under the hood.
