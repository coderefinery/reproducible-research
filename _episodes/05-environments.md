---
layout: episode
title: "Recording environments"
teaching: 15
exercises: 0
questions:
  - How to capture the software environment of a computational experiment?

---

## Containers

A deeper level of virtualization is provided by container technology.

- Containers can be built to bundle *all the necessary ingredients* (data, code, environment).
- A container provides operating-system-level virtualization, sharing the host system’s kernel with other containers.
- Popular container implementations are **[Docker](https://www.docker.com/)** and **[Singularity](http://singularity.lbl.gov/)**.
- "[the term] is borrowed from Shipping Containers, which define a standard to ship goods globally. Docker defines a standard to ship software." ([from the Docker documentation](https://docs.docker.com/glossary/)).


### Docker

- Available for most common operating systems.
- A mechanism to "send the computer to the data" when data is too
  large/sensitive to travel over network.
- DockerHub is a platform to share Docker images (stored in repositories - similar to Git repository).
- Public Docker images available on [DockerHub](https://hub.docker.com/) but a word of warning: <span style="color: red">not all images can be trusted! There have been examples of contaminated images so investigate before using images blindly</span>.

---

### Singularity

- [Singularity](http://singularity.lbl.gov/) is aimed at scientific community and to run scientific workflows on HPC resources.
- Docker images can be converted into Singularity images.

---

### Pros and cons of containers

Containers are popular for a reason - they solve a number of
important problems:
- Allow for seamlessly moving workflows across different platforms.
- Much more lightweight than virtual machines.
- Eliminates the "works on my machine" situation

However, containers may also have some drawbacks:
- Containers can have security vulnerabilities which can be exploited.
- Can be used to hide away software installation problems and thereby
  discourage good software development practices.
- A "super-glued" container image is not good for reproducibility
  - a *recipe* for creating the image is better

> ## Exercise: reproducibility aspects of virtual environments
>
> - Do you think containers contribute to reproducible research?
> - Do you see a use case for your own work?
{: .task}
