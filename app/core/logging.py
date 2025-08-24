import logging
from typing import Any

import structlog


def configure_logging(level: int | str) -> None:
    """Configure standard logging and structlog.

    Parameters
    ----------
    level
        Logging level for root logger, e.g., logging.INFO.
    """

    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)

    timestamper = structlog.processors.TimeStamper(fmt="iso")

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            timestamper,
            structlog.stdlib.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(serializer=None),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        level=level,
        format="%(message)s",
    )


def get_logger(
    name: str,
) -> structlog.stdlib.BoundLogger:
    """Return a structured logger bound to the given name.

    Parameters
    ----------
    name
        Logger name to bind.
    """

    return structlog.get_logger(name)


