import pytest
import logging
import os

from log_module import __init_log_module


def test_init_log_module_creates_logger():
    log_type = "test_log"
    logger = __init_log_module(log_type)

    assert isinstance(logger, logging.Logger)
    assert logger.level == 0  # Warning
    assert logger.name == log_type


def test_init_log_module_creates_log_file():
    log_type = "test_log"
    log_dir = "logs"
    log_file_path = f"{log_dir}/{log_type}.log"

    __init_log_module(log_type)

    assert os.path.exists(log_file_path)

    os.remove(log_file_path)
    os.rmdir(log_dir)


def test_init_log_module_invalid_log_type():
    with pytest.raises(TypeError):
        __init_log_module(None)


def test_init_log_module_empty_log_type():
    with pytest.raises(ValueError):
        __init_log_module("")


def test_init_log_module_non_string_log_type():
    with pytest.raises(TypeError):
        __init_log_module(123)


def test_init_log_module_invalid_directory():
    invalid_path = "/invalid_path/test_log"
    with pytest.raises(OSError):
        __init_log_module(invalid_path)
