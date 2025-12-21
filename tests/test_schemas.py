"""Tests for Pydantic output schemas."""

import pytest
from pydantic import ValidationError

from socratic_sofa.schemas import (
    CriterionScore,
    InquiryEvaluation,
    InquiryOutput,
    JudgmentOutput,
    SocraticQuestion,
    TopicOutput,
    format_inquiry_output,
    format_judgment_output,
    format_topic_output,
)


class TestTopicOutput:
    """Tests for TopicOutput schema."""

    def test_valid_topic_output(self):
        """Test creating a valid TopicOutput."""
        output = TopicOutput(
            topic="What is justice?",
            context="Justice is a fundamental concept in moral and political philosophy.",
            key_concepts=["fairness", "virtue", "social order"],
        )
        assert output.topic == "What is justice?"
        assert "fundamental" in output.context
        assert len(output.key_concepts) == 3

    def test_topic_output_minimum_concepts(self):
        """Test TopicOutput with minimum 2 key concepts."""
        output = TopicOutput(
            topic="What is truth?",
            context="Truth is central to epistemology.",
            key_concepts=["knowledge", "belief"],
        )
        assert len(output.key_concepts) == 2

    def test_topic_output_maximum_concepts(self):
        """Test TopicOutput with maximum 4 key concepts."""
        output = TopicOutput(
            topic="What is happiness?",
            context="Happiness is a core concern in ethics.",
            key_concepts=["pleasure", "virtue", "meaning", "flourishing"],
        )
        assert len(output.key_concepts) == 4

    def test_topic_output_too_few_concepts(self):
        """Test TopicOutput fails with fewer than 2 key concepts."""
        with pytest.raises(ValidationError):
            TopicOutput(
                topic="What is love?",
                context="Love is complex.",
                key_concepts=["emotion"],  # Only 1
            )

    def test_topic_output_too_many_concepts(self):
        """Test TopicOutput fails with more than 4 key concepts."""
        with pytest.raises(ValidationError):
            TopicOutput(
                topic="What is existence?",
                context="Existence is fundamental.",
                key_concepts=["being", "becoming", "essence", "existence", "reality"],  # 5
            )


class TestSocraticQuestion:
    """Tests for SocraticQuestion schema."""

    def test_valid_question(self):
        """Test creating a valid SocraticQuestion."""
        question = SocraticQuestion(
            question="What do you mean by justice?",
            purpose="To clarify the definition being used",
        )
        assert "justice" in question.question
        assert "clarify" in question.purpose


class TestInquiryOutput:
    """Tests for InquiryOutput schema."""

    def test_valid_inquiry_output(self):
        """Test creating a valid InquiryOutput."""
        questions = [
            SocraticQuestion(question=f"Question {i}?", purpose=f"Purpose {i}") for i in range(5)
        ]
        output = InquiryOutput(
            philosophical_angle="Individual moral experience",
            opening_statement="Let us examine justice from the individual's perspective.",
            questions=questions,
            insight_summary="Tensions between personal and societal justice emerge.",
        )
        assert output.philosophical_angle == "Individual moral experience"
        assert len(output.questions) == 5

    def test_inquiry_output_minimum_questions(self):
        """Test InquiryOutput with minimum 5 questions."""
        questions = [SocraticQuestion(question=f"Q{i}?", purpose=f"P{i}") for i in range(5)]
        output = InquiryOutput(
            philosophical_angle="Test angle",
            opening_statement="Test statement",
            questions=questions,
            insight_summary="Test insight",
        )
        assert len(output.questions) == 5

    def test_inquiry_output_maximum_questions(self):
        """Test InquiryOutput with maximum 7 questions."""
        questions = [SocraticQuestion(question=f"Q{i}?", purpose=f"P{i}") for i in range(7)]
        output = InquiryOutput(
            philosophical_angle="Test angle",
            opening_statement="Test statement",
            questions=questions,
            insight_summary="Test insight",
        )
        assert len(output.questions) == 7

    def test_inquiry_output_too_few_questions(self):
        """Test InquiryOutput fails with fewer than 5 questions."""
        questions = [SocraticQuestion(question=f"Q{i}?", purpose=f"P{i}") for i in range(4)]
        with pytest.raises(ValidationError):
            InquiryOutput(
                philosophical_angle="Test",
                opening_statement="Test",
                questions=questions,
                insight_summary="Test",
            )

    def test_inquiry_output_too_many_questions(self):
        """Test InquiryOutput fails with more than 7 questions."""
        questions = [SocraticQuestion(question=f"Q{i}?", purpose=f"P{i}") for i in range(8)]
        with pytest.raises(ValidationError):
            InquiryOutput(
                philosophical_angle="Test",
                opening_statement="Test",
                questions=questions,
                insight_summary="Test",
            )


class TestCriterionScore:
    """Tests for CriterionScore schema."""

    def test_valid_score(self):
        """Test creating a valid CriterionScore."""
        score = CriterionScore(score=4, assessment="Excellent questioning technique")
        assert score.score == 4
        assert "Excellent" in score.assessment

    def test_minimum_score(self):
        """Test minimum valid score of 1."""
        score = CriterionScore(score=1, assessment="Needs improvement")
        assert score.score == 1

    def test_maximum_score(self):
        """Test maximum valid score of 5."""
        score = CriterionScore(score=5, assessment="Outstanding")
        assert score.score == 5

    def test_score_too_low(self):
        """Test score fails when below 1."""
        with pytest.raises(ValidationError):
            CriterionScore(score=0, assessment="Invalid")

    def test_score_too_high(self):
        """Test score fails when above 5."""
        with pytest.raises(ValidationError):
            CriterionScore(score=6, assessment="Invalid")


class TestInquiryEvaluation:
    """Tests for InquiryEvaluation schema."""

    def test_valid_evaluation(self):
        """Test creating a valid InquiryEvaluation."""
        evaluation = InquiryEvaluation(
            question_quality=CriterionScore(score=4, assessment="Good probing"),
            elenctic_effectiveness=CriterionScore(score=3, assessment="Some contradictions"),
            philosophical_insight=CriterionScore(score=5, assessment="Deep insights"),
            socratic_fidelity=CriterionScore(score=4, assessment="Follows method"),
        )
        assert evaluation.question_quality.score == 4
        assert evaluation.philosophical_insight.score == 5


class TestJudgmentOutput:
    """Tests for JudgmentOutput schema."""

    @pytest.fixture
    def sample_evaluation(self):
        """Create a sample InquiryEvaluation for testing."""
        return InquiryEvaluation(
            question_quality=CriterionScore(score=4, assessment="Good"),
            elenctic_effectiveness=CriterionScore(score=3, assessment="Adequate"),
            philosophical_insight=CriterionScore(score=4, assessment="Insightful"),
            socratic_fidelity=CriterionScore(score=4, assessment="Authentic"),
        )

    def test_valid_judgment_output(self, sample_evaluation):
        """Test creating a valid JudgmentOutput."""
        output = JudgmentOutput(
            first_inquiry=sample_evaluation,
            second_inquiry=sample_evaluation,
            differentiation_score=8,
            differentiation_assessment="Second inquiry takes a completely different angle.",
            winner="Second",
            socratic_exemplification="Second inquiry better demonstrates elenchus.",
            recommendation="Explore the tension between individual and collective more deeply.",
        )
        assert output.differentiation_score == 8
        assert output.winner == "Second"

    def test_differentiation_score_range(self, sample_evaluation):
        """Test differentiation score must be 0-10."""
        # Valid minimum
        output = JudgmentOutput(
            first_inquiry=sample_evaluation,
            second_inquiry=sample_evaluation,
            differentiation_score=0,
            differentiation_assessment="Significant overlap",
            winner="First",
            socratic_exemplification="First is better",
            recommendation="More differentiation needed",
        )
        assert output.differentiation_score == 0

        # Valid maximum
        output = JudgmentOutput(
            first_inquiry=sample_evaluation,
            second_inquiry=sample_evaluation,
            differentiation_score=10,
            differentiation_assessment="Complete differentiation",
            winner="Both equally effective",
            socratic_exemplification="Both excellent",
            recommendation="Continue this approach",
        )
        assert output.differentiation_score == 10

    def test_differentiation_score_too_low(self, sample_evaluation):
        """Test differentiation score fails below 0."""
        with pytest.raises(ValidationError):
            JudgmentOutput(
                first_inquiry=sample_evaluation,
                second_inquiry=sample_evaluation,
                differentiation_score=-1,
                differentiation_assessment="Invalid",
                winner="First",
                socratic_exemplification="Test",
                recommendation="Test",
            )

    def test_differentiation_score_too_high(self, sample_evaluation):
        """Test differentiation score fails above 10."""
        with pytest.raises(ValidationError):
            JudgmentOutput(
                first_inquiry=sample_evaluation,
                second_inquiry=sample_evaluation,
                differentiation_score=11,
                differentiation_assessment="Invalid",
                winner="First",
                socratic_exemplification="Test",
                recommendation="Test",
            )


class TestFormatTopicOutput:
    """Tests for format_topic_output function."""

    def test_format_topic_output(self):
        """Test formatting TopicOutput to markdown."""
        output = TopicOutput(
            topic="What is justice?",
            context="Justice is a core concept in moral philosophy.",
            key_concepts=["fairness", "virtue", "law"],
        )
        result = format_topic_output(output)

        assert "## What is justice?" in result
        assert "Justice is a core concept" in result
        assert "**Key Concepts:**" in result
        assert "- fairness" in result
        assert "- virtue" in result
        assert "- law" in result


class TestFormatInquiryOutput:
    """Tests for format_inquiry_output function."""

    def test_format_inquiry_output(self):
        """Test formatting InquiryOutput to markdown."""
        questions = [
            SocraticQuestion(
                question="What do you mean by justice?",
                purpose="To clarify the definition",
            ),
            SocraticQuestion(
                question="Is justice the same as fairness?",
                purpose="To probe assumptions",
            ),
            SocraticQuestion(
                question="Can there be unjust laws?",
                purpose="To reveal contradictions",
            ),
            SocraticQuestion(
                question="Who determines what is just?",
                purpose="To examine authority",
            ),
            SocraticQuestion(
                question="Is justice universal or relative?",
                purpose="To explore scope",
            ),
        ]
        output = InquiryOutput(
            philosophical_angle="Individual moral experience",
            opening_statement="Let us examine justice personally.",
            questions=questions,
            insight_summary="Personal and social justice may conflict.",
        )

        result = format_inquiry_output(output, "First Line of Inquiry", "🔵")

        assert "## 🔵 First Line of Inquiry" in result
        assert "**Philosophical Angle:** Individual moral experience" in result
        assert "Let us examine justice personally." in result
        assert "### Question 1" in result
        assert "> What do you mean by justice?" in result
        assert "*Purpose: To clarify the definition*" in result
        assert "**Insight:** Personal and social justice may conflict." in result


class TestFormatJudgmentOutput:
    """Tests for format_judgment_output function."""

    def test_format_judgment_output(self):
        """Test formatting JudgmentOutput to markdown."""
        evaluation = InquiryEvaluation(
            question_quality=CriterionScore(score=4, assessment="Strong probing"),
            elenctic_effectiveness=CriterionScore(score=3, assessment="Good contradictions"),
            philosophical_insight=CriterionScore(score=5, assessment="Deep insights"),
            socratic_fidelity=CriterionScore(score=4, assessment="Authentic method"),
        )

        output = JudgmentOutput(
            first_inquiry=evaluation,
            second_inquiry=evaluation,
            differentiation_score=7,
            differentiation_assessment="Second takes a different angle effectively.",
            winner="Second",
            socratic_exemplification="Second better demonstrates elenchus.",
            recommendation="Explore practical implications more.",
        )

        result = format_judgment_output(output)

        assert "## Dialectic Evaluation" in result
        assert "### Scoring Breakdown" in result
        assert "| **Question Quality** (40%)" in result
        assert "4/5" in result
        assert "**Winner**: Second" in result
        assert "+7%" in result
        assert "### Recommendation" in result
        assert "Explore practical implications more." in result

    def test_format_judgment_uses_correct_emojis(self):
        """Test that formatting uses correct emojis based on scores."""
        high_score = CriterionScore(score=5, assessment="Excellent")
        mid_score = CriterionScore(score=3, assessment="Adequate")
        low_score = CriterionScore(score=2, assessment="Weak")

        evaluation_high = InquiryEvaluation(
            question_quality=high_score,
            elenctic_effectiveness=high_score,
            philosophical_insight=high_score,
            socratic_fidelity=high_score,
        )
        evaluation_mixed = InquiryEvaluation(
            question_quality=high_score,
            elenctic_effectiveness=mid_score,
            philosophical_insight=low_score,
            socratic_fidelity=mid_score,
        )

        output = JudgmentOutput(
            first_inquiry=evaluation_high,
            second_inquiry=evaluation_mixed,
            differentiation_score=5,
            differentiation_assessment="Partial differentiation",
            winner="First",
            socratic_exemplification="First is stronger overall",
            recommendation="Second needs more depth",
        )

        result = format_judgment_output(output)

        # Check emojis appear (✅ for high, ⚠️ for mid, ❌ for low)
        assert "✅" in result
        assert "⚠️" in result
        assert "❌" in result
