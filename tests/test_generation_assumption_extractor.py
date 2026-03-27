"""Tests for assumption extraction using DSPy."""

from __future__ import annotations

import pytest
from unittest.mock import MagicMock

# Skip all tests if dspy is not installed
dspy = pytest.importorskip("dspy")

from tadv.generation import AssumptionExtractor
from tadv.ir import AssumptionIR, SourceSpan
from tadv.llm.errors import LLMOutputError


@pytest.fixture
def mock_lm():
    """Create a mock dspy.LM for testing."""
    lm = MagicMock(spec=dspy.LM)
    return lm


def test_assumption_extractor_basic(mock_lm):
    """Test basic assumption extraction."""
    extractor = AssumptionExtractor(lm=mock_lm)

    # Mock predictor to return a valid assumption
    mock_prediction = dspy.Prediction(assumptions=[
        {
            "text": "Age must be between 18 and 65",
            "columns": ["age"],
            "type": "range",
            "confidence": 0.95,
            "source_lines": [15, 16]
        }
    ])
    extractor._predictor = MagicMock(return_value=mock_prediction)

    assumptions = extractor.extract(
        code_script="df[df['age'] >= 18]",
        columns=["age", "name"],
        accessed_columns=["age"],
        task_description="Filter adults",
    )

    assert len(assumptions) == 1
    assert isinstance(assumptions[0], AssumptionIR)
    assert assumptions[0].text == "Age must be between 18 and 65"
    assert assumptions[0].columns == ["age"]
    assert assumptions[0].constraint_type == "range"
    assert assumptions[0].confidence == 0.95
    assert len(assumptions[0].sources) == 2
    assert assumptions[0].sources[0].start_line == 15


def test_assumption_extractor_multiple_assumptions(mock_lm):
    """Test extracting multiple assumptions."""
    extractor = AssumptionExtractor(lm=mock_lm)

    mock_prediction = dspy.Prediction(assumptions=[
        {
            "text": "Name must not be null",
            "columns": ["name"],
            "type": "completeness",
            "confidence": 0.98,
            "source_lines": [10]
        },
        {
            "text": "Category must be PREMIUM, STANDARD, or BASIC",
            "columns": ["category"],
            "type": "enum",
            "confidence": 0.92,
            "source_lines": [7]
        }
    ])
    extractor._predictor = MagicMock(return_value=mock_prediction)

    assumptions = extractor.extract(
        code_script="...",
        columns=["name", "category", "age"],
        accessed_columns=["name", "category"],
        task_description="Process customer data",
    )

    assert len(assumptions) == 2
    assert assumptions[0].constraint_type == "completeness"
    assert assumptions[1].constraint_type == "enum"


def test_assumption_extractor_filters_invalid_columns(mock_lm):
    """Test that extractor filters out invalid column names."""
    extractor = AssumptionExtractor(lm=mock_lm)

    # LLM returns an assumption with invalid column
    mock_prediction = dspy.Prediction(assumptions=[
        {
            "text": "Valid assumption",
            "columns": ["age"],
            "type": "range",
            "confidence": 0.9,
            "source_lines": [5]
        },
        {
            "text": "Invalid assumption",
            "columns": ["invalid_column"],  # Not in allowed columns
            "type": "completeness",
            "confidence": 0.8,
            "source_lines": [10]
        }
    ])
    extractor._predictor = MagicMock(return_value=mock_prediction)

    assumptions = extractor.extract(
        code_script="...",
        columns=["age", "name"],
        accessed_columns=["age"],
        task_description="test",
    )

    # Should only include the valid assumption
    assert len(assumptions) == 1
    assert assumptions[0].columns == ["age"]


def test_assumption_extractor_handles_comma_separated_columns(mock_lm):
    """Test that extractor handles columns provided as comma-separated string."""
    extractor = AssumptionExtractor(lm=mock_lm)

    mock_prediction = dspy.Prediction(assumptions=[
        {
            "text": "Test",
            "columns": "age, name",  # String instead of list
            "type": "completeness",
            "confidence": 0.9,
            "source_lines": [5]
        }
    ])
    extractor._predictor = MagicMock(return_value=mock_prediction)

    assumptions = extractor.extract(
        code_script="...",
        columns=["age", "name"],
        accessed_columns=["age", "name"],
        task_description="test",
    )

    assert len(assumptions) == 1
    assert set(assumptions[0].columns) == {"age", "name"}


def test_assumption_extractor_clamps_confidence(mock_lm):
    """Test that confidence values are clamped to [0, 1]."""
    extractor = AssumptionExtractor(lm=mock_lm)

    mock_prediction = dspy.Prediction(assumptions=[
        {
            "text": "Test 1",
            "columns": ["age"],
            "type": "range",
            "confidence": 1.5,  # > 1.0
            "source_lines": [5]
        },
        {
            "text": "Test 2",
            "columns": ["name"],
            "type": "completeness",
            "confidence": -0.2,  # < 0.0
            "source_lines": [10]
        }
    ])
    extractor._predictor = MagicMock(return_value=mock_prediction)

    assumptions = extractor.extract(
        code_script="...",
        columns=["age", "name"],
        accessed_columns=["age", "name"],
        task_description="test",
    )

    assert assumptions[0].confidence == 1.0  # Clamped to 1.0
    assert assumptions[1].confidence == 0.0  # Clamped to 0.0


def test_assumption_extractor_empty_output_raises_error(mock_lm):
    """Test that empty output raises LLMOutputError."""
    extractor = AssumptionExtractor(lm=mock_lm)

    mock_prediction = dspy.Prediction(assumptions=[])
    extractor._predictor = MagicMock(return_value=mock_prediction)

    with pytest.raises(LLMOutputError, match="no valid assumptions"):
        extractor.extract(
            code_script="...",
            columns=["age"],
            accessed_columns=["age"],
            task_description="test",
        )


def test_assumption_extractor_skips_invalid_entries(mock_lm):
    """Test that extractor skips invalid/malformed entries."""
    extractor = AssumptionExtractor(lm=mock_lm)

    mock_prediction = dspy.Prediction(assumptions=[
        {
            "text": "",  # Empty text - should skip
            "columns": ["age"],
            "type": "range",
            "confidence": 0.9,
            "source_lines": [5]
        },
        {
            "text": "Valid assumption",
            "columns": ["name"],
            "type": "completeness",
            "confidence": 0.95,
            "source_lines": [10]
        },
        "not a dict",  # Invalid entry - should skip
    ])
    extractor._predictor = MagicMock(return_value=mock_prediction)

    assumptions = extractor.extract(
        code_script="...",
        columns=["age", "name"],
        accessed_columns=["age", "name"],
        task_description="test",
    )

    # Should only include the valid assumption
    assert len(assumptions) == 1
    assert assumptions[0].text == "Valid assumption"


def test_assumption_extractor_uses_highlighted_code_when_data_flow_provided(mock_lm):
    """Test that data_flow_sources triggers highlighted line numbers."""
    extractor = AssumptionExtractor(lm=mock_lm)

    mock_prediction = dspy.Prediction(assumptions=[
        {
            "text": "Age must be positive",
            "columns": ["age"],
            "type": "range",
            "confidence": 0.9,
            "source_lines": [2]
        }
    ])
    extractor._predictor = MagicMock(return_value=mock_prediction)

    code = "import pandas as pd\ndf = df[df['age'] > 0]\nprint(df)"
    data_flow_sources = [SourceSpan(start_line=2, end_line=2)]

    assumptions = extractor.extract(
        code_script=code,
        columns=["age"],
        accessed_columns=["age"],
        task_description="test",
        data_flow_sources=data_flow_sources,
    )

    assert len(assumptions) == 1
    # Verify the predictor received highlighted code
    call_kwargs = extractor._predictor.call_args[1]
    code_sent = call_kwargs["code_script"]
    assert "-**->" in code_sent  # Should have highlighting markers
    assert "0002:" in code_sent  # 4-digit zero-padded


def test_assumption_extractor_plain_code_without_data_flow(mock_lm):
    """Test that plain line numbers are used without data_flow_sources."""
    extractor = AssumptionExtractor(lm=mock_lm)

    mock_prediction = dspy.Prediction(assumptions=[
        {
            "text": "Age must be positive",
            "columns": ["age"],
            "type": "range",
            "confidence": 0.9,
            "source_lines": [2]
        }
    ])
    extractor._predictor = MagicMock(return_value=mock_prediction)

    code = "import pandas as pd\ndf = df[df['age'] > 0]\nprint(df)"

    extractor.extract(
        code_script=code,
        columns=["age"],
        accessed_columns=["age"],
        task_description="test",
    )

    # Verify plain line numbers (no highlighting markers)
    call_kwargs = extractor._predictor.call_args[1]
    code_sent = call_kwargs["code_script"]
    assert "-**->" not in code_sent
    assert " | " in code_sent  # Plain format: "1 | code"
