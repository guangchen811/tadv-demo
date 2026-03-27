"""LLM utilities and error handling.

Note: This module previously defined an LLMClient protocol, but we've moved
to using DSPy directly for all LLM interactions. See tadv.generation for
DSPy-based implementations.
"""

from tadv.llm.errors import LLMError, LLMOutputError
from tadv.llm.factory import create_lm, create_lm_from_env

__all__ = [
    "LLMError",
    "LLMOutputError",
    "create_lm",
    "create_lm_from_env",
]
