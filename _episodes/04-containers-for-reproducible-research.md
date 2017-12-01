---
layout: episode
title: "Containers for reproducible research"
teaching: 10
exercises: 15
questions:
   - "How to capture the environment under which experiment was made?"
   - "How do you communicate different versions of dependencies you need?" 
objectives:
  - "Get a basic idea of using containers to capture research environments"
 
---

# Containers

- Containers can be seen as a 'ready-to-eat' software
- Containers can be built to bundle all the necessary ingredients (data, code, environment)
- A great solution to the problem of "dependency hell"
- Allows for seamlessly moving workflows across different platforms
- A container provides operating-system-level virtualization, i.e., it shares  the host system’s kernel with other containers
- Popular container implementations are **Docker** and **Singularity**

## Docker
- Docker provides containerization in software level
- Available for most common operating systems
- Provides an easy and fast way to bundle all the necessary libraries and data together
- Docker Hub - A platform to share docker images (Note: images are stored in repositories ~ similar to git repository)
- Public Docker images available in [Docker Hub](https://hub.docker.com/) but a word of warning: <span style="color: red">not all images can be trusted! There have been examples of contaminated images so investigate before using images blindly</span>.

---

## Docker fundamentals
- Docker is a client server application. The Docker client talks to the Docker server
or daemon, which, in turn, does all the work.

<img src="/reproducible-research/img/docker_architecture.svg" style="height: 400px;"/>

- Docker client
   - End user uses docker client to communicate with docker engine 
- Docker daemon
   - Executes the commands sent to the docker client. It manages containers, images, builds, etc. <!--The Docker daemon (dockerd) listens for Docker API requests and manages Docker objects such as images, containers, networks, and volumes.--> 
- Docker registry
   - Stores Docker images. Docker Hub and Docker Cloud are public registries that anyone can use, and Docker is configured to look for images on Docker Hub by default.
   - You can even run your own private registry


## What is a docker image
- A container image is executable package of a piece of software that includes everything needed to run it: code, runtime, system tools, system libraries, settings
- A Docker image is made up of filesystems layered over each other <!--Docker calls each of these filesystems images.-->

Listing docker images
  ```bash
  docker images
  ```
Searching docker images from Dockerhub
  ```bash
  docker search ubuntu
  ```
Pulling from dockerhub <!-- (if no tag is mentioned pulls the latest one by default) -->
  ```bash
  docker pull ubuntu
  ```
Starting container from the pulled image
  ```bash
  docker run -i -t ubuntu
  
  -i flag keeps STDIN open from the container
  -t flag provides an interactive shell to the container
  ```
   
Check running containers
  ```bash
  docker ps
  ```
Stop the container
  ```bash
  docker stop container_id or name
  ```
## Building docker images
- An image is built based on the Dockerfile
- The Dockerfile contains a series of instructions paired with arguments

```vim
     #version 0.0.1
     FROM ubuntu:16.04 (good to mention the image version being used)
     MAINTAINER Sri Harsha Vathsavayi "sriharsha.vathsavayi@csc.fi"
     RUN apt-get update
     ...
  ```
Instructions in the Dockerfile (for full reference, please visit [Dockerfile](https://docs.docker.com/engine/reference/builder/) )

```vim
   FROM -  sets the base image for subsequent instructions
   RUN - execute any commands in a new layer on top of the current image and commit the results
   COPY - copies local files from build context into our image
   WORKDIR - provides a way to set the working directory for the container when a container is launched from the image
   CMD -  specifies the command to run when a container is launched
   ..
   ..
  ```
  
Let's create a Dockerfile for our example project
```vim
     #version 0.0.1
     FROM ubuntu:16.04
     MAINTAINER Your name "email address"
     
     # update the apt package manager
     RUN apt-get update     
  
     # install python
     RUN apt-get install -y python
  
     # install make
     RUN apt-get install -y build-essential
  
     # copy project to container 
     COPY ./ /opt/character_count/
  
     # set work directory in container
     WORKDIR /opt/character_count
  
     # default command to execute when container starts 
     CMD ["/bin/bash"]
  ```

At this point, our project directory will be like this:
```bash
character_count/
|-- data/
|   |--readme.txt
|   |--shakespeare.in
|-- manuscript                           
|-- results/
|   |--format-data.tmp
|   |--format-data.out
|-- source/
|   |--count.py
|   |--plot.py
|--Makefile
|--Dockerfile
```
  
We can build the image by running docker build in the character_count directory containing Dockerfile 

 ```bash
     docker build -t <dockerhub-username>/character_count:0.0.1 .
  ``` 

Check if the image is created
 ```bash
     docker images
  ``` 

## Starting containers from images
We can run a container using `docker run` command

```bash
docker run -i -t --name wordscount image_name 
``` 
Note: Use -d to start a container in the background in a detached mode (to create long-running containers)

**Anyone with this image can reproduce the results we have generated**

<!--
  ```bash
  docker run -d -p 80:80 --name my_webserver vaths/nginx_test
  ```
The -p flag manages which network ports Docker exposes at runtime. 
    - Docker can randomly assign a high port from the range 49000 to 49900 on the Docker host that maps to port 80 on the container.
    - We can specify a specific port on the Docker host that maps to port 80 on the container.
-->

---
## Managing data
- Note that Docker containers should be disposable: the data must be saved elsewhere
- A volume allows data to persist, even when a container is deleted. Volumes are also a convenient way to share data between the host and the container.
- For details on volumes, please visit [docker volumes](https://docs.docker.com/engine/admin/volumes/) page

**sharing a host directory with container**
 
  ```bash
  docker run -it --name my-directory-test -v <path-on-hostmachine>:/opt/data wordscount
  ```

## Sharing a docker image
- Docker Hub - A platform to share docker images
- Login to dockerhub

 ```bash
  docker login
  ```
- Push to dockerhub. The image name has to be in **youruser/yourimage** format. 

 ```bash
  docker push image_name
  ```
- For proprietary/sensitive images private Docker registries can be used

---
## Singularity container (good to know)
- Singularity is aimed at scientific community and to run scientific workflows
- Docker is compatible with singularity, but the main purpose of docker is for micro services development and different than the purpose of singularity
- Docker is compatible with singularity, so docker images can be later converted into singularity images


