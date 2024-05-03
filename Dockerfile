# base image  
FROM nvidia/cuda:12.4.1-devel-rockylinux9
RUN dnf update -y
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

# Install common dependencies
RUN dnf -y install wget
RUN dnf -y install python3
RUN dnf -y install python3-pip
RUN dnf -y install libjpeg-turbo-devel libtiff-devel libjpeg-devel fftw-devel
RUN dnf -y install gcc gcc-c++ openmpi-devel mpich cmake git

# Import NVIDIA CUDA repository keyring
RUN curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/rhel9/x86_64/cuda-rhel9.repo | tee /etc/yum.repos.d/cuda.repo

# Install the CUDA keyring package
RUN rpm --import https://developer.download.nvidia.com/compute/cuda/repos/rhel9/x86_64/D42D0685.pub

# Install the CUDA Toolkit and development files 
RUN dnf install -y cuda

# Install IMOD 
RUN wget http://bio3d.colorado.edu/imod/AMD64-RHEL5/imod_4.11.24_RHEL7-64_CUDA10.1.sh
RUN chmod +x imod_4.11.24_RHEL7-64_CUDA10.1.sh
#RUN dnf -y install openssh-client
#RUN dnf -y install libjpeg62
#RUN dnf -y install libjpeg-dev
#RUN dnf -y install default-jre
#RUN dnf -y install libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxkbcommon-x11-0
RUN dnf -y install openssh-clients
RUN dnf -y install java-1.8.0-openjdk
RUN dnf -y install libxcb-devel libX11-xcb libXScrnSaver libxkbcommon-x11
RUN sh imod_4.11.24_RHEL7-64_CUDA10.1.sh -debian -y
ENV IMOD_DIR=/usr/local/imod_4.11.24
RUN echo 'export IMOD_DIR="/usr/local/imod_4.11.24/"' >> /etc/bash.bashrc
RUN echo 'export PATH="${IMOD_DIR}/bin:$PATH"' >> /etc/bash.bashrc
RUN source /etc/bashrc

# Download and build MotionCor3
RUN git clone https://github.com/czimaginginstitute/MotionCor3.git
WORKDIR $DjangoDir/MotionCor3/LibSrc/Mrcfile
RUN make
WORKDIR $DjangoDir/MotionCor3/LibSrc/Util
RUN make
WORKDIR $DjangoDir/MotionCor3
RUN echo 'export PATH="/usr/local/cuda-12.4/bin:$PATH"' >> /etc/bash.bashrc
RUN source /etc/bash.bashrc
RUN make exe -f makefile11 CUDAHOME=/usr/local/cuda-12.4
RUN mv MotionCor3 ../MotionCor3Binary
WORKDIR $DjangoDir
RUN rm -rf MotionCor3/
RUN mv MotionCor3Binary /usr/local/bin/motioncor3
RUN source /etc/bash.bashrc

# Download and build AreTomo2
RUN git clone https://github.com/czimaginginstitute/AreTomo2.git
WORKDIR $DjangoDir/AreTomo2
RUN make exe -f makefile11 CUDAHOME=/usr/local/cuda-12.4
RUN mv AreTomo2 ../AreTomo2Binary
WORKDIR $DjangoDir
RUN rm -rf MotionCor3/
RUN mv AreTomo2Binary /usr/local/bin/aretomo2
RUN source /etc/bash.bashrc

# pip
RUN pip3 install --upgrade pip
COPY . $DjangoDir
WORKDIR $DjangoDir
RUN pip3 install -r requirements.txt

# start application
WORKDIR $DjangoDir
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py loaddata tasks
EXPOSE 8000
CMD python3 manage.py runserver 0.0.0.0:8000
