"""
Content moderation for Socratic Sofa
Uses AI to evaluate if topics are appropriate for philosophical dialogue
"""

import os

from anthropic import Anthropic

from socratic_sofa.logging_config import get_logger, log_timing

# Module logger
logger = get_logger(__name__)


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
        logger.info("Topic rejected - too long", extra={"topic_length": len(topic)})
        return False, "Topic is too long. Please keep it concise (under 500 characters)."

    # Use Claude to moderate the content
    try:
        logger.debug("Starting content moderation", extra={"topic_length": len(topic)})
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
            model="claude-3-5-haiku-20241022",  # Fast and cheap for moderation
            max_tokens=100,
            messages=[{"role": "user", "content": moderation_prompt}],
        )

        result = response.content[0].text.strip()

        if result.startswith("APPROPRIATE"):
            logger.info("Topic approved", extra={"topic_length": len(topic)})
            return True, ""
        elif result.startswith("INAPPROPRIATE:"):
            reason = result.replace("INAPPROPRIATE:", "").strip()
            logger.info(
                "Topic rejected by moderation",
                extra={"topic_length": len(topic), "reason": reason},
            )
            return False, f"This topic may not be appropriate: {reason}"
        else:
            # If unclear response, err on the side of caution but be permissive
            logger.debug("Unclear moderation response - allowing", extra={"response": result})
            return True, ""

    except Exception as e:
        # If moderation fails, log the error but allow the topic (fail open for better UX)
        logger.warning(
            "Content moderation error - failing open",
            extra={"error": str(e), "topic_length": len(topic)},
        )
        return True, ""


def get_alternative_suggestions(rejected_topic: str = "") -> list[str]:
    """
    Provide alternative philosophical topics when a topic is rejected.

    Attempts to provide thematically related alternatives based on the rejected topic,
    falling back to general philosophical questions if no theme is detected.

    Args:
        rejected_topic: The topic that was rejected (optional)

    Returns:
        List of suggested alternative topics, potentially themed to the rejected topic
    """
    # Default philosophical questions
    default_suggestions = [
        "What is justice?",
        "What is the good life?",
        "Is morality relative or universal?",
        "What is consciousness?",
        "Do we have free will?",
        "Can AI have rights?",
        "What is truth?",
        "Is beauty objective?",
    ]

    # If no rejected topic provided, return defaults
    if not rejected_topic or not rejected_topic.strip():
        return default_suggestions

    # Thematic alternative suggestions based on keywords
    topic_lower = rejected_topic.lower()

    # Technology and AI themes
    if any(
        word in topic_lower
        for word in ["ai", "robot", "technology", "computer", "digital", "internet", "social media"]
    ):
        return [
            "Can AI have rights?",
            "Should we fear artificial intelligence?",
            "What is consciousness?",
            "Can machines be creative?",
            "What makes us human in a digital age?",
            "Is privacy a fundamental right?",
            "How should we regulate technology?",
            "What is the nature of intelligence?",
        ]

    # Ethics and morality themes
    if any(
        word in topic_lower
        for word in [
            "moral",
            "ethics",
            "right",
            "wrong",
            "should",
            "ought",
            "good",
            "bad",
            "virtue",
        ]
    ):
        return [
            "Is morality relative or universal?",
            "What is the good life?",
            "Can morality exist without religion?",
            "What is justice?",
            "Are there universal human rights?",
            "Is utilitarianism the best ethical framework?",
            "What role should empathy play in ethics?",
            "Can an action be both right and wrong?",
        ]

    # Politics and society themes
    if any(
        word in topic_lower
        for word in [
            "government",
            "politics",
            "society",
            "democracy",
            "freedom",
            "liberty",
            "law",
            "rights",
        ]
    ):
        return [
            "What is justice?",
            "What is the ideal form of government?",
            "Are there limits to freedom of speech?",
            "What is the social contract?",
            "Should voting be mandatory?",
            "What role should government play in our lives?",
            "Are universal human rights possible?",
            "Can democracy survive the digital age?",
        ]

    # Mind and consciousness themes
    if any(
        word in topic_lower
        for word in [
            "mind",
            "consciousness",
            "brain",
            "thought",
            "awareness",
            "perception",
            "mental",
            "cognitive",
        ]
    ):
        return [
            "What is consciousness?",
            "Do we have free will?",
            "Is the mind separate from the brain?",
            "What is the nature of reality?",
            "Can we trust our perceptions?",
            "What is the self?",
            "Are our thoughts truly our own?",
            "What is subjective experience?",
        ]

    # Existential and meaning themes
    if any(
        word in topic_lower
        for word in [
            "meaning",
            "purpose",
            "life",
            "death",
            "existence",
            "existential",
            "absurd",
            "suffer",
        ]
    ):
        return [
            "What is the good life?",
            "What makes life meaningful?",
            "Is there inherent meaning in the universe?",
            "How should we face mortality?",
            "Can we create our own purpose?",
            "What is happiness?",
            "Is suffering necessary for meaning?",
            "What is the examined life?",
        ]

    # Knowledge and truth themes
    if any(
        word in topic_lower
        for word in [
            "truth",
            "knowledge",
            "belief",
            "fact",
            "science",
            "evidence",
            "prove",
            "certain",
        ]
    ):
        return [
            "What is truth?",
            "Can we know anything with certainty?",
            "What is the relationship between science and philosophy?",
            "Is objective truth possible?",
            "What is knowledge?",
            "Can faith and reason coexist?",
            "What are the limits of human knowledge?",
            "How do we distinguish truth from opinion?",
        ]

    # Aesthetic and beauty themes
    if any(
        word in topic_lower
        for word in ["art", "beauty", "aesthetic", "music", "creative", "culture"]
    ):
        return [
            "Is beauty objective?",
            "What is art?",
            "Can machines be creative?",
            "What is the purpose of art?",
            "Is there a universal aesthetic?",
            "What makes something beautiful?",
            "Can art be immoral?",
            "What is the value of aesthetic experience?",
        ]

    # If no theme detected, return defaults
    return default_suggestions


def get_rejection_guidelines() -> str:
    """
    Provide general guidelines about what makes topics appropriate for philosophical discourse.

    Returns:
        Markdown-formatted string explaining content guidelines
    """
    return """
**Our Guidelines for Philosophical Discourse**

We welcome questions that:
- Explore ethics, morality, and values through reasoned inquiry
- Question fundamental assumptions about society, knowledge, or existence
- Examine difficult topics with intellectual rigor and good faith
- Seek understanding through the Socratic method

We filter out topics that:
- Contain explicit sexual or violent content
- Include hate speech or discriminatory language
- Promote illegal activities (policy questions about legalization are welcome)
- Appear designed to provoke rather than explore

**The Difference**: "Should drugs be legalized?" explores policy and ethics ✓
vs. explicit content about drug use ✗

If your topic was rejected, try rephrasing it as a philosophical question that explores underlying principles, values, or reasoning rather than specific content.
"""
