import typing
import subprocess
import os
from program.task import Task

class FlowProject():
    """ Project is an overall holder of tasks and overall descriptive metadata """

    def toDisk():
        ''' serialize to a folder, with associated metadata files '''

    def parse(path_to_folder):
        ''' create an instance of Project from reading from disk '''

    ## Methods to query the project
    # get Next job index?
    # get List of jobs in this project?
    # get Descriptions/header information for the project?
    # setters for above...
