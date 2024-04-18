# base image  
FROM nikolaik/python-nodejs:python3.10-nodejs18
RUN apt-get update
RUN apt-get upgrade -y
SHELL ["/bin/bash", "-c"] 

# set environment variables and work directory
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DjangoDir=/home/tomoflows
ENV ReactDir=/home/tomoflows/frontend
ENV DataDir=/home/tomoflows/data
RUN mkdir -p $DjangoDir
RUN mkdir -p $DataDir
WORKDIR $DjangoDir

# install dependencies

# imod
RUN wget http://bio3d.colorado.edu/imod/AMD64-RHEL5/imod_4.11.24_RHEL7-64_CUDA10.1.sh
RUN chmod +x imod_4.11.24_RHEL7-64_CUDA10.1.sh
# RUN echo 'deb http://ftp.debian.org/debian buster-backports main' | tee /etc/apt/sources.list.d/buster-backports.list
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get -y install openssh-client
RUN apt-get -y install libjpeg62
RUN apt-get -y install libjpeg-dev
RUN apt-get -y install default-jre
RUN apt-get -y install libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxkbcommon-x11-0
RUN sh imod_4.11.24_RHEL7-64_CUDA10.1.sh -debian -y
RUN source /etc/bash.bashrc

# cuda
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/debian12/x86_64/cuda-keyring_1.1-1_all.deb
RUN dpkg -i cuda-keyring_1.1-1_all.deb
RUN apt-get -y install software-properties-common
RUN add-apt-repository contrib -y
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get -y install cuda-toolkit-12-4
RUN source /etc/bash.bashrc

# motioncor3
RUN git clone https://github.com/czimaginginstitute/MotionCor3.git
WORKDIR $DjangoDir/MotionCor3/LibSrc/Mrcfile
RUN make
WORKDIR $DjangoDir/MotionCor3/LibSrc/Util
RUN make
WORKDIR $DjangoDir/MotionCor3
RUN ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/local/cuda/lib64/stubs/libcuda.so.1
RUN echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64/stubs/:$LD_LIBRARY_PATH' >> /etc/bash.bashrc
RUN echo 'export PATH="/usr/local/cuda-12.4/bin:$PATH"' >> /etc/bash.bashrc
RUN source /etc/bash.bashrc
RUN make exe -f makefile11 CUDAHOME=/usr/local/cuda-12.4
RUN mv MotionCor3 ../MotionCor3Binary
WORKDIR $DjangoDir
RUN rm -rf MotionCor3/
RUN mv MotionCor3Binary /usr/local/bin/motioncor3
RUN source /etc/bash.bashrc

# pip
RUN pip install --upgrade pip
COPY . $DjangoDir
RUN pip install -r requirements.txt

# start application
WORKDIR $DjangoDir
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py loaddata tasks
EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000
