# Task Workflow Documentation

## Overview

Socratic Sofa implements a sequential task pipeline where four distinct tasks execute in strict order. Each task builds upon the output of previous tasks, creating a complete Socratic dialogue with evaluation.

## Task Pipeline Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Task Execution Flow                       │
└──────────────────────────────────────────────────────────────┘

Task 1: propose_topic
├── Agent: Socratic Philosopher
├── Input: {topic, current_year}
├── Output: 01_topic.md
└── Duration: ~10-20 seconds
         │
         ↓ [Topic Definition]

Task 2: propose
├── Agent: Socratic Philosopher
├── Input: {topic, current_year} + Task 1 output
├── Output: 02_proposition.md
└── Duration: ~40-60 seconds
         │
         ↓ [First Dialogue]

Task 3: oppose
├── Agent: Socratic Philosopher
├── Input: {topic, current_year} + Tasks 1-2 output
├── Output: 03_opposition.md
└── Duration: ~40-60 seconds
         │
         ↓ [Alternative Dialogue]

Task 4: judge_task
├── Agent: Dialectic Moderator
├── Input: Tasks 1-3 output
├── Output: 04_judgment.md
└── Duration: ~30-50 seconds
         │
         ↓ [Final Evaluation]

Total Duration: 120-180 seconds
```

## Task Definitions

## Task 1: propose_topic

### Purpose
Generate or refine the philosophical topic for Socratic inquiry.

### Configuration

```yaml
description: >
  {topic}

  If a topic was provided above, use it exactly as given. If no topic
  was provided (empty input), propose an engaging philosophical topic
  suitable for Socratic inquiry. The topic should invite examination
  of assumptions, definitions, and beliefs through systematic questioning.

expected_output: >
  The philosophical topic or question for this dialogue. If the user
  provided a topic, simply present it clearly. If no topic was provided,
  propose an engaging question like "What is justice?" or "Can virtue
  be taught?" or "What is the good life?"

agent: socratic_questioner
output_file: outputs/01_topic.md
```

### Agent Assignment
**Socratic Philosopher** (socratic_questioner)

### Input Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `topic` | string | No | User-provided topic (empty if AI should choose) |
| `current_year` | string | Yes | Current year for context relevance |

### Behavior Logic

```python
if topic.strip():
    # User provided topic
    output = clarify_and_present_topic(topic)
else:
    # No topic provided, AI generates one
    output = generate_philosophical_topic()
```

### Output Format

**Markdown file**: `outputs/01_topic.md`

**Structure**:
```markdown
# Topic: [Topic Title or Question]

[Brief context or elaboration if needed]
```

**Example Outputs**:

*User-Provided*:
```markdown
# Topic: Should we colonize Mars?

Exploring the ethical and practical considerations of human colonization
of Mars in the 21st century.
```

*AI-Generated*:
```markdown
# Topic: What is the nature of consciousness?

Can consciousness be reduced to physical processes, or does it possess
qualities that transcend the material?
```

### Dependencies
- None (first task in pipeline)

### Success Criteria
- Clear, well-formed philosophical question or topic
- Suitable for Socratic inquiry (not yes/no question)
- Relevant to human experience and accessible to reasoning

---

## Task 2: propose

### Purpose
Explore one perspective on the topic through 5-7 Socratic questions.

### Configuration

```yaml
description: >
  Using the Socratic method, explore one perspective on the proposed
  topic through a series of probing questions. Do NOT make assertions
  or argue a position. Instead, pose questions that would help examine
  the assumptions and implications of one view on the topic. Make sure
  your inquiry is relevant given the current year is {current_year}.

expected_output: >
  A Socratic dialogue consisting of 5-7 carefully crafted questions that:
  - Begin with clarifying the key concepts and definitions
  - Probe the foundations and assumptions of the position
  - Reveal potential contradictions or tensions
  - Lead toward deeper inquiry without asserting conclusions
  - Follow the pattern: definition → assumption → contradiction → insight
  Each question should be numbered and build upon previous questions.

agent: socratic_questioner
output_file: outputs/02_proposition.md
```

### Agent Assignment
**Socratic Philosopher** (socratic_questioner)

### Input Variables

| Variable | Type | Source | Description |
|----------|------|--------|-------------|
| `topic` | string | Initial input | Topic from propose_topic task |
| `current_year` | string | Initial input | Current year for relevance |
| *context* | string | Task 1 | Topic definition from propose_topic |

### Question Pattern

The agent follows a structured progression:

```
1. DEFINITION PHASE (Questions 1-2)
   └── Clarify key concepts and terms

2. ASSUMPTION PHASE (Questions 3-4)
   └── Identify underlying beliefs and foundations

3. CONTRADICTION PHASE (Questions 5-6)
   └── Expose tensions and logical inconsistencies

4. INSIGHT PHASE (Question 7)
   └── Guide toward deeper understanding
```

### Output Format

**Markdown file**: `outputs/02_proposition.md`

**Structure**:
```markdown
# First Line of Inquiry

1. [Definition question about key concept]

2. [Clarification question building on #1]

3. [Assumption-probing question]

4. [Foundation-examining question]

5. [Contradiction-revealing question]

6. [Implication-exploring question]

7. [Deeper insight question]
```

**Example Output**:

```markdown
# First Line of Inquiry

1. When we speak of "colonizing Mars," what exactly do we mean—establishing
   a permanent human presence, or merely temporary scientific outposts?

2. If we seek to make Mars a new home for humanity, must we transform it
   to be Earth-like, or could humans adapt to live in Martian conditions?

3. On what grounds do we claim the right to colonize Mars—is it simply
   because we have the technological capability to do so?

4. Would establishing a human colony on Mars represent progress for our
   species, or might it be an escape from problems we should face on Earth?

5. If we believe humans should spread throughout the cosmos, does this
   imply Earth is insufficient for our needs, or that expansion is part
   of human nature?

6. Could the resources and effort required for Mars colonization be better
   used to address pressing challenges on Earth, or are these endeavors
   complementary rather than competing?

7. What does our desire to colonize other planets reveal about how we view
   our relationship with our home planet?
```

### Dependencies
- Task 1 (propose_topic) must complete successfully
- Topic definition provides context for inquiry angle

### Success Criteria
- 5-7 numbered questions
- Questions build sequentially
- No direct assertions or claims
- Follows definition → assumption → contradiction → insight pattern
- Relevant to current year context
- Genuine philosophical probing (not rhetorical)

### Evaluation Metrics
*(Applied by judge_task)*
- Question Quality (40%)
- Elenctic Effectiveness (25%)
- Philosophical Insight (20%)
- Socratic Fidelity (15%)

---

## Task 3: oppose

### Purpose
Explore an alternative or opposing perspective through 5-7 different Socratic questions.

### Configuration

```yaml
description: >
  Using the Socratic method, explore an alternative or opposing perspective
  on the topic through a different line of questioning. Again, do NOT make
  assertions. Pose questions that would help examine a different set of
  assumptions or reveal different tensions in the topic. Make sure your
  inquiry is relevant given the current year is {current_year}.

expected_output: >
  A Socratic dialogue consisting of 5-7 carefully crafted questions that:
  - Approach the topic from a different angle than the first inquiry
  - Challenge different assumptions or explore alternative implications
  - Reveal tensions or contradictions in the opposing view
  - Guide toward new insights without providing answers
  - Demonstrate genuine philosophical curiosity and intellectual humility
  Each question should be numbered and flow naturally from one to the next.

agent: socratic_questioner
output_file: outputs/03_opposition.md
```

### Agent Assignment
**Socratic Philosopher** (socratic_questioner)

### Input Variables

| Variable | Type | Source | Description |
|----------|------|--------|-------------|
| `topic` | string | Initial input | Topic from propose_topic task |
| `current_year` | string | Initial input | Current year for relevance |
| *context* | string | Tasks 1-2 | Previous topic and first dialogue |

### Differentiation Strategy

The agent must approach the topic differently:

```
First Inquiry Focus → Alternative Inquiry Focus

Individual rights → Collective responsibility
Present concerns → Future implications
Practical benefits → Ethical considerations
Material aspects → Spiritual/philosophical aspects
Human perspective → Environmental/universal perspective
```

### Output Format

**Markdown file**: `outputs/03_opposition.md`

**Structure**:
```markdown
# Alternative Line of Inquiry

1. [Different angle on key concept]

2. [Alternative assumption to examine]

3. [Contrasting perspective question]

4. [Different implication to explore]

5. [Alternative contradiction to reveal]

6. [Counter-consideration question]

7. [Synthesizing insight from different angle]
```

**Example Output**:

```markdown
# Alternative Line of Inquiry

1. Before considering whether we should colonize Mars, must we not ask:
   do we have any obligation to preserve Mars in its current state?

2. If Mars harbors even microbial life, would establishing a human colony
   constitute a form of cosmic imperialism—imposing our presence on another
   world's inhabitants?

3. When we imagine Mars colonization, are we envisioning a democratic
   society, or would the extreme environment necessitate authoritarian
   control for survival?

4. Could the isolation and confinement of a Mars colony lead to new forms
   of human culture and identity that might eventually conflict with Earth?

5. If only the wealthy can afford passage to Mars, would colonization
   create a new form of inequality—a literal upper class in space?

6. What happens to the concept of national sovereignty when humans establish
   presence on another planet—who governs Mars?

7. Does the dream of Mars colonization reveal our capacity for long-term
   thinking and cooperation, or our tendency toward escapism when facing
   difficult challenges?
```

### Dependencies
- Task 1 (propose_topic) must complete
- Task 2 (propose) must complete
- Must offer genuinely different perspective from Task 2

### Success Criteria
- 5-7 numbered questions
- Distinct angle from first inquiry
- No repetition of previous questions
- Challenges different assumptions
- Maintains Socratic method (questions, not assertions)
- Relevant to current year
- Flows naturally between questions

### Evaluation Metrics
*(Applied by judge_task)*
- Question Quality (40%)
- Elenctic Effectiveness (25%)
- Philosophical Insight (20%)
- Socratic Fidelity (15%)

---

## Task 4: judge_task

### Purpose
Evaluate the quality and effectiveness of both Socratic dialogues.

### Configuration

```yaml
description: >
  Evaluate the quality and effectiveness of the Socratic dialogues presented.
  Assess whether the questioning genuinely follows the Socratic method,
  reveals meaningful insights, and advances philosophical understanding.
  Do NOT judge the philosophical positions themselves, but rather the
  quality of the inquiry.

expected_output: >
  A comprehensive evaluation including:
  - Scores for each dialogue on: Question Quality (40%), Elenctic
    Effectiveness (25%), Philosophical Insight (20%), and Socratic
    Fidelity (15%)
  - Total percentage scores for each inquiry
  - Brief assessment of which inquiry better exemplifies the Socratic method
  - One-sentence suggestion for deepening the Socratic examination
  - Notes on whether questions genuinely probe or merely lead to conclusions

agent: judge
output_file: outputs/04_judgment.md
```

### Agent Assignment
**Dialectic Moderator** (judge)

### Input Variables

| Variable | Type | Source | Description |
|----------|------|--------|-------------|
| *context* | string | Tasks 1-3 | All previous outputs for evaluation |

### Evaluation Framework

```
For Each Dialogue:
├── Question Quality (0-5 scale)
│   ├── Clarity of questions
│   ├── Logical progression
│   ├── Depth of inquiry
│   └── Weight: 40% (multiply by 8)
│
├── Elenctic Effectiveness (0-5 scale)
│   ├── Contradiction revelation
│   ├── Assumption challenging
│   ├── Belief testing
│   └── Weight: 25% (multiply by 5)
│
├── Philosophical Insight (0-5 scale)
│   ├── Depth of understanding
│   ├── Advancement toward truth
│   ├── New insights generated
│   └── Weight: 20% (multiply by 4)
│
└── Socratic Fidelity (0-5 scale)
    ├── Adherence to method
    ├── Intellectual humility
    ├── Avoidance of assertions
    └── Weight: 15% (multiply by 3)

Total: Sum of weighted scores (out of 100%)
```

### Output Format

**Markdown file**: `outputs/04_judgment.md`

**Structure**:
```markdown
# Dialectic Evaluation

## First Line of Inquiry
- Question Quality (40%): [score]/5 → [percentage]%
- Elenctic Effectiveness (25%): [score]/5 → [percentage]%
- Philosophical Insight (20%): [score]/5 → [percentage]%
- Socratic Fidelity (15%): [score]/5 → [percentage]%
**Total: [sum]%**

[Brief notes on strengths and weaknesses]

## Alternative Line of Inquiry
- Question Quality (40%): [score]/5 → [percentage]%
- Elenctic Effectiveness (25%): [score]/5 → [percentage]%
- Philosophical Insight (20%): [score]/5 → [percentage]%
- Socratic Fidelity (15%): [score]/5 → [percentage]%
**Total: [sum]%**

[Brief notes on strengths and weaknesses]

## Comparative Assessment
[Which inquiry better exemplifies the Socratic method and why]

## Recommendation for Deeper Inquiry
[One-sentence suggestion for how to deepen the examination]

## Notes on Authenticity
[Whether questions genuinely probe vs. lead to predetermined conclusions]
```

**Example Output**:

```markdown
# Dialectic Evaluation

## First Line of Inquiry
- Question Quality (40%): 4.5/5 → 36%
- Elenctic Effectiveness (25%): 4/5 → 20%
- Philosophical Insight (20%): 4/5 → 16%
- Socratic Fidelity (15%): 5/5 → 15%
**Total: 87%**

Strong logical progression from definition through implication. Questions
maintain proper Socratic humility while effectively probing assumptions
about human expansion and technological capability.

## Alternative Line of Inquiry
- Question Quality (40%): 4/5 → 32%
- Elenctic Effectiveness (25%): 4.5/5 → 23%
- Philosophical Insight (20%): 4/5 → 16%
- Socratic Fidelity (15%): 4/5 → 12%
**Total: 83%**

Excellent at revealing ethical contradictions, particularly regarding
equality and governance. Slightly weaker Socratic fidelity due to
implied positions in questions 5-6.

## Comparative Assessment
The first inquiry demonstrates superior Socratic fidelity with more
neutral questioning, while the alternative inquiry excels at elenchus—
revealing deeper contradictions about power, inequality, and sovereignty.

## Recommendation for Deeper Inquiry
To deepen examination, probe the relationship between individual autonomy
and collective survival when environmental constraints are absolute.

## Notes on Authenticity
Both dialogues maintain largely authentic Socratic questioning, though
the alternative inquiry occasionally implies preferred positions through
question framing (particularly questions about inequality and imperialism).
```

### Dependencies
- Tasks 1-3 must all complete successfully
- Requires both dialogues to evaluate
- Must have access to topic context

### Success Criteria
- Scores provided for all four criteria (both dialogues)
- Weighted percentages calculated correctly
- Comparative assessment present
- Improvement suggestion provided
- Authenticity notes included
- Focus on methodology, not philosophical content

### Evaluation Principles

**Do Evaluate**:
- Quality of question construction
- Effectiveness of Socratic technique
- Depth of philosophical inquiry
- Adherence to Socratic method

**Don't Evaluate**:
- Correctness of philosophical positions
- Agreement with particular viewpoints
- Personal philosophical preferences
- "Right" answers to questions posed

---

## Task Dependencies & Data Flow

### Dependency Graph

```
propose_topic (no dependencies)
    ↓
    ├─→ propose (depends on: propose_topic)
    │       ↓
    │       └─→ oppose (depends on: propose_topic, propose)
    │               ↓
    └───────────────→ judge_task (depends on: all previous)
```

### Context Propagation

**CrewAI Context System**:
- Each task automatically receives output from previous tasks
- Context includes both task descriptions and generated outputs
- Agents maintain awareness of conversation flow

**Information Available at Each Task**:

| Task | Available Information |
|------|----------------------|
| propose_topic | Initial inputs only (topic, current_year) |
| propose | Topic + topic definition |
| oppose | Topic + topic definition + first dialogue |
| judge_task | Topic + both dialogues + all context |

### File System Output

```
outputs/
├── 01_topic.md        (Created by: propose_topic)
├── 02_proposition.md  (Created by: propose)
├── 03_opposition.md   (Created by: oppose)
└── 04_judgment.md     (Created by: judge_task)
```

**Output Files**:
- Persistent across sessions
- Overwritten on each new dialogue
- Human-readable markdown format
- No database or structured storage

---

## Error Handling & Recovery

### Task Failure Scenarios

**Scenario 1: Task Execution Failure**
```
If any task fails → entire pipeline stops
No partial outputs displayed
Error message shown to user
Previous output files may be stale
```

**Scenario 2: Agent Timeout**
```
CrewAI default: 25 iterations per agent
If exceeded → task fails
Retry: Not automatic, requires new kickoff
```

**Scenario 3: Invalid Output**
```
If agent produces non-markdown output → file still created
Gradio renders whatever is present
Quality may be degraded
judge_task may note quality issues
```

### Recovery Mechanisms

**Current Implementation**:
- No automatic retry logic
- User must restart dialogue
- Previous outputs overwritten (not preserved)

**Error Display**:
```python
try:
    result = crew.kickoff(inputs=inputs)
    # Read output files
except Exception as e:
    error_msg = f"Error running dialogue: {str(e)}"
    return error_msg, error_msg, error_msg, error_msg
```

### Timeout Configuration

**CrewAI Defaults**:
- Max iterations per agent: 25
- No explicit time limit
- Typical duration: 120-180 seconds
- Can vary based on topic complexity

---

## Performance Optimization

### Current Bottlenecks

1. **Sequential Execution**: Cannot parallelize tasks
2. **API Latency**: Each task requires Claude API calls
3. **File I/O**: Writing and reading markdown files
4. **Context Size**: Large context passed between tasks

### Optimization Strategies

**Already Implemented**:
- Verbose mode for debugging (can be disabled)
- Direct file output (no database overhead)
- Clear task boundaries (minimal re-processing)

**Potential Improvements**:
- Cache common topic evaluations
- Parallel execution of independent components
- Streaming output as tasks complete
- Reduce context size through summarization

---

## Future Task Enhancements

### Proposed Additional Tasks

1. **follow_up Task**: Allow user to ask clarifying questions
2. **synthesis Task**: Combine insights from both inquiries
3. **historical_context Task**: Compare with historical philosophers
4. **practical_application Task**: Apply philosophical insights to real scenarios

### Task Modification Ideas

1. **Configurable Depth**: Allow 3-5 or 7-10 question options
2. **Difficulty Levels**: Adjust complexity based on user preference
3. **Domain Specialization**: Philosophy subfield focus (ethics, epistemology, etc.)
4. **Multi-Agent Debate**: More than two perspectives per topic
5. **Iterative Refinement**: Allow re-running with feedback

### Quality Improvements

1. **Automated Quality Checks**: Validate output format before moving to next task
2. **Rollback Capability**: Restart from specific task if quality is poor
3. **User Intervention Points**: Allow user to guide inquiry direction
4. **Adaptive Questioning**: Adjust based on judge_task feedback
