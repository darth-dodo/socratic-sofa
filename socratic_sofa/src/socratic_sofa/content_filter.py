"""
Content moderation for Socratic Sofa
Uses AI to evaluate if topics are appropriate for philosophical dialogue
"""

import os
from anthropic import Anthropic


def is_topic_appropriate(topic: str) -> tuple[bool, str]:
    """
    Check if a topic is appropriate for philosophical dialogue using AI moderation.

    Args:
        topic: The topic string to check

    Returns:
        Tuple of (is_appropriate: bool, reason: str)
        - If appropriate: (True, "")
        - If inappropriate: (False, "reason for rejection")
    """
    if not topic or not topic.strip():
        return True, ""

    # Check length first (quick check before API call)
    if len(topic) > 500:
        return False, "Topic is too long. Please keep it concise (under 500 characters)."

    # Use Claude to moderate the content
    try:
        client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

        moderation_prompt = f"""You are a content moderator for a philosophical dialogue platform. Evaluate if this topic is appropriate for respectful philosophical discussion.

Topic: "{topic}"

Criteria for rejection:
- Explicitly sexual or pornographic content
- Graphic violence or gore
- Hate speech or discrimination
- Illegal activities (except as legitimate policy questions like "should X be legal?")
- Trolling or bad faith topics

Criteria for acceptance:
- Legitimate philosophical questions about ethics, even if controversial
- Policy questions about legalization/regulation
- Questions about morality, even if touching on difficult subjects
- Sincere inquiry into human nature and society

Respond with ONLY:
- "APPROPRIATE" if the topic is suitable for philosophical dialogue
- "INAPPROPRIATE: [brief reason]" if it should be rejected

Response:"""

        response = client.messages.create(
            model="claude-haiku-4-20250605",  # Fast and cheap for moderation
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
            # If unclear response, err on the side of caution but be permissive
            return True, ""

    except Exception as e:
        # If moderation fails, log the error but allow the topic (fail open for better UX)
        print(f"⚠️ Content moderation error: {e}")
        return True, ""


def get_alternative_suggestions() -> list[str]:
    """
    Provide alternative philosophical topics when a topic is rejected.

    Returns:
        List of suggested alternative topics
    """
    return [
        "What is justice?",
        "What is the good life?",
        "Is morality relative or universal?",
        "What is consciousness?",
        "Do we have free will?",
        "Can AI have rights?",
        "What is truth?",
        "Is beauty objective?",
    ]
