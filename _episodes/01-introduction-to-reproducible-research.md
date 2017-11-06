---
layout: episode
title: "Making research reproducible"
teaching: 15
exercises: 30
questions:
  - "Why research should be reproducible?"
  - "Can someone reproduce the results we have published/reported?"
  - "How to repeat an experiment with different data after one year later?"
  - "How to make results reproducible regardless of platforms with minimal effort?"
  - "How do you communicate different versions of dependencies you need?"
objectives:
  - "The goal is to get a basic idea of different tools that can be used to make research reproducible"
  - "You can use some of these tools in your research lifecycle"
keypoints:
  -
 
---

## Why reproducible research?
   - long term value of data
   - Uniqueness of data. Data collected today may be invalid/inappropriate 6 months
     from now
   - Publications after 2 years data collection ends  
   
## What is reproducible research?

- Same code and data used for conducting an experiment
- ??? _use material from coderefinery drive_
- generic definitions
- For any research project, an independent researcher should be able to replicate the experiment under the same conditions and receive the same results.

---

## Main drawbacks of not able to reproduce research 
- software/code used to produce research
- data used to produce research
- documentation on how data is generated
- How to create software (with different libraries) we have applied?

---
## Could we apply the tools used in the workshop to create reproducible research?

### Tracking the code we have used in an experiment

- Using git for tracking the code. 
- Multiple ways to track a specific piece of code.
- for example, using git tags to mark a specific piece of code we have used in an experiment

### Documentation on data generation  

- As projects grow, it is quite difficult to keep track of all the workflow steps and how they fit together
- How we have generated/created the data in the first case
- The steps we have followed in creating the data
- for example, we can use make to track the steps we have followed in generating the data
- makefile itself can act as a documentation for data generation

---

## How to create the software applied for an experiment?
- Software we have used may depend on lot of dependencies and may be difficult to create and run
- Many research softwares can be problematical to install and configure without experts. 
- Could we bundle all the necessary dependencies together, so that it is easy to run the software
- We can use containers to create isolation environments.

---

# Containers

- Containers can be seen as a 'ready-to-eat' software. Containers can be built to bundle all the necessary ingredients.
- A standardized unit of software
- A great solution to the problem of dependency hell
- Allows for seamlessly moving workflows across different platforms
- Popular container implementations are Docker and Singularity

## Docker
- Docker provides containerisation in software level
- Available for most common operating systems, and also some clouds: AWS, Azure
- Provides an easy and fast way to bundle all the necessary library and data together
- Public Docker images available in Docker hub [https://hub.docker.com/](https://hub.docker.com/) but a word of warning: <span style="color: red">not all images can be trusted! There have been examples of contaminated images so investigate before using images blindly</span>.

##- Note that Docker containers should be disposable: the data must be saved elsewhere
##- The image is built based on the Dockerfile

---

## What aspects of containers would we like to communicate?


## Docker fundamentals
- How docker virtualizes the environment
- Docker engine/daemon
- Docker client

## What is a docker image
- A container image is a lightweight, stand-alone, executable package of a piece of software that includes everything needed to run it: code, runtime, system tools, system libraries, settings.
- A Docker image is made up of filesystems layered over each other. Docker calls each of these filesystems images.
- Listing docker images
- Searching docker images from Dockerhub
- pulling from dockerhub

## building docker images
- Dockerfile with docker build command
- The Dockerfile contains a series of instructions paired with arguments
- commands to use
- example create a simple webserver

## creating containers from images
- running a container
- exposing ports
- volumes

## sharing a docker image
- dockerhub
- pushing to dockerhub
- docker private registries

---
## singularity container (good to know)
- Singularity is aimed at scientific community and to run scientific workflows
- Docker is compatible with singularity, but the main purpose of docker is for micro services and different that the purpose of singularity
- Docker is compatible with singularity, so docker images can be later converted into singularity images

---
## Exercise:

#### Let's look at an example project and ask other groups to reproduce it

- Code tracking with git
- data generation using make
- dependency isolation using containers
