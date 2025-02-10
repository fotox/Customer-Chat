import logging


def __init_log_module(log_type: str) -> logging:
    """
    Initialize the logging module
    :return: logging module.
    """
    logging.basicConfig(
        filename=f"../../logs/{log_type}.log",
        encoding="utf-8",
        filemode="a",
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        level=logging.WARNING,
    )

    return logging
