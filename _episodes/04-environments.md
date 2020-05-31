---
layout: episode
title: "Recording environments"
teaching: 15
exercises: 0
questions:
  - How to capture the software environment of a computational experiment?

---

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

<div class="alert alert-dismissible alert-warning">
  <button type="button" class="close" data-dismiss="alert">&times;</button>
  <h4 class="alert-heading">Use only official and trusted images!</h4>
  <p>
    Not all images can be trusted! There have been examples of contaminated
    images so investigate before using images blindly. Apply same caution as installing
    software packages from untrusted package repositories.
  </p>
</div>

#### Examples of useful Docker images
1) Run a specific version of *Rstudio* 

`docker run --rm -p 8787:8787 -e PASSWORD=yourpasswordhere rocker/rstudio`

Then open your browser to [http://localhost:8787](http://localhost:8787) with login rstudio and password "yourpasswordhere" used in the previous command.
If you want to try an older version you can check the tags at [https://hub.docker.com/r/rocker/rstudio/tags](https://hub.docker.com/r/rocker/rstudio/tags) and run for example

`docker run --rm -p 8787:8787 -e PASSWORD=yourpasswordhere rocker/rstudio:3.3`

2) Run a specific version of *Anaconda3* from [https://hub.docker.com/r/continuumio/anaconda3](https://hub.docker.com/r/continuumio/anaconda3)

`docker run -i -t continuumio/anaconda3 /bin/bash`

and similarly one can also pick an image for *Anaconda2* at [https://hub.docker.com/r/continuumio/anaconda2/tags](https://hub.docker.com/r/continuumio/anaconda2/tags)


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


> ## Discussion: reproducibility aspects of container images
>
> - Do you think containers contribute to reproducible research?
> - Do you see a use case for your own work?
{: .discussion}
