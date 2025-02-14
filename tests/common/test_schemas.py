import pytest
from pydantic import ValidationError

from common.schemas import Message
from ..helper.load_test_data import load_test_data


@pytest.mark.parametrize("test_data", load_test_data("test_schema"))
def test_message(test_data):
    if type(test_data['input']['sender']) and isinstance(test_data['input']['message'], str):
        msg = Message(sender=test_data['input']['sender'], message=test_data['input']['message'])
        assert msg.sender == test_data['expected']['sender']
        assert msg.message == test_data['expected']['message']
    else:
        with pytest.raises(ValidationError):
            Message(**test_data)
