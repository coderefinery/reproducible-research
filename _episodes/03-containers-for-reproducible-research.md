---
layout: episode
title: "Containers for reproducible research"
teaching: 15
exercises: 10
questions:
  - "How do you communicate different versions of dependencies you need?" 
  - "How to capture environments under which experiment was made?"
objectives:
  - "Get a basic idea of using containers to capture research environments"
  - "You can incorporate some of these tools in your research lifecycle"
 
---

# Containers

- Containers can be seen as a 'ready-to-eat' software. 
- Containers can be built to bundle all the necessary ingredients (data, code, environment).
- A standardized unit of software
- A great solution to the problem of "dependency hell"
- Allows for seamlessly moving workflows across different platforms
- A container provides operating-system-level virtualization. Container technology allows multiple isolated user space instances to be run on a single host.
- Popular container implementations are Docker and Singularity

## Docker
- Docker provides containerization in software level
- Available for most common operating systems, and also some clouds: AWS, Azure
- Provides an easy and fast way to bundle all the necessary libraries and data together
- Docker Hub - A platform to share docker images (Note: images are stored in repositories ~ similar to git repository)
- Public Docker images available in [Docker Hub](https://hub.docker.com/) but a word of warning: <span style="color: red">not all images can be trusted! There have been examples of contaminated images so investigate before using images blindly</span>.
- [ ] Example  

---

## What aspects of containers would we like to communicate?


## Docker fundamentals
- Docker provides operating-system-level virtualization
- Docker is a client server application. The Docker client talks to the Docker server
or daemon, which, in turn, does all the work.

<img src="/reproducible-research/img/docker_architecture.svg" style="height: 400px;"/>

- Docker client
   - End user uses docker client to communicate with docker engine 
- Docker daemon
   - Executes the commands sent to the docker client. It manages containers, images, builds, etc. <!--The Docker daemon (dockerd) listens for Docker API requests and manages Docker objects such as images, containers, networks, and volumes.--> 
- Docker registry
   - Stores Docker images. Docker Hub and Docker Cloud are public registries that anyone can use, and Docker is configured to look for images on Docker Hub by default. You can even run your own private registry. 


## What is a docker image
- A container image is a lightweight, stand-alone, executable package of a piece of software that includes everything needed to run it: code, runtime, system tools, system libraries, settings.
- A Docker image is made up of filesystems layered over each other. Docker calls each of these filesystems images.
- Listing docker images
  ```bash
  docker images
  ```
- Searching docker images from Dockerhub
  ```bash
  docker search ubuntu
  ```
- pulling from dockerhub
  ```bash
  docker pull ubuntu:16.04
  ```

## Building docker images
- An image is built based on the Dockerfile
- Dockerfile contains a series of instructions for building Docker images
<!-- - ```vim
     #version 0.0.1
     FROM ubuntu:16.04
     MAINTAINER Sri Harsha Vathsavayi "sriharsha.vathsavayi@csc.fi"
     RUN apt-get update
     ...
  ``` -->
- The Dockerfile contains a series of instructions paired with arguments
- We can build the image by running docker build in directory containing Dockerfile

<!--  ```bash
     docker build -t="vaths/nginx_test" .
  ``` 
 commands to use
  ```vim
   FROM
   RUN
   ADD
   COPY
   ENV
   VOLUME
   WORKDIR
   EXPOSE
   ..
  ```
 Let's create a simple webserver
```vim
     #version 0.0.1
     FROM ubuntu:16.04
     MAINTAINER Sri Harsha Vathsavayi "sriharsha.vathsavayi@csc.fi"
     RUN apt-get update
     RUN apt-get install -y nginx
     RUN echo 'I am inside container' >/var/www/html/index.html
     EXPOSE 80
  ``` -->
  

## creating containers from images
- running a container
<!--  ```bash
  docker run -d -p 80 --name my_webserver vaths/nginx_test
  ``` -->
- exposing ports
- volumes
- Note that Docker containers should be disposable: the data must be saved elsewhere

## Sharing a docker image
- dockerhub
- pushing to dockerhub
  ```bash
  docker login
  ```
<!--  ```bash
  docker push vaths/nginx_test
  ```  -->
- docker private registries

---
## singularity container (good to know)
- Singularity is aimed at scientific community and to run scientific workflows
- Docker is compatible with singularity, but the main purpose of docker is for micro services development and different than the purpose of singularity
- Docker is compatible with singularity, so docker images can be later converted into singularity images


