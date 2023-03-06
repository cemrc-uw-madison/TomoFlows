# base image  
FROM nikolaik/python-nodejs:python3.10-nodejs18

# set environment variables and work directory
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DjangoDir=/home/tomoflows
ENV ReactDir=/home/tomoflows/frontend
RUN mkdir -p $DjangoDir
WORKDIR $DjangoDir

# install dependencies
# RUN wget https://bio3d.colorado.edu/imod/AMD64-RHEL5/imod_4.11.24_RHEL7-64_CUDA10.1.sh
# RUN ./imod_4.11.24_RHEL7-64_CUDA10.1.sh
# 
RUN pip install --upgrade pip
COPY . $DjangoDir
RUN pip install -r requirements.txt
WORKDIR $ReactDir
RUN npm install
RUN npm run build
WORKDIR $DjangoDir
RUN python manage.py makemigrations
RUN python manage.py migrate

# start application
EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000
