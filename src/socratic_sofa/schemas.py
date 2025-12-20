"""
Pydantic schemas for structured output from Socratic Sofa dialogue tasks.

These schemas ensure consistent, well-formatted output from CrewAI tasks
for better readability in the Gradio interface.
"""

from pydantic import BaseModel, Field


class TopicOutput(BaseModel):
    """Structured output for the propose_topic task."""

    topic: str = Field(description="The philosophical topic or question for the dialogue")
    context: str = Field(
        description="Brief context explaining why this topic is philosophically significant"
    )
    key_concepts: list[str] = Field(
        description="2-4 key philosophical concepts this topic will explore",
        min_length=2,
        max_length=4,
    )


class SocraticQuestion(BaseModel):
    """A single Socratic question with its purpose."""

    question: str = Field(description="The Socratic question itself")
    purpose: str = Field(
        description="Brief explanation of what this question aims to reveal or challenge"
    )


class InquiryOutput(BaseModel):
    """Structured output for the propose and oppose tasks (Socratic inquiries)."""

    philosophical_angle: str = Field(
        description="The specific philosophical perspective or angle being explored"
    )
    opening_statement: str = Field(description="A brief statement framing the inquiry approach")
    questions: list[SocraticQuestion] = Field(
        description="5-7 carefully crafted Socratic questions",
        min_length=5,
        max_length=7,
    )
    insight_summary: str = Field(
        description="A brief summary of the philosophical tensions or insights revealed"
    )


class CriterionScore(BaseModel):
    """Score for a single evaluation criterion."""

    score: int = Field(description="Score from 1-5", ge=1, le=5)
    assessment: str = Field(description="Brief assessment explaining the score")


class InquiryEvaluation(BaseModel):
    """Evaluation of a single inquiry."""

    question_quality: CriterionScore = Field(
        description="Assessment of whether questions genuinely probe or merely lead"
    )
    elenctic_effectiveness: CriterionScore = Field(
        description="Assessment of how well contradictions are revealed"
    )
    philosophical_insight: CriterionScore = Field(
        description="Assessment of depth and significance of insights"
    )
    socratic_fidelity: CriterionScore = Field(
        description="Assessment of adherence to genuine Socratic method"
    )


class JudgmentOutput(BaseModel):
    """Structured output for the judge_task (dialectic evaluation)."""

    first_inquiry: InquiryEvaluation = Field(description="Evaluation of the first line of inquiry")
    second_inquiry: InquiryEvaluation = Field(
        description="Evaluation of the second/alternative line of inquiry"
    )
    differentiation_score: int = Field(
        description="Bonus score (0-10) for how distinct the second inquiry is from the first",
        ge=0,
        le=10,
    )
    differentiation_assessment: str = Field(
        description="Assessment of how the second inquiry differentiates from the first"
    )
    winner: str = Field(
        description="Which inquiry was more effective: 'First', 'Second', or 'Both equally effective'"
    )
    socratic_exemplification: str = Field(
        description="Assessment of which inquiry better exemplifies the Socratic method and why"
    )
    recommendation: str = Field(
        description="One-sentence suggestion for deepening the Socratic examination"
    )


def format_topic_output(output: TopicOutput) -> str:
    """Format TopicOutput as readable markdown."""
    lines = [
        f"## {output.topic}",
        "",
        output.context,
        "",
        "**Key Concepts:**",
    ]
    for concept in output.key_concepts:
        lines.append(f"- {concept}")
    return "\n".join(lines)


def format_inquiry_output(output: InquiryOutput, title: str, emoji: str) -> str:
    """Format InquiryOutput as readable markdown."""
    lines = [
        f"## {emoji} {title}",
        "",
        f"**Philosophical Angle:** {output.philosophical_angle}",
        "",
        output.opening_statement,
        "",
        "---",
        "",
    ]

    for i, q in enumerate(output.questions, 1):
        lines.append(f"### Question {i}")
        lines.append(f"> {q.question}")
        lines.append("")
        lines.append(f"*Purpose: {q.purpose}*")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"**Insight:** {output.insight_summary}")

    return "\n".join(lines)


def _format_criterion(name: str, criterion: CriterionScore) -> str:
    """Format a single criterion score."""
    emoji = "✅" if criterion.score >= 4 else "⚠️" if criterion.score >= 3 else "❌"
    return f"- {emoji} **{name}** ({criterion.score}/5): {criterion.assessment}"


def format_judgment_output(output: JudgmentOutput) -> str:
    """Format JudgmentOutput as readable markdown."""

    # Calculate total scores
    def calc_total(eval: InquiryEvaluation) -> float:
        weighted = (
            eval.question_quality.score * 0.40
            + eval.elenctic_effectiveness.score * 0.25
            + eval.philosophical_insight.score * 0.20
            + eval.socratic_fidelity.score * 0.15
        )
        return (weighted / 5) * 100

    first_total = calc_total(output.first_inquiry)
    second_total = calc_total(output.second_inquiry) + output.differentiation_score

    lines = [
        "## Dialectic Evaluation",
        "",
        "### Scoring Breakdown",
        "",
        "| Criterion | First Inquiry | Second Inquiry |",
        "|-----------|--------------|----------------|",
        f"| **Question Quality** (40%) | {output.first_inquiry.question_quality.score}/5 | {output.second_inquiry.question_quality.score}/5 |",
        f"| **Elenctic Effectiveness** (25%) | {output.first_inquiry.elenctic_effectiveness.score}/5 | {output.second_inquiry.elenctic_effectiveness.score}/5 |",
        f"| **Philosophical Insight** (20%) | {output.first_inquiry.philosophical_insight.score}/5 | {output.second_inquiry.philosophical_insight.score}/5 |",
        f"| **Socratic Fidelity** (15%) | {output.first_inquiry.socratic_fidelity.score}/5 | {output.second_inquiry.socratic_fidelity.score}/5 |",
        f"| **Differentiation Quality** (bonus +10%) | N/A | +{output.differentiation_score}% |",
        f"| **Total Score** | {first_total:.0f}% | {second_total:.0f}% |",
        "",
        "### Assessment",
        "",
        f"**Winner**: {output.winner}",
        "",
        f"**Differentiation**: {output.differentiation_assessment}",
        "",
        f"**Socratic Exemplification**: {output.socratic_exemplification}",
        "",
        "### Detailed Analysis",
        "",
        "**First Inquiry:**",
        _format_criterion("Question Quality", output.first_inquiry.question_quality),
        _format_criterion("Elenctic Effectiveness", output.first_inquiry.elenctic_effectiveness),
        _format_criterion("Philosophical Insight", output.first_inquiry.philosophical_insight),
        _format_criterion("Socratic Fidelity", output.first_inquiry.socratic_fidelity),
        "",
        "**Second Inquiry:**",
        _format_criterion("Question Quality", output.second_inquiry.question_quality),
        _format_criterion("Elenctic Effectiveness", output.second_inquiry.elenctic_effectiveness),
        _format_criterion("Philosophical Insight", output.second_inquiry.philosophical_insight),
        _format_criterion("Socratic Fidelity", output.second_inquiry.socratic_fidelity),
        "",
        "### Recommendation",
        "",
        f"*{output.recommendation}*",
    ]

    return "\n".join(lines)
