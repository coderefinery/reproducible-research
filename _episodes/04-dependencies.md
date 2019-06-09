---
layout: episode
title: "Recording dependencies"
teaching: 15
exercises: 0
questions:
  - How can we communicate different versions of software dependencies?
keypoints:
  - Capturing software dependencies is a must for reproducibility.

---

# Virtual environments

- Software may have lots of dependencies which may be difficult to recreate.
- Results should be possible to reproduce regardless of platform and with minimal effort.
- Many research codes can be problematic to install and configure without experts (see ["dependency hell"](https://en.wikipedia.org/wiki/Dependency_hell)).
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

---

<img src="{{ site.baseurl }}/img/conda_logo.svg" style="height: 40px;"/>

- Created by Continuum Analytics, part of Anaconda/Miniconda
  but can be installed standalone.
- Open source BSD license.
- Installs binary conda packages.
- Manages isolated software environments.
- Allows you to create and share conda packages.

<a href="https://medium.freecodecamp.org/why-you-need-python-environments-and-how-to-manage-them-with-conda-85f155f4353c">
<img src="{{ site.baseurl }}/img/conda_cartoon.jpeg" style="height: 300px;"/>
</a>

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
either via [Anaconda Cloud](https://anaconda.org/) or through
the `anaconda` command:

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
$ conda search -c bioconda snakemake-minimal=5.4.3 --info

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
| [pipenv](https://pipenv.readthedocs.io/en/latest/) | Python package and virtualenv management | Official PyPA recommendation, combines functionality of `pip` and `virtualenv`. |
| [poetry](https://poetry.eustace.io/) | Handle dependency installation, building/packaging of Python packages | Competitor to `pipenv`. |

<a href="https://xkcd.com/1987/">
<img src="{{ site.baseurl }}/img/python_environment.png" style="height: 300px;" class="center">
</a>
