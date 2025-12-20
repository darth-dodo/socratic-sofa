# System Architecture Overview

## Introduction

Socratic Sofa is an AI-powered philosophical dialogue system that implements the Socratic method through multi-agent collaboration. Built on CrewAI and powered by Claude AI, the system generates authentic philosophical inquiry through systematic questioning rather than direct assertions.

## High-Level Architecture

```mermaid
flowchart TB
    subgraph UI["User Interface (Gradio)"]
        Topic["Topic Selection"]
        Display["Dialogue Display"]
    end

    subgraph Filter["Content Filter"]
        Mod["AI Moderation"]
        Rate["Rate Limiter"]
    end

    subgraph Crew["CrewAI Orchestration"]
        SP["Socratic Philosopher"]
        DM["Dialectic Moderator"]
    end

    subgraph Tasks["Task Pipeline"]
        T1["1. propose_topic"]
        T2["2. propose"]
        T3["3. oppose"]
        T4["4. judge_task"]
    end

    Topic --> Rate --> Mod
    Mod -->|Approved| Crew
    Mod -->|Rejected| Topic

    SP --> T1 --> T2 --> T3
    DM --> T4

    Tasks --> Display
```

## Data Flow

### Request Flow Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant G as Gradio UI
    participant F as Content Filter
    participant R as Rate Limiter
    participant C as CrewAI
    participant A as Claude API

    U->>G: Select/Enter Topic
    G->>R: Check Rate Limit
    R->>F: is_topic_appropriate()
    F->>A: Claude 3.5 Haiku
    A-->>F: APPROPRIATE/INAPPROPRIATE

    alt Topic Rejected
        F-->>G: Show Suggestions
        G-->>U: Alternative Topics
    else Topic Approved
        F-->>C: Start Crew
        C->>A: propose_topic
        A-->>C: Topic Result
        C->>A: propose (First Inquiry)
        A-->>C: Inquiry Result
        C->>A: oppose (Alternative)
        A-->>C: Alternative Result
        C->>A: judge_task
        A-->>C: Evaluation
        C-->>G: Stream Results
        G-->>U: Display Dialogue
    end
```

### Task Dependencies

```mermaid
flowchart TD
    subgraph Agent1["Socratic Philosopher"]
        PT["propose_topic"]
        P["propose"]
        O["oppose"]
    end

    subgraph Agent2["Dialectic Moderator"]
        J["judge_task"]
    end

    PT -->|"Topic Context"| P
    PT -->|"Topic Context"| O
    P -->|"First Inquiry Context"| O
    P -->|"First Inquiry"| J
    O -->|"Alternative Inquiry"| J

    J --> Result["Final Evaluation & Scores"]
```

## Component Interactions

### CrewAI Framework

**Process Type**: Sequential

- Tasks execute in strict order
- Each task receives context from previous tasks
- Output from one task becomes input for the next

**Agent Assignment**:

| Task            | Agent                | Purpose                 |
| --------------- | -------------------- | ----------------------- |
| `propose_topic` | Socratic Philosopher | Select/Generate Topic   |
| `propose`       | Socratic Philosopher | First Line of Inquiry   |
| `oppose`        | Socratic Philosopher | Alternative Inquiry     |
| `judge_task`    | Dialectic Moderator  | Evaluate Both Dialogues |

### Module Dependencies

```mermaid
flowchart LR
    subgraph Core["Core Modules"]
        CF[content_filter.py]
        CR[crew.py]
        GA[gradio_app.py]
        MA[main.py]
    end

    subgraph Support["Support Modules"]
        LC[logging_config.py]
        RL[rate_limiter.py]
    end

    subgraph External["External"]
        AN[Anthropic API]
        CW[CrewAI]
        GR[Gradio]
    end

    LC --> CF
    LC --> CR
    LC --> GA
    RL --> CF

    CF --> GA
    CR --> GA
    CR --> MA

    AN --> CF
    AN --> CW
    CW --> CR
    GR --> GA
```

## Technology Stack

### Core Components

```mermaid
flowchart TB
    subgraph Runtime["Runtime Environment"]
        PY["Python 3.11+"]
        UV["UV Package Manager"]
    end

    subgraph AI["AI Layer"]
        Claude["Claude Sonnet 4.5"]
        Haiku["Claude 3.5 Haiku"]
        CrewAI["CrewAI Framework"]
    end

    subgraph Web["Web Layer"]
        Gradio["Gradio Interface"]
        YAML["YAML Config"]
    end

    subgraph Quality["Quality Tools"]
        Pytest["pytest + 220 tests"]
        PreCommit["pre-commit hooks"]
        Ruff["ruff linter"]
    end

    subgraph Infra["Infrastructure"]
        Logging["Structured Logging"]
        RateLimit["Rate Limiting"]
    end

    PY --> AI
    PY --> Web
    UV --> PY
    CrewAI --> Claude
    Gradio --> CrewAI
```

### AI Models

| Model             | Purpose             | Characteristics                    |
| ----------------- | ------------------- | ---------------------------------- |
| Claude Sonnet 4.5 | Dialogue generation | Deep reasoning, multi-turn context |
| Claude 3.5 Haiku  | Content moderation  | Fast (<1s), cost-effective         |

### Quality Assurance

| Tool       | Purpose                  |
| ---------- | ------------------------ |
| pytest     | 220+ tests, 99% coverage |
| pre-commit | Automated quality checks |
| ruff       | Linting and formatting   |
| bandit     | Security scanning        |
| vulture    | Dead code detection      |

## Architectural Decisions

### Why Sequential Process?

The Socratic method inherently requires sequential reasoning where each question builds upon previous ones. Sequential processing ensures:

- Logical progression of inquiry
- Context preservation across dialogues
- Proper setup for evaluation phase
- Natural flow matching human philosophical dialogue
- Differentiation between first and second inquiries through context awareness

### Why Two Separate Claude Instances?

```mermaid
flowchart LR
    subgraph Moderation["Content Moderation"]
        H["Claude 3.5 Haiku"]
        F["Fast: <1 second"]
        C["Cost-effective"]
    end

    subgraph Dialogue["Dialogue Generation"]
        S["Claude Sonnet 4.5"]
        D["Deep reasoning"]
        Q["Quality-focused"]
    end

    H --> F --> C
    S --> D --> Q
```

### Why Gradio?

- **Rapid Development**: Quick prototype to production
- **Mobile-First**: Responsive out of the box
- **Real-time Updates**: Stream-friendly interface
- **Python Integration**: Seamless with CrewAI
- **Deployment**: Easy Hugging Face Spaces integration

## Performance Characteristics

### Latency Profile

```mermaid
gantt
    title Dialogue Generation Timeline
    dateFormat s
    axisFormat %S

    section Moderation
    Rate Check           :a1, 0, 0.1s
    Content Filter       :a2, after a1, 1s

    section Dialogue
    propose_topic        :b1, after a2, 30s
    propose (5-7 questions) :b2, after b1, 45s
    oppose (5-7 questions)  :b3, after b2, 45s
    judge_task           :b4, after b3, 30s
```

### Resource Usage

| Resource | Expected Usage             |
| -------- | -------------------------- |
| Memory   | ~500MB per dialogue        |
| CPU      | Moderate during generation |
| Network  | Rate-limited API calls     |

## Monitoring & Observability

### Logging Architecture

```mermaid
flowchart TB
    subgraph Sources["Log Sources"]
        App["Application Code"]
        Filter["Content Filter"]
        Crew["CrewAI Agents"]
    end

    subgraph Logger["Logging Framework"]
        LC["logging_config.py"]
        JSON["JSON Formatter"]
        Console["Console Formatter"]
    end

    subgraph Output["Output Destinations"]
        Dev["Development: Console"]
        Prod["Production: JSON"]
    end

    Sources --> LC
    LC --> JSON --> Prod
    LC --> Console --> Dev
```

### Logging Features

- **Context Propagation**: Session IDs, topic context, request metadata
- **Performance Tracking**: Automatic timing for functions and operations
- **Error Details**: Structured exception logging with traceback
- **Log Levels**: DEBUG, INFO, WARNING, ERROR with configurable thresholds

## Deployment Architecture

### Local Development

```bash
python -m socratic_sofa.gradio_app
  → Starts Gradio on 0.0.0.0:7860
  → Reads configurations from config/
```

### Production Deployment

```mermaid
flowchart LR
    subgraph Container["Docker Container"]
        G["Gunicorn"]
        App["Gradio App"]
    end

    subgraph Services["External Services"]
        API["Anthropic API"]
        HF["Hugging Face Spaces"]
    end

    G --> App --> API
    HF --> Container
```

**Environment Requirements**:

- Python 3.11+ runtime
- ANTHROPIC_API_KEY environment variable
- 1GB+ RAM recommended

## Security & Safety

### Content Moderation Flow

```mermaid
flowchart TD
    Input["User Topic Input"]
    Length{"Length > 500?"}
    AI["Claude 3.5 Haiku Check"]
    Decision{"Appropriate?"}
    Pass["Allow Topic"]
    Reject["Reject + Suggestions"]
    Fallback["Fail Open (on error)"]

    Input --> Length
    Length -->|Yes| Reject
    Length -->|No| AI
    AI --> Decision
    Decision -->|Yes| Pass
    Decision -->|No| Reject
    AI -->|Error| Fallback
```

### Security Measures

| Layer      | Protection                    |
| ---------- | ----------------------------- |
| Input      | 500 char limit, rate limiting |
| Moderation | AI-powered content filtering  |
| API Keys   | Environment variables only    |
| Output     | Markdown with XSS protection  |

## Future Enhancements

### Planned Features

- **Multi-User Support**: Session-based dialogues, user authentication
- **Dialogue Branching**: Follow-up questions on specific points
- **API Layer**: RESTful API for programmatic access
- **Export Options**: PDF, HTML, plain text formats
