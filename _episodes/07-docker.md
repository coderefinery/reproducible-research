---
layout: episode
title: "(Optional) Creating and sharing a container image"
teaching: 10
exercises: 10

---

### Docker fundamentals

- Docker is a client-server application. The Docker client talks to the Docker server
or daemon, which, in turn, does all the work.

<img src="{{ site.baseurl }}/img/docker_architecture.svg" style="height: 400px;"/>

- Docker client
   - End user uses Docker client to communicate with Docker daemon .
- Docker daemon
   - Executes the commands sent to the Docker client. Manages containers, images, builds, etc.
- Docker registry
   - Stores Docker images. DockerHub and Docker Cloud are public registries that anyone can use, and Docker is configured to look for images on DockerHub by default.

---

### What are Docker images and containers

- A Docker *image* is executable package of a piece of software that includes everything needed to run it: code, runtime, system tools, system libraries, settings.
- When you start the image, you have a running *container* of this image.

---

### Docker commands

| Command  | Effect  |
| -------- | ------- |
| `docker help <command>` | Get help |
| `docker images` | List Docker images |
| `docker search ubuntu` | Search Docker images from DockerHub |
| `docker pull ubuntu` | Pull from DockerHub |
| `docker run -i -t ubuntu` | Start container from pulled image (-i keeps STDIN open, -t provides an interactive shell) |
| `docker ps` | Check running containers |
| `docker ps -a` | Check all containers (also those not running) |
| `docker stop container_id/name` | Stop the container |
| `docker start -i container_id/name` | Start (in interactive mode) a stopped container |
| `docker rm <container name>` | Remove a container |
| `docker rmi <image name>` | Remove an image |

---

### Building Docker images

- An image is built based on a Dockerfile.
- A Dockerfile contains a series of instructions paired with arguments.

```vim
#version 0.1
FROM ubuntu:16.04 (good to mention the image version being used)
LABEL maintainer="sriharsha.vathsavayi@csc.fi"
RUN apt-get update
...
```
Instructions in the Dockerfile (for full reference, please visit [Dockerfile](https://docs.docker.com/engine/reference/builder/)).

```vim
FROM -  sets the base image for subsequent instructions
RUN - execute any commands in a new layer on top of the current image and commit the results
COPY - copies local files from build context into our image
WORKDIR - provides a way to set the working directory for the container when a container is launched from the image
CMD -  specifies the command to run when a container is launched
LABEL - adds metadata to an image and is a key-value pair
..
..
```

> ## Mnemonics
>
> - The Dockerfile is like a cooking recipe, building an image from the
>   Dockerfile is like doing the actual cooking.
> - Running the Docker image to create a container doesn't have a good
>   cooking analogy, but:
>   - a Docker image is like a *class* in OOP, a Docker container is like an instance of the class.
{: .callout}

---

### Containerizing our workflow

> This exercise is based on the [same example project](https://github.com/coderefinery/word-count) as in the previous episodes.

> If you would like to type along but you don't have Docker installed, you 
> can log in to the ["Play with Docker Classroom"](https://training.play-with-docker.com/) which gives you access to Docker in the cloud.
> You can first click [Stage 1: The Basics](https://training.play-with-docker.com/ops-stage1)
> and then [Your First Linux Containers](https://training.play-with-docker.com/ops-s1-hello),
> and finally "Log in to access"

Let's create a Dockerfile for our example project.
It is available in the project repository if you want to experiment with
it later.

```vim
#version 0.1
FROM ubuntu:16.04

#maintainer information
LABEL maintainer="kthw@kth.se"

# update the apt package manager
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

# install make
RUN apt-get install -y build-essential

# install nano
RUN apt-get install -y nano

# install python
RUN apt-get install -y python3.6 python3.6-dev python3-pip python3.6-venv
RUN yes | pip3 install numpy
RUN yes | pip3 install matplotlib
RUN yes | pip3 install snakemake

# copy project to container
COPY ./ /opt/word_count/

# set work directory in container
WORKDIR /opt/word_count

# default command to execute when container starts
CMD /bin/bash
```

We can build the image by running docker build in the word_count directory containing Dockerfile:

```shell
$ docker build -t word_count:0.1 .
```
This will take a few minutes...

Check if the image is created:
```shell
$ docker images

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
word_count          0.1                 3103c7bde05b        4 minutes ago       744MB
ubuntu              16.04               7aa3602ab41e        3 weeks ago         115MB
```

- We now have two images, the *base image* `ubuntu:16.04` is the parent of our `word_count:0.1` image.

---

### Starting containers from images

We can run a container using `docker run` command:

```shell
$ docker run -i -t --name wordcount word_count:0.1
```
Note: Use -d to start a container in the background in a detached mode (to create long-running containers).

We can now see the running container (in another terminal):
```shell
$ docker ps
```

---

### Managing data

- Docker containers should be disposable - the data must be saved elsewhere.
- A Docker volume allows data to persist, even when a container is deleted. Volumes are also a convenient way to share data between the host and the container.
- For details on volumes, [refer to the documentation](https://docs.docker.com/engine/admin/volumes/) page.

**Sharing a host directory with container**

  ```shell
$ docker run -it --name my-directory-test -v <path-on-hostmachine>:/opt/data <image_name>
  ```

**Anyone with this image can reproduce the results we have generated**
  ```shell
$ docker run -v <path-on-hostmachine/results_directory>:/opt/word_count/results word_count:0.1 snakemake -s Snakefile_all
  ```
The `results_directory` folder will have the results of our word count example project.

We can also specify snakemake (or  any other command) as the default command to run when our container starts, by giving it as parameter for CMD in Dockerfile.

---

### Sharing a Docker image
- DockerHub - A platform to share Docker images.
- Login to DockerHub:

 ```shell
$ docker login
  ```
- Push to DockerHub. The image name has to be in **youruser/yourimage** format
(thus instead of the name `word_count`,
we should have used `<dockerhub-username>/word_count` above):

 ```shell
$ docker push image_name
  ```
- For proprietary/sensitive images private Docker registries can be used
