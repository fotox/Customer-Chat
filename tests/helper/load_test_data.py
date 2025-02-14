import json


def load_test_data(filename: str) -> dict:
    """
    Load test input and expected data from file.
    :param filename: name of input file
    :return: input and expected data
    """
    with open(f"tests/resources/{filename}.json", "r", encoding="utf-8") as f:
        return json.load(f)
