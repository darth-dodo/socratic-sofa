# Schemas API Reference

## Overview

The `schemas.py` module defines Pydantic models for structured output from Socratic Sofa dialogue tasks. These schemas ensure consistent, well-formatted output for better readability in the Gradio interface.

**Module Features**:

- **Structured Output**: Type-safe Pydantic models for all task outputs
- **Validation**: Automatic validation of field constraints (e.g., question counts, score ranges)
- **Formatting Functions**: Convert Pydantic models to readable markdown

**Dependencies**:

```python
from pydantic import BaseModel, Field
```

---

## Models

### `TopicOutput`

Structured output for the `propose_topic` task.

**Fields**:

| Field          | Type        | Description                                   | Constraints |
| -------------- | ----------- | --------------------------------------------- | ----------- |
| `topic`        | `str`       | The philosophical question for the dialogue   | Required    |
| `context`      | `str`       | Why this topic is philosophically significant | Required    |
| `key_concepts` | `list[str]` | Key philosophical concepts to explore         | 2-4 items   |

**Example**:

```python
from socratic_sofa.schemas import TopicOutput

output = TopicOutput(
    topic="What is justice?",
    context="Justice is a fundamental concept in moral and political philosophy.",
    key_concepts=["fairness", "virtue", "social order"]
)
```

---

### `SocraticQuestion`

A single Socratic question with its purpose.

**Fields**:

| Field      | Type  | Description                                    |
| ---------- | ----- | ---------------------------------------------- |
| `question` | `str` | The Socratic question itself                   |
| `purpose`  | `str` | What this question aims to reveal or challenge |

**Example**:

```python
from socratic_sofa.schemas import SocraticQuestion

question = SocraticQuestion(
    question="What do you mean by justice?",
    purpose="To clarify the definition being used"
)
```

---

### `InquiryOutput`

Structured output for the `propose` and `oppose` tasks (Socratic inquiries).

**Fields**:

| Field                 | Type                     | Description                                 | Constraints |
| --------------------- | ------------------------ | ------------------------------------------- | ----------- |
| `philosophical_angle` | `str`                    | The perspective being explored              | Required    |
| `opening_statement`   | `str`                    | Brief framing of the inquiry approach       | Required    |
| `questions`           | `list[SocraticQuestion]` | The Socratic questions                      | 5-7 items   |
| `insight_summary`     | `str`                    | Philosophical tensions or insights revealed | Required    |

**Example**:

```python
from socratic_sofa.schemas import InquiryOutput, SocraticQuestion

output = InquiryOutput(
    philosophical_angle="Individual moral experience",
    opening_statement="Let us examine justice from the individual's perspective.",
    questions=[
        SocraticQuestion(question="What do you mean by justice?", purpose="Clarify definition"),
        SocraticQuestion(question="Is justice the same as fairness?", purpose="Probe assumptions"),
        # ... 3-5 more questions
    ],
    insight_summary="Tensions between personal and societal justice emerge."
)
```

---

### `CriterionScore`

Score for a single evaluation criterion.

**Fields**:

| Field        | Type  | Description                    | Constraints   |
| ------------ | ----- | ------------------------------ | ------------- |
| `score`      | `int` | Score from 1-5                 | 1 ≤ score ≤ 5 |
| `assessment` | `str` | Brief explanation of the score | Required      |

**Example**:

```python
from socratic_sofa.schemas import CriterionScore

score = CriterionScore(
    score=4,
    assessment="Excellent questioning technique with genuine probing"
)
```

---

### `InquiryEvaluation`

Evaluation of a single inquiry.

**Fields**:

| Field                    | Type             | Description                                        |
| ------------------------ | ---------------- | -------------------------------------------------- |
| `question_quality`       | `CriterionScore` | Do questions genuinely probe? (40% weight)         |
| `elenctic_effectiveness` | `CriterionScore` | How well are contradictions revealed? (25% weight) |
| `philosophical_insight`  | `CriterionScore` | Depth and significance of insights (20% weight)    |
| `socratic_fidelity`      | `CriterionScore` | Adherence to Socratic method (15% weight)          |

---

### `JudgmentOutput`

Structured output for the `judge_task` (dialectic evaluation).

**Fields**:

| Field                        | Type                | Description                         | Constraints |
| ---------------------------- | ------------------- | ----------------------------------- | ----------- |
| `first_inquiry`              | `InquiryEvaluation` | Evaluation of first inquiry         | Required    |
| `second_inquiry`             | `InquiryEvaluation` | Evaluation of second inquiry        | Required    |
| `differentiation_score`      | `int`               | Bonus for differentiation           | 0-10        |
| `differentiation_assessment` | `str`               | How distinct the second inquiry is  | Required    |
| `winner`                     | `str`               | Which inquiry was more effective    | Required    |
| `socratic_exemplification`   | `str`               | Which better exemplifies the method | Required    |
| `recommendation`             | `str`               | Suggestion for deeper examination   | Required    |

---

## Formatting Functions

### `format_topic_output()`

Format `TopicOutput` as readable markdown.

**Signature**:

```python
def format_topic_output(output: TopicOutput) -> str
```

**Output Format**:

```markdown
## What is justice?

Justice is a fundamental concept in moral and political philosophy.

**Key Concepts:**

- fairness
- virtue
- social order
```

---

### `format_inquiry_output()`

Format `InquiryOutput` as readable markdown.

**Signature**:

```python
def format_inquiry_output(output: InquiryOutput, title: str, emoji: str) -> str
```

**Parameters**:

| Parameter | Type            | Description                                   |
| --------- | --------------- | --------------------------------------------- |
| `output`  | `InquiryOutput` | The inquiry to format                         |
| `title`   | `str`           | Section title (e.g., "First Line of Inquiry") |
| `emoji`   | `str`           | Emoji prefix (e.g., "🔵" or "🟢")             |

**Output Format**:

```markdown
## 🔵 First Line of Inquiry

**Philosophical Angle:** Individual moral experience

Let us examine justice from the individual's perspective.

---

### Question 1

> What do you mean by justice?

_Purpose: To clarify the definition_

### Question 2

> Is justice the same as fairness?

_Purpose: To probe assumptions_

---

**Insight:** Tensions between personal and societal justice emerge.
```

---

### `format_judgment_output()`

Format `JudgmentOutput` as readable markdown.

**Signature**:

```python
def format_judgment_output(output: JudgmentOutput) -> str
```

**Output Format**:

```markdown
## Dialectic Evaluation

### Scoring Breakdown

| Criterion                                | First Inquiry | Second Inquiry |
| ---------------------------------------- | ------------- | -------------- |
| **Question Quality** (40%)               | 4/5           | 4/5            |
| **Elenctic Effectiveness** (25%)         | 3/5           | 4/5            |
| **Philosophical Insight** (20%)          | 5/5           | 4/5            |
| **Socratic Fidelity** (15%)              | 4/5           | 4/5            |
| **Differentiation Quality** (bonus +10%) | N/A           | +7%            |
| **Total Score**                          | 82%           | 87%            |

### Assessment

**Winner**: Second

**Differentiation**: Second takes a completely different angle...

### Detailed Analysis

**First Inquiry:**

- ✅ **Question Quality** (4/5): Strong probing...
  ...

### Recommendation

_Explore the tension between individual and collective more deeply._
```

---

## Integration with CrewAI

The schemas integrate with CrewAI's `output_pydantic` parameter:

```python
from crewai import Task
from socratic_sofa.schemas import TopicOutput

@task
def propose_topic(self) -> Task:
    return Task(
        config=self.tasks_config["propose_topic"],
        callback=self.task_callback,
        output_pydantic=TopicOutput,
    )
```

---

## Fallback Behavior

The `format_task_output()` function in `gradio_app.py` handles cases where Pydantic parsing fails:

1. **Try Pydantic**: If `task_output.pydantic` exists, use the formatted output
2. **Fallback to Raw**: If parsing fails, use `task_output.raw` with appropriate headers

```python
def format_task_output(task_output, task_name: str) -> str:
    try:
        if hasattr(task_output, "pydantic") and task_output.pydantic is not None:
            # Use Pydantic formatting
            ...
        # Fallback to raw
        return task_output.raw
    except Exception:
        return task_output.raw
```

---

## Emoji Indicators

The formatting functions use consistent emoji indicators:

| Emoji | Meaning                    | Score Range |
| ----- | -------------------------- | ----------- |
| ✅    | Excellent/Strong           | 4-5         |
| ⚠️    | Adequate/Needs improvement | 3           |
| ❌    | Weak/Problematic           | 1-2         |

---

## Notes

- All schemas use Pydantic v2 syntax
- Field constraints are enforced at instantiation time
- Formatting functions are pure and side-effect free
- Raw output fallback ensures graceful degradation
