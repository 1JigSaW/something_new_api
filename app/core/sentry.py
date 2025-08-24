from typing import Any

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration


def init_sentry(
    dsn: str | None,
    environment: str,
) -> None:
    """Initialize Sentry if DSN is provided.

    Parameters
    ----------
    dsn
        Sentry DSN string. If None or empty, Sentry is not initialized.
    environment
        Environment name (e.g., dev, staging, prod).
    """

    if not dsn:
        return

    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        integrations=[FastApiIntegration()],
        traces_sample_rate=0.0,
        profiles_sample_rate=0.0,
    )


