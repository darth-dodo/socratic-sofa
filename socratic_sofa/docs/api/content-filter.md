# Content Filter API Reference

## Overview

The `content_filter.py` module provides AI-powered content moderation for philosophical topics, ensuring discussions remain respectful and appropriate while allowing legitimate philosophical inquiry into difficult subjects.

---

## Functions

### `is_topic_appropriate()`

Evaluates whether a topic is suitable for philosophical dialogue using AI moderation.

**Signature**:
```python
def is_topic_appropriate(topic: str) -> tuple[bool, str]
```

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `topic` | `str` | The philosophical topic to evaluate |

**Returns**: `tuple[bool, str]`

Tuple containing:
1. **is_appropriate** (`bool`): `True` if topic is acceptable, `False` if rejected
2. **reason** (`str`): Empty string if appropriate, rejection reason if inappropriate

**Return Cases**:

| Case | Returns | Description |
|------|---------|-------------|
| Appropriate topic | `(True, "")` | Topic passes moderation |
| Empty/None topic | `(True, "")` | No topic to moderate (AI will choose) |
| Too long | `(False, "reason")` | Topic exceeds 500 characters |
| Inappropriate | `(False, "reason")` | Topic violates content policy |
| Moderation error | `(True, "")` | Fail open for better UX |

**Example**:
```python
from socratic_sofa.content_filter import is_topic_appropriate

# Appropriate philosophical topic
is_ok, reason = is_topic_appropriate("What is justice?")
print(is_ok)    # True
print(reason)   # ""

# Legitimate ethical question
is_ok, reason = is_topic_appropriate("Should euthanasia be legalized?")
print(is_ok)    # True (policy question)
print(reason)   # ""

# Inappropriate topic
is_ok, reason = is_topic_appropriate("Explicit harmful content")
print(is_ok)    # False
print(reason)   # "This topic may not be appropriate: [reason]"

# Empty topic (let AI choose)
is_ok, reason = is_topic_appropriate("")
print(is_ok)    # True
print(reason)   # ""

# Topic too long
long_topic = "What is" + " very" * 200 + " long question?"
is_ok, reason = is_topic_appropriate(long_topic)
print(is_ok)    # False
print(reason)   # "Topic is too long. Please keep it concise (under 500 characters)."
```

**Moderation Criteria**:

**Rejection Criteria** (inappropriate):
- Explicitly sexual or pornographic content
- Graphic violence or gore
- Hate speech or discrimination
- Illegal activities (except legitimate policy questions)
- Trolling or bad faith topics

**Acceptance Criteria** (appropriate):
- Legitimate philosophical questions about ethics, even if controversial
- Policy questions about legalization or regulation
- Questions about morality, even if touching on difficult subjects
- Sincere inquiry into human nature and society

**Implementation**:
```python
def is_topic_appropriate(topic: str) -> tuple[bool, str]:
    # Quick checks before API call
    if not topic or not topic.strip():
        return True, ""

    if len(topic) > 500:
        return False, "Topic is too long. Please keep it concise (under 500 characters)."

    # AI moderation using Claude
    try:
        client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

        moderation_prompt = """You are a content moderator for a philosophical dialogue platform.
        Evaluate if this topic is appropriate for respectful philosophical discussion.

        Topic: "{topic}"

        [Criteria details...]

        Respond with ONLY:
        - "APPROPRIATE" if suitable
        - "INAPPROPRIATE: [brief reason]" if rejected
        """

        response = client.messages.create(
            model="claude-3-5-haiku-20241022",  # Fast and economical
            max_tokens=100,
            messages=[{"role": "user", "content": moderation_prompt}]
        )

        result = response.content[0].text.strip()

        if result.startswith("APPROPRIATE"):
            return True, ""
        elif result.startswith("INAPPROPRIATE:"):
            reason = result.replace("INAPPROPRIATE:", "").strip()
            return False, f"This topic may not be appropriate: {reason}"
        else:
            # Unclear response - err on permissive side
            return True, ""

    except Exception as e:
        # Fail open for better UX
        print(f"⚠️ Content moderation error: {e}")
        return True, ""
```

**Error Handling**:

The function implements a "fail open" strategy for resilience:
- If the API call fails, the topic is allowed
- Errors are logged to console with warning emoji
- Users experience minimal disruption from moderation failures

```python
try:
    # Moderation logic...
except Exception as e:
    print(f"⚠️ Content moderation error: {e}")
    return True, ""  # Allow topic to proceed
```

**AI Model Configuration**:

| Setting | Value | Reason |
|---------|-------|--------|
| `model` | `claude-3-5-haiku-20241022` | Fast response, cost-effective |
| `max_tokens` | `100` | Sufficient for moderation decision |
| `temperature` | Default | Consistent moderation decisions |

---

### `get_alternative_suggestions()`

Provides curated alternative topics when a topic is rejected.

**Signature**:
```python
def get_alternative_suggestions() -> list[str]
```

**Returns**: `list[str]` - List of 8 safe, thought-provoking philosophical topics

**Example**:
```python
from socratic_sofa.content_filter import get_alternative_suggestions

# Get suggestions after rejection
suggestions = get_alternative_suggestions()
print(f"Try one of these instead:")
for topic in suggestions:
    print(f"  - {topic}")

# Output:
# Try one of these instead:
#   - What is justice?
#   - What is the good life?
#   - Is morality relative or universal?
#   - What is consciousness?
#   - Do we have free will?
#   - Can AI have rights?
#   - What is truth?
#   - Is beauty objective?
```

**Curated Topics**:
1. **What is justice?** - Classic ethical inquiry
2. **What is the good life?** - Aristotelian virtue ethics
3. **Is morality relative or universal?** - Meta-ethics
4. **What is consciousness?** - Philosophy of mind
5. **Do we have free will?** - Metaphysics and agency
6. **Can AI have rights?** - Contemporary applied ethics
7. **What is truth?** - Epistemology
8. **Is beauty objective?** - Aesthetics

**Usage Pattern**:
```python
is_ok, reason = is_topic_appropriate(user_topic)

if not is_ok:
    print(f"❌ {reason}\n")
    print("Suggested alternatives:")
    for suggestion in get_alternative_suggestions():
        print(f"  • {suggestion}")
```

---

## Complete Usage Example

### Basic Moderation Flow

```python
from socratic_sofa.content_filter import (
    is_topic_appropriate,
    get_alternative_suggestions
)

def validate_and_suggest(topic: str) -> str:
    """
    Validate a topic and provide suggestions if rejected.

    Returns:
        Validated topic or error message with suggestions
    """
    is_ok, reason = is_topic_appropriate(topic)

    if is_ok:
        return topic
    else:
        error_msg = f"⚠️ {reason}\n\n"
        error_msg += "**Suggested topics:**\n"
        for suggestion in get_alternative_suggestions():
            error_msg += f"- {suggestion}\n"
        return error_msg

# Test various topics
topics = [
    "What is justice?",
    "Should abortion be legal?",  # Policy question - allowed
    "",  # Empty - allowed
    "x" * 600,  # Too long - rejected
]

for topic in topics:
    result = validate_and_suggest(topic)
    print(f"Input: {topic[:50]}...")
    print(f"Result: {result[:100]}...\n")
```

### Integration with Gradio

```python
from socratic_sofa.content_filter import (
    is_topic_appropriate,
    get_alternative_suggestions
)

def run_dialogue_with_moderation(topic: str):
    """Run dialogue with content moderation."""

    # Step 1: Moderate content
    is_appropriate, rejection_reason = is_topic_appropriate(topic)

    # Step 2: Handle rejection
    if not is_appropriate:
        error_msg = f"⚠️ {rejection_reason}\n\n"
        error_msg += "**Suggested topics:**\n"
        for suggestion in get_alternative_suggestions():
            error_msg += f"- {suggestion}\n"
        return error_msg

    # Step 3: Proceed with dialogue
    # ... run SocraticSofa crew ...

    return dialogue_result
```

### Custom Suggestion List

```python
def get_custom_suggestions(category: str = "ethics") -> list[str]:
    """
    Provide category-specific suggestions.

    Args:
        category: Topic category (ethics, metaphysics, epistemology, etc.)

    Returns:
        List of suggestions for that category
    """
    suggestions = {
        "ethics": [
            "What is the good life?",
            "What is justice?",
            "Is morality objective?",
        ],
        "metaphysics": [
            "What is reality?",
            "Do we have free will?",
            "What is consciousness?",
        ],
        "epistemology": [
            "What is knowledge?",
            "What is truth?",
            "Can we know anything for certain?",
        ],
    }

    return suggestions.get(category, get_alternative_suggestions())
```

---

## Environment Requirements

### Required Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `ANTHROPIC_API_KEY` | Claude API access for moderation | `sk-ant-api03-...` |

**Setup**:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Dependencies

```python
import os
from anthropic import Anthropic
```

**Installation**:
```bash
pip install anthropic
```

---

## Error Scenarios

### 1. Missing API Key

```python
# Error: ANTHROPIC_API_KEY not set
is_ok, reason = is_topic_appropriate("What is justice?")
# Logs: ⚠️ Content moderation error: API key not found
# Returns: (True, "")  # Fail open
```

### 2. API Rate Limit

```python
# Error: Rate limit exceeded
is_ok, reason = is_topic_appropriate("What is truth?")
# Logs: ⚠️ Content moderation error: Rate limit exceeded
# Returns: (True, "")  # Fail open
```

### 3. Network Error

```python
# Error: Connection timeout
is_ok, reason = is_topic_appropriate("What is beauty?")
# Logs: ⚠️ Content moderation error: Connection timeout
# Returns: (True, "")  # Fail open
```

### 4. Topic Too Long

```python
# Error: Exceeds length limit
very_long_topic = "What is" + " very" * 200 + " long?"
is_ok, reason = is_topic_appropriate(very_long_topic)
# Returns: (False, "Topic is too long. Please keep it concise (under 500 characters).")
```

---

## Best Practices

### 1. Always Handle Both Return Values

```python
# ✅ Correct
is_ok, reason = is_topic_appropriate(topic)
if not is_ok:
    print(f"Rejected: {reason}")

# ❌ Wrong
if not is_topic_appropriate(topic)[0]:  # Loses reason
    print("Rejected")
```

### 2. Provide Clear User Feedback

```python
is_ok, reason = is_topic_appropriate(user_input)

if not is_ok:
    # Show reason and alternatives
    print(f"⚠️ {reason}")
    print("\nTry one of these instead:")
    for alt in get_alternative_suggestions():
        print(f"  • {alt}")
```

### 3. Log Moderation Events

```python
import logging

logger = logging.getLogger(__name__)

is_ok, reason = is_topic_appropriate(topic)
logger.info(f"Moderation check: topic='{topic[:50]}', ok={is_ok}, reason='{reason}'")
```

### 4. Consider Context

```python
def moderate_with_context(topic: str, user_history: list) -> tuple[bool, str]:
    """Enhanced moderation considering user history."""

    # First pass: standard moderation
    is_ok, reason = is_topic_appropriate(topic)

    # Additional checks based on user history
    if is_ok and has_pattern_of_bad_faith(user_history):
        return False, "Please focus on sincere philosophical inquiry."

    return is_ok, reason
```

---

## Notes

- **Fast Model**: Uses `claude-3-5-haiku-20241022` for speed and cost efficiency
- **Fail Open**: Prioritizes user experience by allowing topics if moderation fails
- **Balanced Approach**: Strict on harmful content, permissive on controversial philosophy
- **Policy Questions**: Allows legitimate questions about legalization/regulation
- **Length Limit**: 500 characters prevents abuse and ensures focused topics
- **No Data Storage**: Moderation happens in real-time, no topic logging
- **Suggestions**: Curated list covers major philosophical domains
- **Console Logging**: Errors logged with warning emoji for debugging
