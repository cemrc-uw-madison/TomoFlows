import pytest
import sys
import os
# Get access of file inside script program
absolute_path = os.path.dirname(__file__)

absolute_list = absolute_path.split("/")
absolute_list[-1] = "program/"
sys.path.append("/".join(absolute_list))
from task_gain import TaskGain


test_type = "Gain"
delimiter = "/"
test_data_path = os.path.dirname(__file__) + delimiter + "TestData" + delimiter + test_type + delimiter
test_data_dir = os.listdir(test_data_path)
for test in test_data_dir:
    print(os.listdir(test_data_path + test))
def test_input_image_type():
    """
    Test if user provide correct input file format: dm4
    """
    task_gain1 = TaskGain("sample.dm4")
    task_gain2 = TaskGain("K3-GAT21320024GainRef.x1.m3.dm4")
    assert task_gain1.input_file.split('.')[-1] == 'dm4'
    assert task_gain2.input_file.split('.')[-1] == 'dm4'

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
    with open("K3-GAT21320024GainRef-Shrink.mrc", "rb") as f_shrink, open("K3-GAT21320024GainRef.dm4", "rb") as f_origin:
        assert len(f_origin.read()) - 4*len(f_shrink.read()) < 1024*1024