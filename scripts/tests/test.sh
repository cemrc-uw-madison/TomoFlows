#!/bin/bash
if [ "$1" == "update" ] 
then 
    if [ -d "TestData"]
    then 
        echo "Deleting old data..."
        rm -r TestData
        echo "Downloading latest data..."    
        wget https://cemrcstatic.blob.core.windows.net/cryoet-tomoflows/TestData.tar
        tar -xvf TestData.tar
        rm TestData.tar
        echo "Test data exists, run unit tests..."
        pytest test_task_gain.py
    fi
else
    if [ -d "TestData" ]
    then
        echo "Test data exists, run unit tests..."
        pytest test_task_gain.py 
    else
        echo "Test data not exists, download begins..."
        wget https://cemrcstatic.blob.core.windows.net/cryoet-tomoflows/TestData.tar
        tar -xvf TestData.tar
        rm TestData.tar
        echo "Test data exists, run unit tests..."
        pytest test_task_gain.py
    fi
fi