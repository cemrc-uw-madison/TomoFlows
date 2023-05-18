#!/bin/bash
if [ -d "TestData" ]
then
    echo "Test data exists, run unit tests"
    python3 
else
    echo "Test data not exists, download begins"
    wget https://cemrcstatic.blob.core.windows.net/cryoet-tomoflows/TestData.tar
    tar -xvf TestData.tar
    rm TestData.tar
fi