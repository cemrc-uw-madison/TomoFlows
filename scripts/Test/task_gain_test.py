import pytest
from program.task_gain import TaskGain
import os


def test_input_image_type():
    """
    Test if user provide correct input file format: dm
    """
    task_gain = TaskGain("sample.dm4")
    assert task_gain.input_file.split('.')[-1] == 'dm4'


def test_exception_wrong_type():
    """
    Test if program raise correct exception message when provided
    with wrong image format
    """

    with pytest.raises(ValueError) as exc_info:
        task_gain = TaskGain("sample.jpg")

    exception_raised = exc_info.value
    assert exception_raised.args[0] == "Input image format must be dm4!"


def test_output_file_name():
    """
    Test if program create correct output file name
    """
    task_gain = TaskGain("sample.dm4")
    assert task_gain.output_file == "sample.mrc"


def test_output_image_type():
    """
    Test if program generate correct output image
    """
    task_gain = TaskGain("K3-GAT21320024GainRef.dm4")
    if os.path.exists("K3-GAT21320024GainRef.mrc"):
        os.remove("K3-GAT21320024GainRef.mrc")
    if os.path.exists("shrink.mrc"):
        os.remove("shrink.mrc")
    task_gain.run("shrink.mrc")
    assert os.path.exists("shrink.mrc")
    assert not os.path.exists("K3-GAT21320024GainRef.mrc")
    with open("shrink.mrc", "rb") as f_shrink, open("K3-GAT21320024GainRef.dm4", "rb") as f_origin:
        assert len(f_origin.read()) - 4*len(f_shrink.read()) < 1024*1024