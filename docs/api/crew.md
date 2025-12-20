# Crew API Reference

## Overview

The `crew.py` module defines the core `SocraticSofa` crew class that orchestrates the philosophical dialogue system using CrewAI agents and tasks.

## Classes

### `SocraticSofa`

**Inherits**: `CrewBase`

The main crew class that manages the Socratic dialogue process using specialized AI agents following the Socratic method.

#### Attributes

| Attribute | Type              | Description                                     |
| --------- | ----------------- | ----------------------------------------------- |
| `agents`  | `List[BaseAgent]` | List of AI agents participating in the dialogue |
| `tasks`   | `List[Task]`      | List of sequential tasks to execute             |

---

## Agent Methods

### `socratic_questioner()`

Creates the primary Socratic philosopher agent responsible for conducting philosophical inquiry.

**Decorator**: `@agent`

**Returns**: `Agent`

**Configuration**: Loaded from `agents_config['socratic_questioner']`

**Description**: This agent is trained in the Socratic method and guides philosophical inquiry through systematic questioning, exposing contradictions, and maintaining intellectual humility.

**Example**:

```python
crew = SocraticSofa()
questioner = crew.socratic_questioner()
# Agent is automatically used when crew.kickoff() is called
```

---

### `judge()`

Creates the dialectic moderator agent that evaluates the quality of philosophical inquiry.

**Decorator**: `@agent`

**Returns**: `Agent`

**Configuration**: Loaded from `agents_config['judge']`

**Description**: This agent assesses whether the dialogue follows authentic Socratic principles, evaluates the effectiveness of questioning, and provides critical feedback on the dialectic process.

**Example**:

```python
crew = SocraticSofa()
judge_agent = crew.judge()
# Agent is automatically used when crew.kickoff() is called
```

---

## Task Methods

### `propose_topic()`

Task for proposing or refining the philosophical topic for discussion.

**Decorator**: `@task`

**Returns**: `Task`

**Configuration**: Loaded from `tasks_config['propose_topic']`

**Description**: Analyzes and refines the input topic, ensuring it's suitable for Socratic inquiry. If no topic is provided, the AI selects an appropriate philosophical question.

**Example**:

```python
task = crew.propose_topic()
# Task executes automatically as part of sequential crew process
```

---

### `propose()`

Task for conducting the first line of Socratic inquiry.

**Decorator**: `@task`

**Returns**: `Task`

**Configuration**: Loaded from `tasks_config['propose']`

**Description**: The socratic_questioner agent conducts a series of probing questions following the Socratic method: establishing definitions, examining assumptions, revealing contradictions, and moving toward deeper understanding.

**Example**:

```python
task = crew.propose()
# Depends on propose_topic() output
```

---

### `oppose()`

Task for conducting an alternative line of Socratic inquiry from a different angle.

**Decorator**: `@task`

**Returns**: `Task`

**Configuration**: Loaded from `tasks_config['oppose']`

**Description**: Explores the same topic from a contrasting perspective, revealing additional dimensions and contradictions through Socratic questioning. This creates a richer dialectic by examining multiple viewpoints.

**Example**:

```python
task = crew.oppose()
# Depends on propose() output
```

---

### `judge_task()`

Task for evaluating the quality of the Socratic dialogue.

**Decorator**: `@task`

**Returns**: `Task`

**Configuration**: Loaded from `tasks_config['judge_task']`

**Description**: The judge agent evaluates whether the dialogue followed authentic Socratic principles, assesses the effectiveness of questioning, and provides critical feedback on both lines of inquiry.

**Example**:

```python
task = crew.judge_task()
# Depends on both propose() and oppose() outputs
```

---

### `crew()`

Creates and returns the configured Crew instance.

**Decorator**: `@crew`

**Returns**: `Crew`

**Configuration**:

- **agents**: All agents defined in the class
- **tasks**: All tasks defined in the class
- **process**: `Process.sequential` (tasks execute in order)
- **verbose**: `True` (detailed logging enabled)

**Description**: Assembles the complete crew with agents and tasks, configured for sequential execution. This is the main method for initializing the Socratic dialogue system.

**Example**:

```python
# Initialize and run the crew
from socratic_sofa.crew import SocraticSofa
from datetime import datetime

crew = SocraticSofa().crew()

inputs = {
    'topic': 'What is justice?',
    'current_year': str(datetime.now().year)
}

result = crew.kickoff(inputs=inputs)
print(result.raw)
```

---

## Complete Usage Example

```python
from socratic_sofa.crew import SocraticSofa
from datetime import datetime

# Create the crew
socratic_crew = SocraticSofa()
crew_instance = socratic_crew.crew()

# Prepare inputs
inputs = {
    'topic': 'What is the nature of consciousness?',
    'current_year': str(datetime.now().year)
}

# Execute the dialogue
result = crew_instance.kickoff(inputs=inputs)

# Access the result
print(f"Result: {result.raw}")
```

---

## Execution Flow

The crew executes tasks in the following sequential order:

1. **propose_topic**: Analyzes/refines the input topic
2. **propose**: First line of Socratic inquiry
3. **oppose**: Alternative line of inquiry
4. **judge_task**: Evaluation of the dialogue quality

Each task's output is passed to the next task in the sequence via CrewAI's context mechanism.

---

## Configuration Files

The crew relies on external YAML configuration files:

- **agents.yaml**: Defines agent roles, goals, and backstories
- **tasks.yaml**: Defines task descriptions, expected outputs, and agent assignments

These files should be placed in the `config/` directory relative to the crew definition.

---

## Error Handling

All methods are configured with `verbose=True` for detailed logging. Errors during crew execution should be caught and handled by the calling code:

```python
try:
    result = SocraticSofa().crew().kickoff(inputs=inputs)
except Exception as e:
    print(f"Error during dialogue: {e}")
```

---

## Notes

- All agents operate with `verbose=True` for transparency in the Socratic process
- Tasks execute sequentially, ensuring proper dialogue flow
- Outputs are streamed in real-time via task callbacks
- The crew requires valid ANTHROPIC_API_KEY environment variable
- Type hints use `# type: ignore[index]` for config dictionary access
