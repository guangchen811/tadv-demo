from datetime import datetime, timezone

import pytest

from tadv.api.v1.schemas import CodeFile, CodeLanguage, ConstraintCode, GenerateConstraintsOptions


def test_code_file_serializes_camel_case():
    cf = CodeFile(
        id="uuid",
        name="task.py",
        language=CodeLanguage.PYTHON,
        size=1,
        content="print('hi')",
        uploaded_at=datetime(2026, 1, 28, 10, 30, tzinfo=timezone.utc),
    )
    data = cf.model_dump(by_alias=True)
    assert "uploadedAt" in data
    assert "uploaded_at" not in data


def test_constraint_code_serializes_expected_keys():
    code = ConstraintCode(great_expectations="gx()", deequ="deequ()")
    data = code.model_dump(by_alias=True)
    assert set(data.keys()) == {"greatExpectations", "deequ"}


@pytest.mark.parametrize("payload_key", ["confidenceThreshold", "confidence threshold", "confidence_threshold"])
def test_generate_constraints_options_accepts_confidence_threshold_aliases(payload_key: str):
    opt = GenerateConstraintsOptions.model_validate({payload_key: 0.9})
    assert opt.confidence_threshold == 0.9

