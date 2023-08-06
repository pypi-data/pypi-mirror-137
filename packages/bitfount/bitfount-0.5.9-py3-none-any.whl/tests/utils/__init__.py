"""Utility modules for tests."""
from _pytest.fixtures import SubRequest

# See TODO: [BIT-1051] comments below for why this is kept
# from typing_extensions import TypeAlias

# It's actually `SubRequest` that has the `param` attribute guaranteed so this
# is what we want for type checking purposes, even though it's not part of the
# public API.
# TODO: [BIT-1051] Explicit TypeAlias isn't yet supported in mypy (v0.910) but
#       should be in the next release. Once it is, we can swap the below assignments
#       to be more explicit. The import comment above will also need to be uncommented.
# PytestRequest: TypeAlias = SubRequest
PytestRequest = SubRequest
