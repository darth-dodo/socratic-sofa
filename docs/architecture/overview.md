# System Architecture Overview

## Introduction

Socratic Sofa is an AI-powered philosophical dialogue system that implements the Socratic method through multi-agent collaboration. Built on CrewAI and powered by Claude AI, the system generates authentic philosophical inquiry through systematic questioning rather than direct assertions.

## High-Level Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│                     (Gradio Web Interface)                      │
│  - Topic Selection (Library + Custom Input)                     │
│  - Content Moderation Check                                     │
│  - Real-time Dialogue Display                                   │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Content Filter                             │
│                   (AI-Powered Moderation)                       │
│  - Claude 3.5 Haiku for Fast Moderation                        │
│  - Topic Appropriateness Evaluation                            │
│  - Alternative Suggestions                                      │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│                       CrewAI Orchestration                      │
│                      (SocraticSofa Crew)                        │
│  - Sequential Process Execution                                 │
│  - Agent Coordination                                           │
│  - Task Dependency Management                                   │
└────────────────────┬────────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ↓                         ↓
┌──────────────────┐      ┌──────────────────┐
│  Agent Layer     │      │   Agent Layer    │
│                  │      │                  │
│  Socratic        │      │  Dialectic       │
│  Philosopher     │      │  Moderator       │
│                  │      │                  │
│  - Questioning   │      │  - Evaluation    │
│  - Elenchus      │      │  - Scoring       │
│  - Inquiry       │      │  - Feedback      │
└────────┬─────────┘      └────────┬─────────┘
         │                         │
         ↓                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                         Task Pipeline                           │
│  1. propose_topic    → Select/Generate Topic                    │
│  2. propose          → First Line of Inquiry (5-7 questions)    │
│  3. oppose           → Alternative Inquiry (5-7 questions)      │
│  4. judge_task       → Evaluate Both Dialogues                  │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│                       Output Storage                            │
│  - 01_topic.md       (Topic Definition)                         │
│  - 02_proposition.md (First Dialogue)                           │
│  - 03_opposition.md  (Alternative Dialogue)                     │
│  - 04_judgment.md    (Evaluation & Scores)                      │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Request Flow

1. **Topic Input Phase**
   ```
   User → Dropdown Selection OR Custom Input
        → Topic Selection Handler
        → Final Topic Determination
   ```

2. **Content Moderation Phase**
   ```
   Final Topic → is_topic_appropriate()
               → Claude 3.5 Haiku API Call
               → Evaluation (APPROPRIATE/INAPPROPRIATE)
               → Pass Through OR Reject with Suggestions
   ```

3. **Dialogue Generation Phase**
   ```
   Approved Topic → SocraticSofa Crew Kickoff
                  → Sequential Task Execution:
                     1. propose_topic task
                     2. propose task (First Inquiry)
                     3. oppose task (Alternative Inquiry)
                     4. judge_task (Evaluation)
                  → Markdown Output Files
   ```

4. **Display Phase**
   ```
   Output Files → Read from outputs/ directory
                → Format with Section Headers
                → Render in Gradio Interface
   ```

### Task Dependencies

```
propose_topic (Agent: Socratic Philosopher)
      │
      ↓
propose (Agent: Socratic Philosopher)
      │ [Context: Topic from propose_topic]
      ↓
oppose (Agent: Socratic Philosopher)
      │ [Context: Topic + First Inquiry]
      ↓
judge_task (Agent: Dialectic Moderator)
      │ [Context: Both Inquiries]
      ↓
Final Evaluation & Scores
```

## Component Interactions

### CrewAI Framework

**Process Type**: Sequential
- Tasks execute in strict order
- Each task receives context from previous tasks
- Output from one task becomes input for the next

**Agent Assignment**:
- `propose_topic` → Socratic Philosopher
- `propose` → Socratic Philosopher
- `oppose` → Socratic Philosopher
- `judge_task` → Dialectic Moderator

**Verbose Mode**: Enabled for debugging and transparency

### Web Interface (Gradio)

**Interface Structure**:
- Single-column layout optimized for mobile
- Responsive CSS with mobile breakpoints
- Touch-friendly button sizing (min 48px height)
- Progressive disclosure of information

**User Interaction Flow**:
1. Topic selection via dropdown or text input
2. Content moderation feedback (if rejected)
3. Progress indication during execution (2-3 minutes)
4. Staged output display (Topic → Inquiries → Evaluation)

**Theme Configuration**:
- Primary: Indigo
- Secondary: Purple
- Soft theme for philosophical aesthetic

## Technology Stack

### Core Framework
- **CrewAI**: Multi-agent orchestration framework
- **Python 3.11+**: Runtime environment
- **Anthropic Claude**: AI model for agents and moderation

### AI Models
- **Claude Opus/Sonnet**: Main dialogue generation (via CrewAI)
- **Claude 3.5 Haiku**: Fast content moderation (direct API)

### Web Framework
- **Gradio**: Web interface and UI components
- **YAML**: Configuration management (agents, tasks, topics)

### File System
- **Markdown**: Output format for all generated content
- **outputs/**: Directory for sequential task outputs

## Architectural Decisions

### Why Sequential Process?

The Socratic method inherently requires sequential reasoning where each question builds upon previous ones. Sequential processing ensures:
- Logical progression of inquiry
- Context preservation across dialogues
- Proper setup for evaluation phase
- Natural flow matching human philosophical dialogue

### Why Two Separate Claude Instances?

**Content Moderation** (Claude 3.5 Haiku):
- Fast response time (<1 second)
- Cost-effective for simple binary decisions
- Independent from philosophical reasoning
- Fail-open design for better UX

**Dialogue Generation** (Claude Opus/Sonnet via CrewAI):
- Deep reasoning capabilities
- Better at maintaining philosophical rigor
- Handles complex multi-turn context
- Optimized for quality over speed

### Why Markdown Output Files?

- **Portability**: Easy to share and archive dialogues
- **Readability**: Human-readable format
- **Versioning**: Git-friendly for dialogue tracking
- **Rendering**: Direct support in Gradio interface
- **Export**: Simple conversion to other formats

### Why Gradio?

- **Rapid Development**: Quick prototype to production
- **Mobile-First**: Responsive out of the box
- **Real-time Updates**: Stream-friendly interface
- **Python Integration**: Seamless with CrewAI
- **Deployment**: Easy Hugging Face Spaces integration

## Scalability Considerations

### Current Limitations

1. **Synchronous Execution**: Each dialogue blocks until complete (2-3 minutes)
2. **File-Based Output**: Not suitable for high-concurrency scenarios
3. **No Persistence**: No database for dialogue history
4. **Single Instance**: No load balancing or redundancy

### Potential Improvements

1. **Async Processing**: Queue-based system with job status tracking
2. **Database Storage**: PostgreSQL for dialogue persistence
3. **Caching Layer**: Redis for topic library and common queries
4. **Horizontal Scaling**: Multiple worker instances with load balancer

## Security & Safety

### Content Moderation

**AI-Based Filtering**:
- Reject explicit sexual/violent content
- Block hate speech and discrimination
- Filter illegal activity promotion
- Allow legitimate philosophical inquiry

**Fail-Open Design**:
- Moderation failures allow topic through
- Better UX than blocking all requests
- Logged for monitoring and improvement

### API Key Management

**Environment Variables**:
- `ANTHROPIC_API_KEY`: Required for both moderation and dialogue
- Not stored in code or configuration files
- Validated at startup

### Input Validation

**Topic Length**: Maximum 500 characters
**Injection Prevention**: Prompt engineering in moderation system
**Output Sanitization**: Markdown rendering with XSS protection

## Performance Characteristics

### Expected Latency

- **Content Moderation**: <1 second
- **Topic Selection**: <2 seconds (AI-generated topics)
- **Dialogue Generation**: 120-180 seconds (full pipeline)
- **UI Response**: <100ms (file reading and rendering)

### Resource Usage

- **Memory**: ~500MB per active dialogue
- **CPU**: Moderate during generation, minimal during waiting
- **Network**: API calls to Anthropic (rate limit aware)
- **Storage**: ~10KB per dialogue (markdown files)

## Monitoring & Observability

### Current Logging

- CrewAI verbose mode: Agent actions and task execution
- Gradio console: Request handling and errors
- Content filter: Moderation decisions and failures

### Recommended Additions

1. **Structured Logging**: JSON format with correlation IDs
2. **Metrics Collection**: Dialogue completion rate, moderation accuracy
3. **Error Tracking**: Sentry or similar for production issues
4. **Performance Monitoring**: Response times, API latency

## Deployment Architecture

### Local Development

```
python -m socratic_sofa.gradio_app
  → Starts Gradio on 0.0.0.0:7860
  → Reads configurations from config/
  → Outputs to outputs/ directory
```

### Production Deployment

**Container-Based**:
```
Docker → Gunicorn → Gradio App
       → Health checks
       → Auto-restart on failure
       → Log aggregation
```

**Environment Requirements**:
- Python 3.11+ runtime
- ANTHROPIC_API_KEY environment variable
- 1GB+ RAM recommended
- Persistent storage for outputs/

## Future Architecture Enhancements

### Multi-User Support

- Session-based output directories
- User authentication and history
- Concurrent dialogue handling
- Rate limiting per user

### Advanced Features

- **Dialogue Branching**: Follow-up questions on specific points
- **Multi-Agent Debates**: More than two perspectives
- **Historical Analysis**: Compare with famous philosophical texts
- **Collaborative Mode**: Multiple users contributing to inquiry

### Integration Points

- **API Layer**: RESTful API for programmatic access
- **Webhook Support**: Notify external systems on completion
- **Export Options**: PDF, HTML, plain text formats
- **Sharing**: Social media integration for dialogues
