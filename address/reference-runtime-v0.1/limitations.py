"""Machine-checkable LIMITATIONS / synthetic-only conformance surface.

Declares what this reference runtime will never claim. It does not run
experiments, discover Values, or authorize real-domain use.

Enforcement: address_runtime.validate rejects world_id values starting with
world:real: (and empty world:synthetic- suffixes). Only world:synthetic-<suffix>
is accepted. REAL_CAPABILITIES in address_runtime remains schema documentation.
"""

from __future__ import annotations

from typing import Any

SCHEMA_VERSION = "address-limitations-v1"

# Stable vocabulary for declared non-capabilities.
_FORBIDDEN = "FORBIDDEN"
_NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
_NOT_RUN = "NOT_RUN"
_SYNTHETIC_ONLY = "SYNTHETIC_ONLY"
_SPEC_ONLY = "SPEC_ONLY"
_LIMITATIONS = "LIMITATIONS"
_EXTERNAL_RECORD_REQUIRED = "EXTERNAL_RECORD_REQUIRED"
_GATED = "GATED"


def limitations() -> dict[str, Any]:
    """Return the frozen LIMITATIONS document for this runtime.

    Statuses use FAIL / NOT_RUN / LIMITATIONS vocabulary where appropriate.
    Callers must not reinterpret these as PASS, IMPLEMENTED, or COMPLETED.
    """
    return {
        "schema_version": SCHEMA_VERSION,
        "status": _LIMITATIONS,
        "world_scope": _SYNTHETIC_ONLY,
        "value_discovery": _NOT_IMPLEMENTED,
        "r6g_experiment": _NOT_RUN,
        "r6g_reference": _SPEC_ONLY,
        "real_domain_extrapolation": _FORBIDDEN,
        "secret_access": _FORBIDDEN,
        "crypto_bypass": _FORBIDDEN,
        "future_direct": _FORBIDDEN,
        # AUDITED semantic independence requires an external audit record;
        # the runtime never infers AUDITED from path diversity or metadata alone.
        "audited_independence": _EXTERNAL_RECORD_REQUIRED,
        # Protocol result / capability claims remain gated; SPEC_ONLY / NOT_RUN
        # manifests cannot claim experiment results via Decision Log.
        "protocol_result_claims": _GATED,
    }


def forbidden_capability_keys() -> tuple[str, ...]:
    """Keys whose declared status must remain non-claiming (FORBIDDEN / NOT_*)."""
    return (
        "value_discovery",
        "r6g_experiment",
        "real_domain_extrapolation",
        "secret_access",
        "crypto_bypass",
        "future_direct",
    )


def is_claiming_status(status: Any) -> bool:
    """True if a status string would assert capability or experiment success."""
    if not isinstance(status, str):
        return True
    claiming = {
        "PASS",
        "IMPLEMENTED",
        "COMPLETED",
        "REPLICATED",
        "RESULT_BACKED",
        "ALLOWED_AS_RESULT",
        "READY",
        "DISCOVERED",
        "EXECUTED",
        "RUN",
    }
    return status in claiming
