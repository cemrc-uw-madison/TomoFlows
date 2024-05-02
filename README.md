![tomoflows](Documentation/Design/img/TomoFlows_Logo.png)

# TomoFlows

TomoFlows is a web-based UI for a task-based processing pipeline for Cryo-EM tomographic dataflows, intended for facility and independent users.

![tomoflows](Documentation/Design/img/TomoFlows_Available_Tasks_UI.png)

See [Design Documentation](scripts/Documentation/Design/index.md)

Ideally, TomoFlows would be installed on a Linux server or workstation with available NVIDIA GPUs (NVIDIA GTX 1080 or newer generations of GPU supported by CUDA).

## Running on Docker
1. Install Docker: See [Docker Documentation](https://docs.docker.com/get-docker/). Full functionality for this application requires a CUDA compatible NVIDIA GPU, and Docker to be configured with GPU support.

### Docker with GPU support
These instructions are for CentOS Linux environments.

Install NVIDIA Drivers > 550.54.15, with CUDA 12.4 support.

See instructions here [CentOS Docker Documentation](https://docs.docker.com/engine/install/centos/).

1. Add the official Docker repository

2. Install the `docker-ce`, `docker-ce-cli`, `containerd.io`, and `docker-compose-plugin` packages.
  `dnf install docker-ce docker-ce-cli containerd.io docker-compose-plugin`

3. Install the `nvidia-container-toolkit` package
  `dnf install nvidia-container-toolkit`

4. Setup the configuration of Docker to use the container runtime. Edit a file `/etc/docker/daemon.json` to include this configuration:

 ```
             {
                 "default-runtime": "nvidia",
                 "runtimes": {
                     "nvidia": {
                         "path": "/usr/bin/nvidia-container-runtime",
                         "runtimeArgs": []
                     }
                 }
             }

 ```

5. Start and enable the Docker service
 `sudo systemctl start dockerd`
 `sudo systemctl enable dockerd`

6. Add your user to the `docker` group if you want to run this non-root.

 `sudo usermod -aG docker <user>`

### Docker Desktop
If you are using Docker Desktop, you should allow paths to be used by containers, see "Preferences > Resources > File Sharing" in Docker Desktop to include `/tmp`

### Build an image and run with docker compose
3. Navigate to `frontend` and build React files with `npm install && npm run build`
2. Build Docker Image: `docker build . -t tomoflows-img`
3. Run Docker Container: `docker compose up -d` (remove -d to attach container to terminal and not run in background)
4. Open Browser and visit `http://localhost:8000`
5. Connect to container shell: `docker compose exec tomoflows bash` (OPTIONAL)
7. Stop and Remove Container: `docker compose down` (OPTIONAL)
6. Kill Container: `docker compose kill` (OPTIONAL)

> NOTE: important note - not all tasks/software packages are currently available in the containerized version, and the Dockerfile and instructions will need to be updated to support all tasks. For full use, the section below for a development environment should instead be followed. 

### NVIDIA GPU Passthrough with Docker on Linux
Verify your setup.

You can check that your Docker supports running NVIDIA GPUs with the sample YAML configuration provided:

`cd nvidia_gpu_docker`
`docker compose up`

```
docker compose up
[+] Running 1/0
 ✔ Container nvidia_gpu_docker-gpu-test-1  Created                                                     0.0s 
Attaching to gpu-test-1
gpu-test-1  | ==========
gpu-test-1  | == CUDA ==
gpu-test-1  | ==========
gpu-test-1  | 
gpu-test-1  | CUDA Version 12.4.1
gpu-test-1  | 
gpu-test-1  | Container image Copyright (c) 2016-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
gpu-test-1  | 
gpu-test-1  | Wed May  1 18:41:30 2024       
gpu-test-1  | +-----------------------------------------------------------------------------------------+
gpu-test-1  | | NVIDIA-SMI 550.54.15              Driver Version: 550.54.15      CUDA Version: 12.4     |
gpu-test-1  | |-----------------------------------------+------------------------+----------------------+
gpu-test-1  | | GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
gpu-test-1  | | Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
gpu-test-1  | |                                         |                        |               MIG M. |
gpu-test-1  | |=========================================+========================+======================|
gpu-test-1  | |   0  NVIDIA RTX A4000               Off |   00000000:09:00.0 Off |                  Off |
gpu-test-1  | | 41%   33C    P8              7W /  140W |     471MiB /  16376MiB |      0%      Default |
gpu-test-1  | |                                         |                        |                  N/A |
gpu-test-1  | +-----------------------------------------+------------------------+----------------------+
gpu-test-1  |                                                                                          
gpu-test-1  | +-----------------------------------------------------------------------------------------+
gpu-test-1  | | Processes:                                                                              |
gpu-test-1  | |  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
gpu-test-1  | |        ID   ID                                                               Usage      |
gpu-test-1  | |=========================================================================================|
gpu-test-1  | +-----------------------------------------------------------------------------------------+
gpu-test-1 exited with code 0
```

Otherwise, if the Docker environment is not working, you may see an error like:

```
[+] Running 0/1
 ⠙ Container  Starting                              0.2s 
Error response from daemon: could not select device driver "nvidia" with capabilities: [[gpu]]
```

If you get an error like this, check that NVIDIA drivers are working on your system, that the nvidia-container-tools are installed, and that Docker is properly configured for NVIDIA GPU support (see above).

## Local Development and non-docker use

### Software environment

Third-party software to be installed and available in your PATH:

- IMOD (version 4.11.24 or higher)
- UCSF MotionCor2 (version 1.5.0+ or higher)
- UCSF AreTomo (version 1.3+)
- gCTF (version 1.06+)

### Virtualenv Setup

1. Create virtual env: `python3 -m virtualenv ~/path/to/env`
2. Activate virtual env: `source ~/path/to/env/bin/activate`
3. Install requirements: `pip install -r requirements.txt`

### Run Development Server

1. Ensure to setup and activate virtualenv and install dependencies
2. Run Django Migrations: `python3 manage.py makemigrations && python3 manage.py migrate`
3. Populate database with tasks: `python3 manage.py loaddata tasks`
3. Start Django Server: `python3 manage.py runserver`
4. Setup Frontend in New Terminal: `cd frontend && npm install`
5. Run Frontend in New Terminal: `npm run dev`

