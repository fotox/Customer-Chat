import json
import os
import pathlib


def load_test_data(filename: str) -> dict:
    """
    Load test input and expected data from file.
    :param filename: name of input file
    :return: input and expected data
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    resource_dir = os.path.join(base_dir, "..", "resources", f"{filename}.json")

    with open(resource_dir, "r", encoding="utf-8") as f:
        return json.load(f)
