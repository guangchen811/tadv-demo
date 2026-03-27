"""GEPA prompt optimization module for TaDV.

Optimizes the three LLM module prompts (Column Access Detection, Assumption
Extraction, Constraint Generation) using DVBench binary task outcomes as
training signal.

Usage::

    from tadv.optimization import run_gepa, DVBenchLoader

    loader = DVBenchLoader()
    units = loader.load_training_units("IPL_win_prediction", max_units=40)
    result = run_gepa(lm=my_lm, training_units=units, n_rounds=2, budget=6)
    print(result.after_instructions)
"""

from tadv.optimization.adapter import (
    ALL_COMPONENTS,
    COMPONENT_COLUMN_ACCESS,
    COMPONENT_ASSUMPTION_EXTRACTION,
    COMPONENT_CONSTRAINT_GENERATION,
    TaDVAdapter,
    _extract_instructions,
)
from tadv.optimization.config import (
    clear_active_instructions,
    get_active_instructions,
    has_active_instructions,
    set_active_instructions,
)
from tadv.optimization.engine import run_gepa
from tadv.optimization.result import OptimizationResult
from tadv.optimization.training import DVBenchLoader, TrainingUnit

__all__ = [
    "get_active_instructions",
    "set_active_instructions",
    "clear_active_instructions",
    "has_active_instructions",
    "run_gepa",
    "DVBenchLoader",
    "TrainingUnit",
    "OptimizationResult",
    "TaDVAdapter",
    "_extract_instructions",
    "ALL_COMPONENTS",
    "COMPONENT_COLUMN_ACCESS",
    "COMPONENT_ASSUMPTION_EXTRACTION",
    "COMPONENT_CONSTRAINT_GENERATION",
]
