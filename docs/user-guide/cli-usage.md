# Command-Line Interface (CLI) Guide

This guide covers using Socratic Sofa from the command line, perfect for automation, batch processing, and programmatic access.

## Overview

The CLI provides direct access to Socratic Sofa's philosophical dialogue generation without the web interface. It's ideal for:

- Automated batch processing of multiple topics
- Integration with other tools and scripts
- Generating dialogues programmatically
- Research and analysis workflows
- Headless server environments

## Installation Verification

Before using the CLI, ensure Socratic Sofa is properly installed:

```bash
# Check installation
poetry --version

# Install dependencies if needed
poetry install

# Verify installation
poetry run python -c "from socratic_sofa.crew import SocraticSofa; print('✓ Installation verified')"
```

## Basic Usage

### Running a Dialogue

**Standard Method:**
```bash
poetry run socratic-sofa
```

**Using Make:**
```bash
make run
```

**Direct Python:**
```bash
poetry run python src/socratic_sofa/main.py
```

### What Happens

When you run the CLI:

1. **Default Topic**: Uses the hardcoded topic: `"how to enjoy life?"`
2. **Processing**: AI agents work through the Socratic dialogue
3. **Duration**: Takes 2-3 minutes to complete
4. **Output**: Results saved to `outputs/` directory
5. **Console**: Final result printed to terminal

### Console Output

**During Processing:**
```
[timestamp] Starting Socratic dialogue...
[timestamp] Agent: socratic_philosopher_proposition
[timestamp] Task: Explore through Socratic questioning...
[timestamp] Agent: socratic_philosopher_opposition
[timestamp] Task: Explore alternative perspective...
[timestamp] Agent: dialectic_moderator
[timestamp] Task: Evaluate dialogue quality...
```

**Final Output:**
```
Raw Result: [Final evaluation summary]
✓ Dialogue complete. Files saved to outputs/
```

## Output Files

### File Structure

Every dialogue generates four markdown files in the `outputs/` directory:

```
outputs/
├── 01_topic.md          # Selected/proposed topic
├── 02_proposition.md    # First line of inquiry
├── 03_opposition.md     # Alternative inquiry
└── 04_judgment.md       # Dialectic evaluation
```

### File Contents

#### 01_topic.md
```markdown
# Selected Topic: [Topic Name]

[Explanation of topic selection]
[Philosophical context]
[Why this topic matters]
```

#### 02_proposition.md
```markdown
# Socratic Inquiry: Proposition

**Initial Position:** [Starting point]

## Question 1
[First probing question]

## Question 2
[Building on previous responses]

[Continues through systematic questioning...]
```

#### 03_opposition.md
```markdown
# Socratic Inquiry: Opposition

**Alternative Angle:** [Different perspective]

## Question 1
[Questions from alternative viewpoint]

[Alternative line of inquiry...]
```

#### 04_judgment.md
```markdown
# Dialectic Evaluation

## Quality Assessment
[How well did the dialogue follow Socratic method?]

## Strengths
[What worked well]

## Areas for Improvement
[Opportunities for deeper exploration]

## Overall Effectiveness
[Meta-commentary on philosophical process]
```

### File Management

**Important Notes:**
- Files are overwritten with each new dialogue
- Save important dialogues before running again
- Consider renaming outputs to preserve them
- Use version control (git) to track dialogue history

**Preserving Outputs:**
```bash
# Save current dialogue with topic name
cp outputs/01_topic.md "saved_dialogues/justice_$(date +%Y%m%d).md"
cp outputs/02_proposition.md "saved_dialogues/justice_prop_$(date +%Y%m%d).md"
cp outputs/03_opposition.md "saved_dialogues/justice_opp_$(date +%Y%m%d).md"
cp outputs/04_judgment.md "saved_dialogues/justice_eval_$(date +%Y%m%d).md"

# Or backup entire directory
cp -r outputs "saved_dialogues/dialogue_$(date +%Y%m%d_%H%M%S)"
```

## Custom Topics

### Modifying the Default Topic

To run with a different topic, you need to modify the source code:

**File Location:** `src/socratic_sofa/main.py`

**Current Default:**
```python
def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'how to enjoy life?',  # ← Change this line
        'current_year': str(datetime.now().year)
    }
```

**Modify Topic:**
```python
def run():
    """
    Run the crew with custom topic.
    """
    inputs = {
        'topic': 'What is justice?',  # Your custom topic
        'current_year': str(datetime.now().year)
    }
```

**Run Modified Version:**
```bash
poetry run socratic-sofa
```

### Programmatic Topic Selection

For automated topic selection, create a custom script:

**File:** `custom_dialogue.py`
```python
#!/usr/bin/env python
"""Custom Socratic dialogue runner"""

import sys
from datetime import datetime
from socratic_sofa.crew import SocraticSofa

def run_dialogue(topic: str):
    """Run dialogue with specified topic"""
    inputs = {
        'topic': topic,
        'current_year': str(datetime.now().year)
    }

    try:
        results = SocraticSofa().crew().kickoff(inputs=inputs)
        print(f"\n✓ Dialogue complete for topic: {topic}")
        print(f"✓ Results saved to outputs/")
        return results.raw
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python custom_dialogue.py 'Your Topic Here'")
        sys.exit(1)

    topic = sys.argv[1]
    run_dialogue(topic)
```

**Usage:**
```bash
poetry run python custom_dialogue.py "What is truth?"
poetry run python custom_dialogue.py "Should AI have rights?"
poetry run python custom_dialogue.py "Is beauty objective?"
```

## Batch Processing

### Processing Multiple Topics

Create a batch processing script for multiple topics:

**File:** `batch_dialogues.py`
```python
#!/usr/bin/env python
"""Batch process multiple topics"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from socratic_sofa.crew import SocraticSofa

def save_dialogue(topic: str, outputs_dir: Path):
    """Save dialogue outputs with topic-specific names"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_'))
    safe_topic = safe_topic.replace(' ', '_')[:50]

    save_dir = outputs_dir / f"{safe_topic}_{timestamp}"
    save_dir.mkdir(parents=True, exist_ok=True)

    # Copy outputs to saved location
    for file in Path("outputs").glob("*.md"):
        shutil.copy(file, save_dir / file.name)

    print(f"✓ Saved to: {save_dir}")

def batch_process(topics: list[str], save_outputs: bool = True):
    """Process multiple topics"""
    results = []
    outputs_dir = Path("batch_outputs")
    outputs_dir.mkdir(exist_ok=True)

    for i, topic in enumerate(topics, 1):
        print(f"\n{'='*60}")
        print(f"Processing {i}/{len(topics)}: {topic}")
        print(f"{'='*60}\n")

        inputs = {
            'topic': topic,
            'current_year': str(datetime.now().year)
        }

        try:
            crew = SocraticSofa().crew()
            result = crew.kickoff(inputs=inputs)
            results.append({'topic': topic, 'result': result, 'success': True})

            if save_outputs:
                save_dialogue(topic, outputs_dir)

        except Exception as e:
            print(f"✗ Error processing '{topic}': {e}")
            results.append({'topic': topic, 'error': str(e), 'success': False})

    # Summary
    print(f"\n{'='*60}")
    print("BATCH PROCESSING COMPLETE")
    print(f"{'='*60}")
    print(f"Total topics: {len(topics)}")
    print(f"Successful: {sum(1 for r in results if r['success'])}")
    print(f"Failed: {sum(1 for r in results if not r['success'])}")

    return results

if __name__ == "__main__":
    # Define your topics
    topics = [
        "What is justice?",
        "Can machines think?",
        "Is lying ever justified?",
        "What is consciousness?",
        "Should we colonize Mars?"
    ]

    batch_process(topics, save_outputs=True)
```

**Usage:**
```bash
poetry run python batch_dialogues.py
```

**Expected Output Structure:**
```
batch_outputs/
├── What_is_justice_20250117_143022/
│   ├── 01_topic.md
│   ├── 02_proposition.md
│   ├── 03_opposition.md
│   └── 04_judgment.md
├── Can_machines_think_20250117_144531/
│   └── [similar files...]
└── [more dialogues...]
```

## Advanced CLI Features

### Training Mode

Train the AI agents on specific topics to improve performance:

**Command:**
```bash
poetry run python src/socratic_sofa/main.py train <iterations> <filename>
```

**Example:**
```bash
poetry run python src/socratic_sofa/main.py train 5 training_results.json
```

**What It Does:**
- Runs the topic `"AI LLMs"` multiple times
- Collects performance data
- Saves training results to specified file
- Improves agent responses over iterations

**Parameters:**
- `iterations`: Number of training cycles (recommended: 5-10)
- `filename`: JSON file to store training data

### Test Mode

Test crew performance with evaluation:

**Command:**
```bash
poetry run python src/socratic_sofa/main.py test <iterations> <eval_model>
```

**Example:**
```bash
poetry run python src/socratic_sofa/main.py test 3 gpt-4
```

**What It Does:**
- Runs test topic `"AI LLMs"`
- Evaluates dialogue quality
- Uses specified LLM for evaluation
- Generates performance metrics

**Parameters:**
- `iterations`: Number of test cycles
- `eval_model`: LLM model for evaluation (e.g., `gpt-4`, `claude-3`)

### Replay Mode

Replay a specific task from a previous run:

**Command:**
```bash
poetry run python src/socratic_sofa/main.py replay <task_id>
```

**Example:**
```bash
poetry run python src/socratic_sofa/main.py replay task_abc123
```

**What It Does:**
- Replays a specific task execution
- Useful for debugging
- Reproduces exact conditions
- Shows detailed task flow

### Trigger Mode

Run with external trigger payloads (for integrations):

**Command:**
```bash
poetry run python src/socratic_sofa/main.py run_with_trigger '{"topic":"Custom topic","context":"Additional context"}'
```

**What It Does:**
- Accepts JSON payload as input
- Useful for webhook integrations
- Enables external system triggers
- Supports custom parameters

## Output Management

### Reading Outputs Programmatically

**Python Script:**
```python
from pathlib import Path

def read_dialogue_outputs():
    """Read all dialogue output files"""
    outputs = {}

    files = {
        'topic': '01_topic.md',
        'proposition': '02_proposition.md',
        'opposition': '03_opposition.md',
        'judgment': '04_judgment.md'
    }

    for key, filename in files.items():
        filepath = Path('outputs') / filename
        if filepath.exists():
            with open(filepath, 'r') as f:
                outputs[key] = f.read()

    return outputs

# Usage
dialogue = read_dialogue_outputs()
print(f"Topic: {dialogue['topic'][:100]}...")
print(f"Proposition length: {len(dialogue['proposition'])} chars")
```

### Converting Outputs

**To HTML:**
```bash
# Using pandoc
pandoc outputs/02_proposition.md -o proposition.html

# For all files
for file in outputs/*.md; do
    pandoc "$file" -o "${file%.md}.html"
done
```

**To PDF:**
```bash
# Using pandoc with LaTeX
pandoc outputs/02_proposition.md -o proposition.pdf

# Better styling
pandoc outputs/02_proposition.md \
    --pdf-engine=xelatex \
    -V geometry:margin=1in \
    -o proposition.pdf
```

**To DOCX:**
```bash
pandoc outputs/02_proposition.md -o proposition.docx
```

### Analyzing Outputs

**Word Count:**
```bash
wc -w outputs/*.md
```

**Extract Questions:**
```bash
grep -h "^## Question\|^\\*\\*Question" outputs/02_proposition.md
```

**Compare Dialogues:**
```bash
diff outputs/02_proposition.md saved_dialogues/justice_prop.md
```

## Environment Configuration

### Required Environment Variables

**OpenAI API (Required):**
```bash
export OPENAI_API_KEY="sk-..."
```

**Optional Variables:**
```bash
# Model selection (default: gpt-4o)
export OPENAI_MODEL_NAME="gpt-4o"

# CrewAI settings
export CREWAI_TELEMETRY=false  # Disable telemetry

# Logging
export LOG_LEVEL="INFO"
```

### Configuration File

Create a `.env` file in the project root:

```bash
# .env file
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL_NAME=gpt-4o
CREWAI_TELEMETRY=false
```

**Load automatically:**
```bash
# Install python-dotenv if needed
poetry add python-dotenv

# Loads automatically in Python
from dotenv import load_dotenv
load_dotenv()
```

## Integration Examples

### Shell Script Wrapper

**File:** `run_dialogue.sh`
```bash
#!/bin/bash
# Wrapper script for Socratic Sofa

TOPIC="${1:-What is happiness?}"
OUTPUT_DIR="saved_dialogues/$(date +%Y%m%d_%H%M%S)"

echo "Running dialogue: $TOPIC"

# Run dialogue
poetry run python -c "
from datetime import datetime
from socratic_sofa.crew import SocraticSofa

inputs = {
    'topic': '$TOPIC',
    'current_year': str(datetime.now().year)
}

SocraticSofa().crew().kickoff(inputs=inputs)
"

# Save outputs
mkdir -p "$OUTPUT_DIR"
cp outputs/*.md "$OUTPUT_DIR/"

echo "Dialogue saved to: $OUTPUT_DIR"
```

**Usage:**
```bash
chmod +x run_dialogue.sh
./run_dialogue.sh "What is truth?"
```

### Python API Wrapper

**File:** `dialogue_api.py`
```python
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from socratic_sofa.crew import SocraticSofa

class DialogueRunner:
    """Simple API wrapper for Socratic dialogues"""

    def __init__(self, outputs_dir: str = "outputs"):
        self.outputs_dir = Path(outputs_dir)
        self.outputs_dir.mkdir(exist_ok=True)

    def run(self, topic: str) -> Dict[str, str]:
        """Run dialogue and return all outputs"""
        inputs = {
            'topic': topic,
            'current_year': str(datetime.now().year)
        }

        # Run crew
        crew = SocraticSofa().crew()
        crew.kickoff(inputs=inputs)

        # Read outputs
        return self._read_outputs()

    def _read_outputs(self) -> Dict[str, str]:
        """Read all output files"""
        outputs = {}

        files = {
            'topic': '01_topic.md',
            'proposition': '02_proposition.md',
            'opposition': '03_opposition.md',
            'judgment': '04_judgment.md'
        }

        for key, filename in files.items():
            filepath = self.outputs_dir / filename
            with open(filepath, 'r') as f:
                outputs[key] = f.read()

        return outputs

# Usage
if __name__ == "__main__":
    runner = DialogueRunner()
    result = runner.run("What is consciousness?")
    print(f"Topic: {result['topic'][:200]}...")
```

## Troubleshooting

### Common Issues

**Problem: ModuleNotFoundError**
```
Solution: Ensure proper installation
$ poetry install
$ poetry run socratic-sofa
```

**Problem: API Key Error**
```
Solution: Set environment variable
$ export OPENAI_API_KEY="sk-..."
$ poetry run socratic-sofa
```

**Problem: Permission Denied**
```
Solution: Check file permissions
$ chmod +x run_dialogue.sh
$ ls -l outputs/
```

**Problem: Outputs Not Generated**
```
Solution: Check outputs/ directory exists
$ mkdir -p outputs
$ poetry run socratic-sofa
```

**Problem: Long Processing Time**
```
Normal: 2-3 minutes is expected
Check: API rate limits or network issues
Try: Simpler topic or different model
```

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Then run normally
from socratic_sofa.crew import SocraticSofa
# ... rest of code
```

## Performance Tips

### Optimization Strategies

**1. Model Selection:**
```python
# Faster but less sophisticated
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"

# Balanced (default)
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

# Highest quality
os.environ["OPENAI_MODEL_NAME"] = "gpt-4-turbo"
```

**2. Batch Processing:**
- Process topics during off-peak hours
- Use parallel processing cautiously (API limits)
- Save outputs immediately to prevent data loss

**3. Error Handling:**
```python
import time

def run_with_retry(topic: str, max_retries: int = 3):
    """Run dialogue with retry logic"""
    for attempt in range(max_retries):
        try:
            return run_dialogue(topic)
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s")
                time.sleep(wait_time)
            else:
                raise
```

## Best Practices

### For Development

1. **Version Control**: Commit important dialogues to git
2. **Naming Convention**: Use descriptive, consistent names
3. **Documentation**: Comment custom scripts thoroughly
4. **Error Handling**: Always include try-except blocks
5. **Logging**: Use Python logging instead of print

### For Production

1. **Environment Variables**: Never hardcode API keys
2. **Rate Limiting**: Respect API usage limits
3. **Monitoring**: Log all dialogue generations
4. **Backup**: Regularly backup outputs directory
5. **Testing**: Test with simple topics before complex ones

### For Research

1. **Reproducibility**: Save exact inputs and timestamps
2. **Metadata**: Include model version and parameters
3. **Organization**: Use systematic directory structures
4. **Analysis**: Process outputs with consistent methods
5. **Documentation**: Maintain research logs

## Next Steps

- [Web Interface Guide](./web-interface.md) - Learn about the GUI
- [Topic Library Guide](./topic-library.md) - Explore available topics
- [Custom Topics Guide](./custom-topics.md) - Create effective questions
- [Architecture Documentation](../architecture.md) - Understand the system

## Conclusion

The CLI provides powerful, flexible access to Socratic Sofa's capabilities. Whether you're automating batch processing, integrating with other tools, or conducting research, the command-line interface offers the control and programmability needed for advanced use cases.

Experiment with different topics, build custom workflows, and leverage the full power of AI-guided philosophical inquiry from your terminal.
