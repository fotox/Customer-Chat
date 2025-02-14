import logging
import os


def __init_log_module(log_type: str) -> logging.Logger:
    """
    Initialize the logging module
    :return: logging module.
    """
    log_dir = "logs"
    log_file_path = f"{log_dir}/{log_type}.log"
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        filename=log_file_path,
        encoding="utf-8",
        filemode="a",
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        level=logging.WARNING,
    )

    return logging.getLogger(log_type)
