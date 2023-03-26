# Recording environments

```{objectives}
- Understand what containers are
- Understand good and less good usecases for containers
- Discuss container definitions files in the context of reusability and
  reproducibility
```

```{instructor-note}
- 10 min teaching/discussion
- 20 min exercise
```

Imagine if you didn't have to install things yourself, but instead you could
get a computer with the exact software for a task pre-installed?  Containers
effectively do that, with various advantages and disadvantages.  They are
**like an entire operating system with software installed, all in one file**, 

```{figure} img/docker_meme.jpg
:alt: He said, then we will ship your machine. And that's how Docker was born.
:width: 60%

From [reddit](https://www.reddit.com/r/ProgrammerHumor/comments/cw58z7/it_works_on_my_machine/).
```

```{discussion} Cooking recipe analogy
- Our codes/scripts <-> cooking recipes
- Container definition files <-> like a blueprint to build a kitchen with all
  utensils in which the recipe can be prepared.
- Container images <-> example kitchens
- Containers <-> kitchens that are copies of example kitchens

(here we will add some images)
```


## From definition files to container images to containers

- Containers can be built to bundle *all the necessary ingredients* (data, code, environment, operating system).
- A container image is like a piece of paper with all the operating system on it. When you run it,
  a transparent sheet is placed on top to form a container. The container runs and writes only on
  that transparent sheet (and what other mounts have been layered on top). When you are done,
  transparency is thrown away. It can be repeated as often as you want, and base is always the same.
- Definition files (e.g. Dockerfile or Singularity definition file) are text
  files that contain a series of instructions to build container images.

Here is an example of a Singularity definition file ([reference](https://apptainer.org/docs/user/main/build_a_container.html#building-containers-from-apptainer-definition-files)):
```txt
Bootstrap: docker
From: ubuntu:20.04

%post
    apt-get -y update
    apt-get -y install cowsay lolcat

%environment
    export LC_ALL=C
    export PATH=/usr/games:$PATH

%runscript
    date | cowsay | lolcat
```

Popular container implementations:
- [Docker](https://www.docker.com/)
- [Singularity](https://sylabs.io/docs/) (popular on high-performance computing systems)
- [Apptainer](https://apptainer.org) (popular on high-performance computing systems, fork of Singularity)
- [podman](https://podman.io/)

They are to some extent interoperable:
- podman is very close to Docker
- Docker images can be converted to Singularity/Apptainer images

---

## Pros and cons of containers

Containers are popular for a reason - they solve a number of
important problems:
- Allow for seamlessly moving workflows across different platforms.
- Can solve the "works on my machine" situation.
- For software with many dependencies, in turn with its own dependencies,
  containers offer possibly the only way to preserve the
  computational experiment for future reproducibility.
- A mechanism to "send the computer to the data" when data is too
- Installing software into a file instead of into your computer (removing
  a file is often easier than uninstalling software if you suddenly regret an
  installation)

However, containers may also have some drawbacks:
- Can be used to hide away software installation problems and thereby
  discourage good software development practices.
- Instead of "works on my machine" problem: "works only in this container" problem?
- They can be difficult to modify (this is the focus of an exercise below)
- Container images can become large

```{danger}
Use only official and trusted images!  Not all images can be trusted! There
have been examples of contaminated images so investigate before using images
blindly. Apply same caution as installing software packages from untrusted
package repositories.
```

---

## Where can one share or find images?

- [Docker Hub](https://hub.docker.com/)
- [Quay](https://quay.io/)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [GitLab Container Registry](https://docs.gitlab.com/ee/user/packages/container_registry/)
- GitHub/GitLab release artifacts
- [Zenodo](https://zenodo.org/)

---

## Exercises

````{exercise} Containers-1: under construction ...
work in progress ...
````

````{exercise} Containers-2: Explore two really useful Docker images
You can try the below if you have Docker installed. If you have
Singularity/Apptainer and not Docker, the goal of the exercise can be to run
the Docker containers through Singularity/Apptainer.

1. Run a specific version of *Rstudio*:
   ```console
   $ docker run --rm -p 8787:8787 -e PASSWORD=yourpasswordhere rocker/rstudio
   ```

   Then open your browser to [http://localhost:8787](http://localhost:8787)
   with login rstudio and password "yourpasswordhere" used in the previous
   command.

   If you want to try an older version you can check the tags at
   [https://hub.docker.com/r/rocker/rstudio/tags](https://hub.docker.com/r/rocker/rstudio/tags)
   and run for example:
   ```console
   $ docker run --rm -p 8787:8787 -e PASSWORD=yourpasswordhere rocker/rstudio:3.3
   ```

2. Run a specific version of *Anaconda3* from
   [https://hub.docker.com/r/continuumio/anaconda3](https://hub.docker.com/r/continuumio/anaconda3):
   ```console
   $ docker run -i -t continuumio/anaconda3 /bin/bash
   ```
````
