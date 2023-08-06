"""
Utilities for testing
"""
from unittest.mock import patch


class patch_env(patch.dict):
    """
    Patch environment variables. Clears by default. Use just like patch.dict.
    """

    def __init__(self, values=(), clear=True, **kwargs):
        super().__init__("os.environ", values=values, clear=clear, **kwargs)
