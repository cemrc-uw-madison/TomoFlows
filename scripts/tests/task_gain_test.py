import pytest
from program.task_gain import TaskGain


def test_check_input_image_type():
    """
    Test if user provide correct input file format: dm
    """
    task_gain = TaskGain("sample.dm4")
    assert task_gain.input_file.split('.')[-1] == 'dm4'


def test_check_exception_wrong_type():
    """
    Test if program raise correct exception message when provided
    with wrong image format
    :return:
    """

    with pytest.raises(ValueError) as exc_info:
        task_gain = TaskGain("sample.jpg")

    exception_raised = exc_info.value
    assert exception_raised.args[0] == "Input image format must be dm4!"


def test_check_output_image_type():
    """
    Test if program generate correct
    """
