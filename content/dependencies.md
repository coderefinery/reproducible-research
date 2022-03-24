# Recording dependencies

```{questions}
- How can we communicate different versions of software dependencies?
```

```{instructor-note}
- 15 min teaching
- 15 min exercises
```
Our codes often depend on other codes that in turn depend on other codes ...

- **Reproducibility**: We can control our code but how can we control dependencies?
- **10-year challenge**: Try to build/run your own code that you have created 10 (or less) years ago. Will your code
  from today work in 5 years if you don't change it?
- **Dependency hell**: Different codes on the same environment can have conflicting dependencies.

---

```{figure} img/python_environment.png
:alt: Python environment
:width: 100%

From [xkcd](https://xkcd.com/).
```

## Conda, Anaconda, pip, Virtualenv, Pipenv, pyenv, Poetry, requirements.txt ...

These tools try to solve the following problems:
- Installing a **specific set of dependencies**, possibly with well defined versions
- **Recording the versions** for all dependencies
- **Isolate environments** on your computer for projects that have conflicting dependencies
- Isolate environments on computers with many users
- Using **different Python/R versions** per project
- Provide tools and services to **share packages**

Isolated environments are also useful because they help you make sure
that you know your dependencies!

---

(different-solutions-to-specify-requirements)=

## Exercise - Different solutions to specify requirements

````{challenge} Dependencies-1: Comparing requirements
Compare these four requirements.txt 

**A**:

Code depends on a number of packages but there is no `requirements.txt` file or equivalent.


**B**:
```
scipy
numpy
sympy
click
git+https://github.com/someuser/someproject.git@master
git+https://github.com/anotheruser/anotherproject.git@master
```

**C**:
```
scipy==1.3.1
numpy==1.16.4
sympy==1.4
click==7.0
git+https://github.com/someuser/someproject.git@d7b2c7e
git+https://github.com/anotheruser/anotherproject.git@sometag
```

**D**:
```
scipy==1.3.1
numpy==1.16.4
sympy==1.4
click==7.0
someproject==1.2.3
anotherproject==2.3.4
```

```{solution}
**A**: If there is no requirements.txt file (or similar), it might become very difficult
for others to create the software environment required to run your software. This can
also apply to yourself in the future!

**B**: Having a requirements.txt file is definitely better than nothing. However, if the
versions are not specified you or someone else might run into problems with dependencies,
deprecated features, changes in package APIs etc.

**C** and **D**: In both these cases exact versions of all dependencies are specified and
both others and you yourself can recreate the software environment required for the project.
**D** is slightly preferable because version numbers are easier to understand than Git
commit hashes or Git tags.
```

````

---

## Pip and [PyPI](https://pypi.org)

- Python Package Index.
- Standard place to share Python packages.
- Also mixed-language packages are possible wrapped in a Python layer.
- Install a package:
```
$ pip install somepackage
```
- Install a specific version:
```
$ pip install somepackage==1.2.3
```
- Freeze the current environment into `requirements.txt`:
```
$ pip freeze > requirements.txt
```
- Install all dependencies listed in `requirements.txt`:
```
$ pip install -r requirements.txt
```
- Creating and sharing your own package: [https://packaging.python.org/tutorials/packaging-projects/](https://packaging.python.org/tutorials/packaging-projects/)
- It is possible to pip install from GitHub or other places:
```
$ pip install git+https://github.com/anotheruser/anotherproject.git@sometag
```

---

## [Conda](https://docs.conda.io/en/latest/)

```{figure} img/conda_cartoon.jpeg
:width: 100%
:alt: Conda cartoon
```

- Not only for Python: any language, also binaries.
- Created by Continuum Analytics, part of Anaconda/Miniconda, but can be installed standalone.
- Open source BSD license.
- Manages isolated software environments.
- Allows you to create and share conda packages.
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) is a lightweight alternative to [Anaconda](https://www.anaconda.com).
- Install a package:
```
$ conda install somepackage
```
- Install a specific version:
```
$ conda install somepackage=1.2.3
```
- Create a new environment:
```
$ conda create --name myenvironment
```
- Create a new environment from `requirements.txt`:
```
$ conda create --name myenvironment --file requirements.txt
```
- On e.g. HPC systems where you don't have write access to central
  installation directory:
```
$ conda create --prefix /some/path/to/env
```
- Activate a specific environment:
```
$ conda activate myenvironment
```
- Deactivate current environment:
```
$ conda deactivate
```
- List all environments:
```
$ conda info -e
```
- Freeze the current environment into `requirements.txt`:
```
$ conda list --export > requirements.txt
```
- Freeze the current environment into `environment.yml`:
```
$ conda env export > environment.yml
```
- To clean unnecessary cached files (which grow quickly over time):
```
$ conda clean # needs one flag, add --help for available options
```

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

---

(exploring-conda-environments)=

## Exercise - Exploring conda environments

```{exercise} Dependencies-2: Working with conda
- Inspect your available environments with `conda info -e`.
- Deactivate the current environment with `conda deactivate`.
- Use `conda activate base` to change to the base environment.
- List the packages in the base environment with `conda list`. How many packages are there?
- Activate the coderefinery environment with `conda activate coderefinery`.
  List the packages with `conda list`.
- Details of the conda installation can be shown with `conda info`.
  Which is the active environment? Where are the packages stored?
  Where are the environments stored?
- Create a new environment with `conda create --name myenv` **and activate it**.
- Install the `pandas` package using `conda install pandas`.
- Export the requirements into requirements.txt with `conda list --export > requirements.txt`.
- Export the full environment using `conda env export > environment.yml`, and 
  compare the `.yml` file format to the `.txt` file format.
- If you want to make sure your new environment.yml is correct, 
  you can use it to create a new 
  test environment using `conda env create -n <envname> -f <file.yml>`.
  Were any new packages installed?
  You can delete the test environment with 
  `conda env remove -n <envname>` or simply remove the directory of the 
  environment (that you can find using `conda info -e`).
```

---

## Other dependency management tools

### Python

- [Virtualenv](https://docs.python-guide.org/dev/virtualenvs/)
  - Example use:
  ```shell
  # creating a new env
  $ virtualenv myenvironment
  $ virtualenv --python=python3 myenvironment
  $ virtualenv /path/to/myenvironment
  # activating env, installing package and deactivating
  $ source myenvironment/bin/activate
  $ pip install somepackage
  $ deactivate
  ```
- [Pipenv](https://pipenv.readthedocs.io)
  - Alternative to virtualenv: you can activate and install in one step
  - Tool to easily manage per-project/per-directory Python **packages**
  - Easier than virtualenv to separate dependencies for development and usage
- [Poetry](https://poetry.eustace.io)
  - Alternative to virtualenv and Pipenv
- [Pyenv](https://github.com/pyenv/pyenv)
  - Tool to easily manage per-project/per-directory Python **versions**
- [Mamba](https://github.com/mamba-org/mamba)
  - works like conda, but resolves dependencies faster 


### R

Good overview of use cases, strategies and tools for reproducible
environment at
[Reproducible Environments](https://environments.rstudio.com).

There are many tools available:
- [packrat](https://rstudio.github.io/packrat/)
  - Package from RStudio to isolate environment. Uses a packrat.lock file for storing dependencies
- [Jetpack](https://github.com/ankane/jetpack)
  - Designed as a CLI on top of packrat. Uses the DESCRIPTION file to store your project dependencies
- [RSuite](https://rsuite.io/)
- [automagic](https://github.com/cole-brokamp/automagic)
- [deplearning](https://github.com/MilesMcBain/deplearning)
- [devtools](https://github.com/r-lib/devtools)
- Are you using something else? Please send a
  [pull request](https://github.com/coderefinery/reproducible-research)!

### C/C++

There are no standard methods or tools to handle dependencies in
C/C++, but useful tools include: 

- [CMake](https://cmake.org/) 
  - Open-source, cross-platform family of tools designed to build,
    test and package software (see also the [CodeRefinery lesson on
    CMake](https://coderefinery.github.io/cmake/))
- [Conan](https://conan.io/)
  - A C/C++ package manager for Developers
- [Conda](https://docs.conda.io/en/latest/)
  - Works with any language, in principle

### Fortran

- [Fortran Package Manager](https://github.com/fortran-lang/fpm) A package manager and build system for Fortran.

### Julia

The inbuilt package manager in Julia,
[Pkg.jl](https://pkgdocs.julialang.org/v1/), is designed around using
isolated environments with independent sets of packages. Environments
can either be local to a particular project or shared and selected by
name.

## See also

- [Semantic Versioning](https://semver.org/)
- [Alternative opinion: Why not semver?](http://faq.sealedabstract.com/why_not_semver/)


```{keypoints}
  - Capturing software dependencies is a must for reproducibility.
  - Files like `requirements.txt`, `environment.yml`, `Pipenv`, ..., should be part of the source repository.
  - Be skeptical when you see dependency lists without versions.
```
