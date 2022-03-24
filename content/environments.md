# Recording environments

```{questions}
  - How to capture the software environment of a computational experiment?
```

```{instructor-note}
- 15 min teaching
- 0 min exercises
```

## Containers

- Containers can be built to bundle *all the necessary ingredients* (data, code, environment).
- A container provides operating-system-level virtualization, sharing the host system’s kernel with other containers.
- Popular container implementations are [Docker](https://www.docker.com/) and [Singularity](http://singularity.lbl.gov/).


### Docker

- Available for most common operating systems.
- A mechanism to "send the computer to the data" when data is too
  large or too sensitive to travel over network.
- [DockerHub](https://hub.docker.com/) is a platform to share Docker images (stored in repositories - similar to a Git repository).
- Public Docker images available on [DockerHub](https://hub.docker.com/).
- A docker container is like a piece of paper with all the operating system on it. When you run it,
a transparent sheet is placed on top to form a container. The container runs and writes only on
that transparent sheet (and what other mounts have been layered on top). When you are done,
transparency is thrown away. It can be repeated as often as you want, and base is always the same.

```{danger}
Use only official and trusted images!
Not all images can be trusted! There have been examples of contaminated
images so investigate before using images blindly. Apply same caution as installing
software packages from untrusted package repositories.
```

#### Examples of useful Docker images

1. Run a specific version of *Rstudio* 
   ```shell
   docker run --rm -p 8787:8787 -e PASSWORD=yourpasswordhere rocker/rstudio
   ```

   Then open your browser to
   [http://localhost:8787](http://localhost:8787) with login rstudio
   and password "yourpasswordhere" used in the previous command.  If
   you want to try an older version you can check the tags at
   [https://hub.docker.com/r/rocker/rstudio/tags](https://hub.docker.com/r/rocker/rstudio/tags)
   and run for example

   ```shell
   docker run --rm -p 8787:8787 -e PASSWORD=yourpasswordhere rocker/rstudio:3.3
   ```

2. Run a specific version of *Anaconda3* from
   [https://hub.docker.com/r/continuumio/anaconda3](https://hub.docker.com/r/continuumio/anaconda3)

   ```shell
   docker run -i -t continuumio/anaconda3 /bin/bash
   ```

   and similarly one can also pick an image for *Anaconda2* at
   [https://hub.docker.com/r/continuumio/anaconda2/tags](https://hub.docker.com/r/continuumio/anaconda2/tags)


### Singularity

- [Singularity](http://singularity.lbl.gov/) is aimed at scientific community and to run scientific workflows on HPC resources.
- Docker images can be converted into Singularity images.

---

## Container vs. image vs. recipe (Dockerfile)

- Image is like a blueprint. It is immutable.
- Container is an instance of an image.
- Dockerfile is a recipe which creates a container based on an image and applies small changes to it.

---

## Pros and cons of containers

Containers are popular for a reason - they solve a number of
important problems:
- Allow for seamlessly moving workflows across different platforms.
- Much more lightweight than virtual machines.
- Eliminates the "works on my machine" situation.
- For software with many dependencies, in turn with its own dependencies,
  containers offer possibly the only way to preserve the
  computational experiment for future reproducibility.

However, containers may also have some drawbacks:
- Containers can have security vulnerabilities which can be exploited.
- Can be used to hide away software installation problems and thereby
  discourage good software development practices.
- It may not be clear whether to record the environment in the image part or the recipe part.


```{discussion} Reproducibility aspects of container images
- Do you think containers contribute to reproducible research?
- Do you see a use case for your own work?
```

---
## Exercise - Play with Docker

`````{exercise} (Optional) Environment-1: Play with Docker
1. This exercise requires a DockerHub account. You can sign up on [https://hub.docker.com/signup](https://hub.docker.com/signup).
2. Go to [Play with Docker](https://labs.play-with-docker.com/) and log in using 
   your DockerHub account. 
3. Click on "Add new instance" - you now have a free Alpine Linux Virtual Machine in browser where you can build and run Docker containers
4. Pull the hello-world image from DockerHub:
   ```shell
   docker pull hello-world
   ```
5. List local images:
   ```shell
   docker image ls
   ```
6. Now create a new container from the image and run it:
   ```shell
   docker run hello-world
   ```  
   This should output "Hello from Docker!" followed by a description of what just happened:
   ```shell
   1. The Docker client contacted the Docker daemon.
   2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
      (amd64)
   3. The Docker daemon created a new container from that image which runs the
      executable that produces the output you are currently reading.
   4. The Docker daemon streamed that output to the Docker client, which sent it
      to your terminal.
   ```
7. The hello-world image can't do much more than this. For a more interesting 
   challenge, we can run bash in interactive mode using the ubuntu image from DockerHub. The following command automatically pulls the image before creating the container:
   ```shell
   docker run -it ubuntu bash
   ```
   Notice that the command prompt changed - we are now "inside" a live container. We can double-check that we're indeed in an Ubuntu environment:
   ```shell
   cat /etc/os-release
   ```
8. Exit the container by typing `exit`.
9. Challenge: run an ubuntu container and make it print "Hello from Ubuntu!".

````{solution}
We use `docker run ubuntu` to run a container from the ubuntu image, and give
it the command `echo "Hello from Ubuntu!"`:
```shell
docker run ubuntu echo "Hello from Ubuntu!"
```
````
`````
