# Gradio App API Reference

## Overview

The `gradio_app.py` module provides a web interface for Socratic Sofa using Gradio. It manages user input, topic selection, content moderation, and displays the philosophical dialogue outputs.

**Module Features**:

- **Structured Output Formatting**: Pydantic models converted to readable markdown
- **Structured Logging**: Context-aware logging for all web interface operations
- **Performance Tracking**: Automatic timing of dialogue generation and crew execution
- **Error Handling**: Graceful degradation with user-friendly error messages
- **Warm Design**: Calming UI with cream, orange and peach color palette

**Dependencies**:

```python
from socratic_sofa.logging_config import get_logger, log_timing
from socratic_sofa.content_filter import is_topic_appropriate, get_alternative_suggestions
from socratic_sofa.crew import SocraticSofa
from socratic_sofa.schemas import (
    format_topic_output,
    format_inquiry_output,
    format_judgment_output,
)
```

---

## Functions

### `format_task_output()`

Formats CrewAI task output using Pydantic schemas for readable markdown display.

**Signature**:

```python
def format_task_output(task_output, task_name: str) -> str
```

**Parameters**:

| Parameter     | Type  | Description                                           |
| ------------- | ----- | ----------------------------------------------------- |
| `task_output` | `Any` | CrewAI TaskOutput object with pydantic or raw content |
| `task_name`   | `str` | Name of the task for formatting selection             |

**Returns**: `str` - Formatted markdown string

**Formatting Logic**:

| Task Name       | Pydantic Model   | Formatting Function        |
| --------------- | ---------------- | -------------------------- |
| `propose_topic` | `TopicOutput`    | `format_topic_output()`    |
| `propose`       | `InquiryOutput`  | `format_inquiry_output()`  |
| `oppose`        | `InquiryOutput`  | `format_inquiry_output()`  |
| `judge_task`    | `JudgmentOutput` | `format_judgment_output()` |

**Fallback Behavior**:

If Pydantic parsing fails, the function gracefully falls back to raw output:

```python
def format_task_output(task_output, task_name: str) -> str:
    try:
        if hasattr(task_output, "pydantic") and task_output.pydantic is not None:
            # Use Pydantic formatting
            ...
        return task_output.raw
    except Exception:
        return task_output.raw
```

**Example**:

```python
# In run_socratic_dialogue()
topic_output = format_task_output(
    crew_output.tasks_output[0],
    "propose_topic"
)
# Returns formatted markdown with topic, context, and key concepts
```

---

### `load_topics()`

Loads the topic library from the YAML configuration file.

**Returns**: `list[str]`

**Description**: Reads `topics.yaml` and flattens the hierarchical topic structure into a single list with category labels in the format `[Category] Topic`.

**Return Value**:

- On success: List of topics with category prefixes
- On error: Default fallback list of basic philosophical questions

**Example**:

```python
topics = load_topics()
# Returns: ['[Ethics] What is justice?', '[Metaphysics] What is reality?', ...]
```

**Error Handling**:

```python
logger = get_logger(__name__)

try:
    with open(topics_file, 'r') as f:
        topics_data = yaml.safe_load(f)
    # Process topics...
    logger.info("Topics loaded successfully", extra={"count": len(topics)})
except Exception as e:
    logger.error("Error loading topics", extra={"error": str(e)})
    return ["What is justice?", "What is happiness?", "What is truth?"]
```

---

### `handle_topic_selection()`

Determines which topic to use based on dropdown and textbox inputs.

**Signature**:

```python
def handle_topic_selection(
    dropdown_value: str = None,
    textbox_value: str = None
) -> str
```

**Parameters**:

| Parameter        | Type  | Default | Description                       |
| ---------------- | ----- | ------- | --------------------------------- |
| `dropdown_value` | `str` | `None`  | Topic selected from dropdown menu |
| `textbox_value`  | `str` | `None`  | Custom topic entered by user      |

**Returns**: `str` - The final topic to use for dialogue

**Priority Logic**:

1. **Textbox** (highest priority): If user typed a custom topic, use it
2. **Empty string**: If dropdown is "✨ Let AI choose" or empty
3. **Dropdown value**: Extract topic from `[Category] Topic` format
4. **Empty string**: If no valid input

**Example**:

```python
# User typed custom topic - takes priority
topic = handle_topic_selection(
    dropdown_value="[Ethics] What is justice?",
    textbox_value="Is artificial intelligence conscious?"
)
# Returns: "Is artificial intelligence conscious?"

# Using dropdown selection
topic = handle_topic_selection(
    dropdown_value="[Ethics] What is justice?",
    textbox_value=""
)
# Returns: "What is justice?"

# Let AI choose
topic = handle_topic_selection(
    dropdown_value="✨ Let AI choose",
    textbox_value=""
)
# Returns: ""

# Extract from formatted dropdown
topic = handle_topic_selection(
    dropdown_value="[Metaphysics] What is reality?",
    textbox_value=None
)
# Returns: "What is reality?"
```

**Implementation Details**:

```python
# Check textbox first
if textbox_value and str(textbox_value).strip():
    return str(textbox_value).strip()

# Handle "Let AI choose" option
if dropdown_value == "✨ Let AI choose":
    return ""

# Extract topic from "[Category] Topic" format
if "] " in dropdown_value:
    return dropdown_value.split("] ", 1)[1]

return dropdown_value
```

---

### `run_socratic_dialogue()`

Executes the Socratic dialogue crew and returns all outputs.

**Signature**:

```python
def run_socratic_dialogue(
    dropdown_topic: str,
    custom_topic: str
) -> tuple[str, str, str, str]
```

**Parameters**:

| Parameter        | Type  | Description                       |
| ---------------- | ----- | --------------------------------- |
| `dropdown_topic` | `str` | Topic selected from dropdown menu |
| `custom_topic`   | `str` | Custom topic entered by user      |

**Returns**: `tuple[str, str, str, str]`

Tuple containing:

1. **Topic output**: Refined/proposed topic
2. **Proposition output**: First line of inquiry
3. **Opposition output**: Alternative inquiry
4. **Judgment output**: Evaluation

**Process Flow**:

1. Determine final topic using `handle_topic_selection()`
2. Run content moderation check
3. Prepare inputs for crew
4. Execute crew.kickoff() with streaming callbacks
5. Return all outputs via streaming generator

**Example**:

```python
# Run dialogue with dropdown selection
topic_out, prop_out, opp_out, judge_out = run_socratic_dialogue(
    dropdown_topic="[Ethics] What is justice?",
    custom_topic=""
)

# Run dialogue with custom topic
topic_out, prop_out, opp_out, judge_out = run_socratic_dialogue(
    dropdown_topic="✨ Let AI choose",
    custom_topic="Can machines have consciousness?"
)

# Display results
print(topic_out)        # Refined topic
print(prop_out)         # First inquiry with header
print(opp_out)          # Alternative inquiry with header
print(judge_out)        # Evaluation
```

**Content Moderation**:

```python
is_appropriate, rejection_reason = is_topic_appropriate(final_topic)
if not is_appropriate:
    error_msg = f"⚠️ {rejection_reason}\n\n"
    error_msg += "**Suggested topics:**\n"
    for suggestion in get_alternative_suggestions():
        error_msg += f"- {suggestion}\n"
    return error_msg, error_msg, error_msg, error_msg
```

**Error Handling**:

```python
try:
    crew = SocraticSofa().crew()
    result = crew.kickoff(inputs=inputs)
    # Read outputs...
except Exception as e:
    error_msg = f"Error running dialogue: {str(e)}"
    return error_msg, error_msg, error_msg, error_msg
```

**Section Headers**:
The function automatically adds visual headers to distinguish dialogue sections:

- Proposition: `"## 🔵 First Line of Inquiry\n\n"`
- Opposition: `"## 🟢 Alternative Line of Inquiry\n\n"`

**Logging**:

The function uses structured logging to track topic selection:

```python
logger = get_logger(__name__)

logger.debug(
    "Topic selection debug",
    extra={
        "dropdown": dropdown_topic,
        "custom": custom_topic,
        "final": final_topic
    }
)
```

**Performance Tracking**:

Crew execution is wrapped with automatic timing:

```python
with log_timing(logger, "crew_execution", topic=final_topic):
    crew = SocraticSofa().crew()
    result = crew.kickoff(inputs=inputs)
```

This automatically logs:

- Start of execution with context
- Completion time and success
- Error details if execution fails

---

### `main()`

Launches the Gradio web interface with configured settings.

**Signature**:

```python
def main() -> None
```

**Configuration**:

| Setting         | Value            | Description                     |
| --------------- | ---------------- | ------------------------------- |
| `server_name`   | `"0.0.0.0"`      | Accept connections from any IP  |
| `server_port`   | `7860`           | Port for the web server         |
| `share`         | `False`          | Don't create public Gradio link |
| `theme`         | `gr.themes.Soft` | Soft theme with custom colors   |
| `primary_hue`   | `"indigo"`       | Primary color scheme            |
| `secondary_hue` | `"purple"`       | Secondary color scheme          |

**Example**:

```python
# Launch the web interface
if __name__ == "__main__":
    main()

# Server will be available at http://localhost:7860
```

**Customization**:

```python
def main():
    """Launch with custom configuration"""
    demo.launch(
        server_name="0.0.0.0",
        server_port=8080,  # Custom port
        share=True,        # Create public link
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="green",
        )
    )
```

---

## Gradio Interface

### Components

The interface uses `gr.Blocks()` with custom CSS for mobile responsiveness.

**Input Components**:

| Component        | Type          | Purpose                             |
| ---------------- | ------------- | ----------------------------------- |
| `topic_dropdown` | `gr.Dropdown` | Select from curated topic library   |
| `topic_input`    | `gr.Textbox`  | Enter custom philosophical question |
| `run_button`     | `gr.Button`   | Trigger dialogue execution          |

**Output Components**:

| Component            | Type          | Content               |
| -------------------- | ------------- | --------------------- |
| `topic_output`       | `gr.Markdown` | Refined topic         |
| `proposition_output` | `gr.Markdown` | First line of inquiry |
| `opposition_output`  | `gr.Markdown` | Alternative inquiry   |
| `judgment_output`    | `gr.Markdown` | Dialectic evaluation  |

### Event Handling

```python
run_button.click(
    fn=run_socratic_dialogue,
    inputs=[topic_dropdown, topic_input],
    outputs=[topic_output, proposition_output, opposition_output, judgment_output]
)
```

---

## Global Constants

### `TOPICS`

**Type**: `list[str]`

**Description**: Pre-loaded list of philosophical topics from `topics.yaml`, populated at module initialization.

**Format**: `["✨ Let AI choose", "[Category] Topic1", "[Category] Topic2", ...]`

**Example**:

```python
from socratic_sofa.gradio_app import TOPICS

print(len(TOPICS))  # Number of available topics
print(TOPICS[0])    # "✨ Let AI choose"
print(TOPICS[1])    # "[Ethics] What is justice?"
```

---

## Warm Design

The interface features a calming design with warm cream, orange and peach colors:

### Color Palette

```css
:root {
  --orange: #f47d31; /* Primary accent */
  --orange-dark: #e06820; /* Dark accent */
  --coral: #ff8c69; /* Warm highlight */
  --peach: #ffb088; /* Medium accent */
  --peach-light: #ffdab9; /* Light accent */
  --peach-cream: #fff0e5; /* Very light accent */
  --cream: #fff8f0; /* Background */
  --warm-white: #fffbf5; /* Cards */
  --soft-peach: #f5e6da; /* Borders */
  --text: #5c3d2e; /* Primary text */
  --text-light: #8b6b5c; /* Secondary text */
}
```

### Key Design Features

- **Soft Rounded Corners**: 50px for buttons, 24px for cards
- **Gradient Buttons**: Orange-to-coral gradient for primary actions
- **Breathing Animation**: Subtle scale animation on active progress stages
- **Smooth Transitions**: Cubic-bezier easing on all interactive elements
- **Touch-Friendly**: Minimum 48px height for mobile touch targets

### Animations

```css
@keyframes breathe {
  0%,
  100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.03);
    opacity: 0.92;
  }
}

.stage.active {
  animation: breathe 3s ease-in-out infinite;
}
```

---

## Mobile Responsive Design

The interface includes comprehensive CSS for mobile optimization:

- **Breakpoint**: `@media (max-width: 768px)`
- **Touch targets**: Minimum 48px height for buttons
- **Typography**: Scaled font sizes for mobile readability
- **Layout**: Single-column stacking on small screens
- **Spacing**: Optimized padding and margins for mobile

**Key Mobile Features**:

```css
button {
  min-height: 48px; /* Touch-friendly */
  width: 100%; /* Full width on mobile */
  border-radius: 50px; /* Pill-shaped buttons */
}

.prose h1 {
  font-size: 1.5rem; /* Scaled for mobile */
}
```

---

## Complete Integration Example

```python
from socratic_sofa.gradio_app import (
    load_topics,
    handle_topic_selection,
    run_socratic_dialogue,
    main
)

# Load available topics
topics = load_topics()
print(f"Available topics: {len(topics)}")

# Manually run a dialogue (without Gradio UI)
topic, prop, opp, judge = run_socratic_dialogue(
    dropdown_topic="[Ethics] What is the good life?",
    custom_topic=""
)

print(f"Topic: {topic[:100]}...")
print(f"Proposition: {prop[:100]}...")
print(f"Opposition: {opp[:100]}...")
print(f"Judgment: {judge[:100]}...")

# Or launch the web interface
main()
```

---

## Environment Requirements

- **ANTHROPIC_API_KEY**: Required for AI model access
- **Python**: 3.10+
- **Dependencies**: gradio, crewai, anthropic, pyyaml

---

## File Dependencies

| File          | Purpose                     |
| ------------- | --------------------------- |
| `topics.yaml` | Topic library configuration |

---

## Notes

- Interface is designed mobile-first with responsive breakpoints
- Content moderation runs before dialogue execution
- Outputs are streamed in real-time as tasks complete
- Debug logging prints topic selection details to console
- Error messages are user-friendly and suggest alternatives
- Execution time is typically 2-3 minutes per dialogue
