---
layout: episode
title: "Virtual environments"
teaching: 20
exercises: 10
questions:
   - "How to capture the software environment of a computational experiment?"
   - "How can we communicate different versions of software dependencies?" 
objectives:
  - "Get a basic idea of how virtualization tools can be used to capture research software environments"
keypoints:
  - Use virtual environments or containers to share reproducible software environments

---

# Virtual environments

- Software may have lots of dependencies which may be difficult to recreate.
- Results should be possible to reproduce regardless of platform and with minimal effort.
- Many research codes can be problematic to install and configure without experts.
- Can we bundle all the necessary dependencies together, making it easier to run the software?

There are many ways to accomplish this, which differ in the scope
of virtualization:

| --- | --- |
| Virtual environments | Isolated *software environments* provided by environment management systems. |
| Operating-system-level virtualization | *Containers* sharing the host system's kernel. |
| Full virtualization | *Virtual machines* (VMs) emulating a computer system, providing functionality to run entire operating system. |

Here we will look into the first two approaches to bundle together 
dependencies into a virtual environment:
- **[Conda](https://docs.conda.io/en/latest/)**, a language agnostic, 
  cross-platform package, dependency and environment manager.
- **[Docker](https://www.docker.com/)**, a tool for creating, deploying, 
  and running applications isolated in "containers".

---

<img src="/reproducible-research/img/conda_logo.svg" style="height: 40px;"/>

- Created by Continuum Analytics, part of the Anaconda/Miniconda 
  Python distributions.
- Open source BSD license.
- Installs binary conda packages.
- Manages isolated software environments.
- Allows you to create and share conda packages.

### Conda as a package manager

With conda it is easy to list, search for, install, remove and update packages.
We can list all currently installed packages:

```shell
$ conda list
```

Let's say we want to install Snakemake. We begin by searching for it:
```shell
$ conda search snakemake

Loading channels: done
No match found for: snakemake. Search: *snakemake*

PackagesNotFoundError: The following packages are not available from current channels:

  - snakemake
...
```

Hmm, it's not available from our *current channels*. What are those?
Let's have a look at the configured channels:
```shell
$ conda config --get channels

--add channels 'defaults'   # lowest priority
--add channels 'conda-forge'   # highest priority
```

Ok, so we might need to look into other conda channels. This we can do 
either via the `anaconda` command, or through the 
[Anaconda Cloud](https://anaconda.org/).

```shell
$ anaconda search snakemake

Using Anaconda API: https://api.anaconda.org
Packages:
   Name                      |  Version | Package Types   | Platforms       | Builds
   ------------------------- |   ------ | --------------- | --------------- | ----------
     bioconda/snakemake        |    5.4.3 | conda           | linux-64, noarch, osx-64 | py34_1, py34_0, py36_1, py36_0, py36_2, 0, 2, py35_2, py35_0, py35_1
...
     bioconda/snakemake-minimal |    5.4.3 | conda           | linux-64, noarch, osx-64 | py36_1, py36_0, py_0, py_1, py_2, py35_0, py35_1
...
```

We see that Snakemake is available in the bioconda channel. But we also 
see that there's an alternative package called `snakemake-minimal`. 
What's the difference? Let's search for snakemake-minimal 
in the bioconda channel, display it's information, and compare it to 
the full snakemake package. We'll also limit ourselves to version 5.4.3:

```shell
$ conda search -c bioconda snakemake-minimal --info

snakemake-minimal 5.4.3 py_0
----------------------------
...
dependencies:
  - appdirs
  - configargparse
  - datrie
  - docutils
  - gitpython
  - jsonschema
  - psutil
  - python >=3.5
  - pyyaml
  - ratelimiter
  - requests >=2.8.1
  - setuptools
  - wrapt
```

What about the full package?

```shell
$ conda search -c bioconda snakemake=5.4.3 --info

snakemake 5.4.3 0
-----------------
...
dependencies:
  - aioeasywebdav
  - boto3
  - dropbox >=7.2.1
  - filechunkio >=1.6
  - ftputil >=3.2
  - google-cloud-storage
  - jinja2
  - jsonschema
  - networkx >=2.0
  - pandas
  - psutil
  - pygraphviz
  - pysftp >=0.2.8
  - python-irodsclient
  - snakemake-minimal 5.4.3.*
```

So we see that snakemake contains several additional packages 
compared to snakemake-minimal.  

We can now install it via:

```shell
$ conda install -c bioconda snakemake-minimal
```

If we want to update the package to the latest version:

```shell
$ conda update snakemake-minimal
```

and if we later want to remove it:

```shell
$ conda remove snakemake-minimal
```

---

### Conda as an environment manager

- Our colleague emails us a code which depends on specific versions of 
  several packages.
- We have some of the packages installed but not in the right versions.
- Can we create an isolated environment to run the code, 
  without breaking other software we have installed?

Conda allows us to create isolated environments for different 
software projects. For simplicity's sake, let's say our colleague 
is using pandas version 0.20.3, while we have pandas 0.24.1.
We create a new conda environment, and specify the versions of pandas:

```shell
$ conda create -n pd20 pandas=0.20

## Package Plan ##

  environment location: /Users/ktw/anaconda3/envs/pd20

  added / updated specs:
    - pandas=0.20

The following packages will be downloaded:
...

# To activate this environment, use
#
#     $ conda activate pd20
...
```

We activate the environment, and double-check that we have the correct 
versions:
```shell
$ conda activate pd20

(pd20)$ python -c "import pandas ; print(pandas.__version__)"
0.20.3
```

To list all environments, use the `info` subcommand:
```shell
$ conda info -e

base                     /Users/ktw/anaconda3
pd20                  *  /Users/ktw/anaconda3/envs/pd20
```

#### Reproducibility

Specifying a single version number of a package is simple, but 
for increased control, portability and reproducibility, 
we should use a file (in yaml or txt format) specifying packages, 
versions and channels needed to create the environment for a project.

Conda can generate this file for you, in one of two ways:
```shell
$ conda env export > environment.yml      # exports in yaml format
$ conda list --export > requirements.txt  # exports in simple text
```

- **The environment/requirements file should be tracked in the same 
repository as the source code!**

In the [word-count project](https://github.com/coderefinery/word-count) 
used in earlier episodes there is a simple requirements file, and we 
can create a new conda environment based on it:
```shell
$ conda create -n word-count --file requirements.txt
...
$ conda activate word-count
```

---

### Using conda to share a package

Conda packages can be built from a *recipe* and shared on 
[anaconda.org](https://anaconda.org/) via
[your own private or public channel](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/create-custom-channels.html), or
via [conda-forge](https://conda-forge.org).

- conda-forge is a GitHub organization containing repositories of conda 
  recipes. 
- Has become the de facto standard channel for packages.
- Several continuous integration providers ensure that each repository 
  ("feedstock") automatically builds its own recipe on Windows, Linux and OSX.

A step-by-step guide on how to contribute packages can be found in the
[conda-forge documentation](http://conda-forge.org/docs/maintainer/adding_pkgs.html). 

To get an idea of what's needed, let's have a look at the 
[boost feedstock](https://github.com/conda-forge/boost-feedstock/tree/2ceef9da69969ab3c0ae42817574b6c5b3219c99) (a set of C++ libraries). We see that:
- Every commit is tested on every platform.
- There's a list of maintainers.
- There's a [meta.yaml file](https://github.com/conda-forge/boost-feedstock/blob/2ceef9da69969ab3c0ae42817574b6c5b3219c99/recipe/meta.yaml) under the `recipe/` directory, along with (optional) `build.sh` and `bld.bat` files for building 
  non-python code on OSX/Linux and Windows platforms.

---

### Conda vs pip vs virtualenv vs pipenv vs poetry...

- Conda arose from the Python (PyData) community, but is designed to 
  manage packages and dependencies within any software stack (less like pip, 
  more like a cross-platform version of apt or yum).

- When it comes to packaging and dependency management in Python 
  (which can be rather convoluted and hard to understand) many alternative 
  tools exist.

| Tool | Purpose | Comments |
| ----- | ------ | -------- |
| [pip](https://pypi.org/project/pip/) | Python package installer | Can be used with conda. | 
| [virtualenv](https://virtualenv.pypa.io/en/latest/) | Tool to create isolated Python environments | Partly integrated into standard library under `venv` module. |
| [pipenv](https://pipenv.readthedocs.io/en/latest/) | Python package and virtualenv management | Official PyPA recommendation, replaces `pip` and `virtualenv`. |
| [poetry](https://poetry.eustace.io/) | Handle dependency installation, building/packaging of Python packages | Competitor to `pipenv`. | 

<a href="https://xkcd.com/1987/">
<img src="/reproducible-research/img/python_environment.png" style="height: 300px;" class="center">
</a>

---

## Containers

- Containers can be built to bundle all the necessary ingredients (data, code, environment).
- A great solution to the problem of ["dependency hell"](https://en.wikipedia.org/wiki/Dependency_hell).
- Allows for seamlessly moving workflows across different platforms.
- A container provides operating-system-level virtualization, i.e. it shares the host system’s kernel with other containers.
- Popular container implementations are **[Docker](https://www.docker.com/)** and **[Singularity](http://singularity.lbl.gov/)**.
- "[the term] is borrowed from Shipping Containers, which define a standard to ship goods globally. Docker defines a standard to ship software." ([from the Docker documentation](https://docs.docker.com/glossary/)).

### Docker

- Docker provides containerization in software level.
- Available for most common operating systems.
- Provides an easy and fast way to bundle all the necessary libraries and data together.
- A mechanism to "send the computer to the data", when data is too large 
  or too sensitive to travel over network.
- DockerHub is a platform to share Docker images (stored in repositories - similar to Git repository).
- Public Docker images available on [DockerHub](https://hub.docker.com/) but a word of warning: <span style="color: red">not all images can be trusted! There have been examples of contaminated images so investigate before using images blindly</span>.

---

### Singularity 

- [Singularity](http://singularity.lbl.gov/) is aimed at scientific community and to run scientific workflows on HPC resources.
- Docker is compatible with Singularity:
  - Docker images can be converted into Singularity images.

---

### Docker fundamentals

- Docker is a client-server application. The Docker client talks to the Docker server
or daemon, which, in turn, does all the work.

<img src="/reproducible-research/img/docker_architecture.svg" style="height: 400px;"/>

- Docker client
   - End user uses Docker client to communicate with Docker daemon .
- Docker daemon
   - Executes the commands sent to the Docker client. Manages containers, images, builds, etc.
- Docker registry
   - Stores Docker images. DockerHub and Docker Cloud are public registries that anyone can use, and Docker is configured to look for images on DockerHub by default.
   - You can even run your own private registry.


### What are Docker images and containers

- A Docker *image* is executable package of a piece of software that includes everything needed to run it: code, runtime, system tools, system libraries, settings.
- When you start the image, you have a running *container* of this image.

Getting help:
```shell
$ docker help <command>
```

Listing Docker images:
```shell
$ docker images
```
Searching Docker images from DockerHub:
```shell
$ docker search ubuntu
```
Pulling from DockerHub (pulls the latest one by default if no tag is mentioned):
```shell
$ docker pull ubuntu
```
Starting container from the pulled image:
```shell
$ docker run -i -t ubuntu
  
-i flag keeps STDIN open from the container
-t flag provides an interactive shell to the container
```
   
Check running containers:
```shell
$ docker ps
```
Check all containers (also those not running):
```shell
$ docker ps -a
```
Stop the container:
```shell
$ docker stop container_id or name
```
Start (in interactive mode) a stopped container:
```shell
$ docker start -i container_id or name
```
Remove a container:
```shell
$ docker rm <container name>
```
Remove an image:
```shell
$ docker rmi <image name>
```

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

#### Mnemonics

- The Dockerfile is like a cooking recipe, building an image from the Dockerfile 
  is like doing the actual cooking.
- Running the Docker image to create a container doesn't have a good cooking analogy, but:
  - a Docker image is like a *class* in OOP, a Docker container is like an instance of the class.

  
## Type-along exercise: Containerizing our workflow

> This exercise is based on the [same example project](https://github.com/coderefinery/word-count) as in the previous episodes

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


## Starting containers from images

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

## Managing data

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

## Sharing a Docker image
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

---

### Where you might want to go from here

- New platforms for doing reproducible research are emerging, see for example [**reana**](http://www.reana.io/).
- Good talks on open reproducible research can be found [here](http://inundata.org/talks/index.html).
