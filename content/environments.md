# Recording environments

```{objectives}
- Understand what containers are and what they are useful for
- Discuss container definitions files in the context of reusability and
  reproducibility
```

```{instructor-note}
- 10 min teaching/discussion
- 10 min demo
```

## What is a container?

Imagine if you didn't have to install things yourself, but instead you could
get a computer with the exact software for a task pre-installed? Containers
effectively do that, with various advantages and disadvantages. They are
**like an entire operating system with software installed, all in one file**.

```{figure} img/docker_meme.jpg
:alt: He said, then we will ship your machine. And that's how Docker was born.
:width: 60%

From [reddit](https://www.reddit.com/r/ProgrammerHumor/comments/cw58z7/it_works_on_my_machine/).
```

``````{discussion} Kitchen analogy
- Our codes/scripts <-> cooking recipes
- Container definition files <-> like a blueprint to build a kitchen with all
  utensils in which the recipe can be prepared.
- Container images <-> showroom kitchens
- Containers <-> A real connected kitchen

Just for fun: which operating systems do the following example kitchens represent?
  `````{tabs}
    ````{tab} 1
      ```{figure} img/kitchen/macos.png
      :alt: Generated image of a kitchen
      :width: 50%

      [Midjourney, CC-BY-NC 4.0]
      ```
    ````

    ````{tab} 2
      ```{figure} img/kitchen/windows.png
      :alt: Generated image of a kitchen
      :width: 50%

      [Midjourney, CC-BY-NC 4.0]
      ```
    ````

    ````{tab} 3
      ```{figure} img/kitchen/linux.png
      :alt: Generated image of a kitchen
      :width: 50%

      [Midjourney, CC-BY-NC 4.0]
      ```
    ````
  `````
``````

## From definition files to container images to containers

- Containers can be built to bundle _all the necessary ingredients_ (data, code, environment, operating system).
- A container image is like a piece of paper with all the operating system on it. When you run it,
  a transparent sheet is placed on top to form a container. The container runs and writes only on
  that transparent sheet (and what other mounts have been layered on top). When you are done,
  transparency is thrown away. It can be repeated as often as you want, and base is always the same.
- Definition files (e.g. Dockerfile or Singularity definition file) are text
  files that contain a series of instructions to build container images.

## You may have use for containers in different ways

- **Installing a certain software is tricky**, or not supported for your operating system? - Check if an image is available and run the software from a container instead!
- You want to make sure your colleagues are using the **same environment** for running your code? - Provide them an image of your container!
  - If this does not work, because they are using a different architecture than you do? - Provide a definition file for them to **build the image suitable to their computers**. This does not create the exact environment as you have, but in most cases similar enough.

## The container recipe

Here is an example of a Singularity definition file ([reference](https://apptainer.org/docs/user/main/build_a_container.html#building-containers-from-apptainer-definition-files)):

```
Bootstrap: docker
From: ubuntu:24.04

%post
    apt-get -y update
    apt-get -y install fortune cowsay lolcat

%environment
    export LC_ALL=C
    export PATH=/usr/games:$PATH

%runscript
    fortune | cowsay | lolcat
```

Popular container implementations:

- [Docker](https://www.docker.com/)
- [Singularity](https://sylabs.io/docs/) (popular on high-performance computing systems)
- [Apptainer](https://apptainer.org) (popular on high-performance computing systems, fork of Singularity)
- [podman](https://podman.io/)

They are to some extent interoperable:

- podman is very close to Docker
- Docker images can be converted to Singularity/Apptainer images
- [Singularity Python](https://singularityhub.github.io/singularity-cli/) can convert Dockerfiles to Singularity definition files

---

## Pros and cons of containers

Containers are popular for a reason - they solve a number of
important problems:

- Allow for seamlessly **moving workflows across different platforms**.
- Can solve the **"works on my machine"** situation.
- For software with many dependencies, in turn with its own dependencies,
  containers offer possibly the only way to preserve the
  computational experiment for **future reproducibility**.
- A mechanism to "send the computer to the data" when the **dataset is too large** to transfer.
- **Installing software into a file** instead of into your computer (removing
  a file is often easier than uninstalling software if you suddenly regret an
  installation)

However, containers may also have some drawbacks:

- Can be used to hide away software installation problems and thereby
  **discourage good software development practices**.
- Instead of "works on my machine" problem: **"works only in this container"** problem?
- They can be **difficult to modify**
- Container **images can become large**

```{danger}
Use only **official and trusted images**!  Not all images can be trusted! There
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

``````{exercise} Containers-1: Time travel
  Scenario: A researcher has written and published their research code which
  requires a number of libraries and system dependencies. They ran their code
  on a Linux computer (Ubuntu). One very nice thing they did was to publish
  also a container image with all dependencies included, as well as the
  definition file (below) to create the container image.

  Now we travel 3 years into the future and want to reuse their work and adapt
  it for our data. The container registry where they uploaded the container
  image however no longer exists. But luckily we still have the definition file
  (below)! From this we should be able to create a new container image.

  - Can you anticipate problems using the definitions file 3 years after its creation?
    Which possible problems can you point out?
  - Discuss possible take-aways for creating more reusable containers.

  `````{tabs}
    ````{tab} Python project using virtual environment
      ```{code-block}
      :linenos:
      Bootstrap: docker
      From: ubuntu:latest

      %post
          # Set environment variables
          export VIRTUAL_ENV=/app/venv

          # Install system dependencies and Python 3
          apt-get update && \
          apt-get install -y --no-install-recommends \
              gcc \
              libgomp1 \
              python3 \
              python3-venv \
              python3-distutils \
              python3-pip && \
          apt-get clean && \
          rm -rf /var/lib/apt/lists/*

          # Set up the virtual environment
          python3 -m venv $VIRTUAL_ENV
          . $VIRTUAL_ENV/bin/activate

          # Install Python libraries
          pip install --no-cache-dir --upgrade pip && \
          pip install --no-cache-dir -r /app/requirements.txt

      %files
          # Copy project files
          ./requirements.txt /app/requirements.txt
          ./app.py /app/app.py
          # Copy data
          /home/myself/data /app/data
          # Workaround to fix dependency on fancylib
          /home/myself/fancylib /usr/lib/fancylib

      %environment
          # Set the environment variables
          export LANG=C.UTF-8 LC_ALL=C.UTF-8
          export VIRTUAL_ENV=/app/venv

      %runscript
          # Activate the virtual environment
          . $VIRTUAL_ENV/bin/activate
          # Run the application
          python /app/app.py
      ```

      ```{solution}
      - Line 2: "ubuntu:latest" will mean something different 3 years in future.
      - Lines 11-12: The compiler gcc and the library libgomp1 will have evolved.
      - Line 30: The container uses requirements.txt to build the virtual environment but we don't see
        here what libraries the code depends on.
      - Line 33: Data is copied in from the hard disk of the person who created it. Hopefully we can find the data somewhere.
      - Line 35: The library fancylib has been built outside the container and copied in but we don't see here how it was done.
      - Python version will be different then and hopefully the code still runs then.
      - Singularity/Apptainer will have also evolved by then. Hopefully this definition file then still works.
      - No contact address to ask more questions about this file.
      - (Can you find more? Please contribute more points.)
      ```
    ````

    ````{tab} R project using renv
    Work in progress: Please contribute a corresponding example which
    demonstrates this in the context of R and renv.
    ````
  `````
``````

````{exercise} (optional) Containers-2: Installing the impossible.

When you are missing privileges for installing certain software tools, containers can come handy.
Here we build a Singularity/Apptainer container for installing `cowsay` and `lolcat` Linux programs.

1. Make sure you have apptainer installed:
   ```console
   $ apptainer --version
   ```

2. Make sure you set the apptainer cache and temporary folders.
   ```console
   $ mkdir ./cache/
   $ mkdir ./temp/
   $ export APPTAINER_CACHEDIR="./cache/"
   $ export APPTAINER_TMPDIR="./temp/"
   ```

3. Build the container from the following definition file above.
   ```console
   apptainer build cowsay.sif cowsay.def
   ```

4. Let's test the container by entering into it with a shell terminal
   ```console
   $ apptainer shell cowsay.sif
   ```

5. We can verify the installation.
   ```console
   $ cowsay "Hello world!"|lolcat
   ```

````

````{exercise} (optional) Containers-3: Explore two really useful Docker images
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

## Resources for further learning

- [Carpentries incubator lesson on Docker](https://carpentries-incubator.github.io/docker-introduction/)
- [Carpentries incubator lesson on Singularity/Apptainer](https://carpentries-incubator.github.io/singularity-introduction/)

```{keypoints}
- Containers can be helpful if complex setups are needed to running a specific software
- They can also be helpful for prototyping without "messing up" your own computing environment, or for running software that requires a different operating system than your own
```
