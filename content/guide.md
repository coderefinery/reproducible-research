---
layout: default
permalink: /guide/
---

# Instructor guide

## Why we teach this lesson

Reproducibility in research is something that publishers, funding agencies, universities,
research leaders and the general public worries about and much is being written about it.
It is also something that researchers care deeply about - this lesson is typically one of the 
most popular lessons in the pre-workshop survey.

Even though most PhD students, postdocs and researchers (i.e. typical workshop participants)
know about the importance of reproducibility in research, they often lack both a general 
overview of what different aspects there are to reproducibility, and the knowledge of 
specific tools that can be used for improving reproducibility.

Many participants may not adhere to good practices when organizing their projects, 
and the "Organizing your projects" episode is meant to encourage participants to 
structure their projects better. This may be obvious to some participants but it 
doesn't harm to preach to the choir.

Many participants do not share data or code, and in particular they are often 
unaware that research output other than published articles can be assigned 
digital object identifiers (DOIs). 
The "Sharing code and data" is meant to bring awareness about FAIRness and Open Science
and to show how DOIs can be obtained for Git repositories..

Even though many participants know that code can have many dependencies (e.g. they 
may have experienced difficulties in getting other people's code to run), they 
often don't know or use good practices when it comes to recording dependencies. 
Most participants also don't use isolated environments for different projects and 
don't know why that can be important.
The episode "Recording dependencies" tries to convey the importance of recording 
dependencies accurately for your projects, and shows how tools like conda can be 
used both as a package and software environment manager.

Many participants have heard about containers and find them interesting, but 
lack an understanding of how they work or how they can be used. The episode 
"Recording environments" introduces the concept of containers, and the optional 
episode "Creating and sharing a container image" goes into details.

Many participants use complicated series of computational steps in their research 
without realizing that this work falls into the category of "scientific workflows", 
and that there actually exist tools that help make such workflows reproducible.
The episode "Recording computational steps" introduces the concept of scientific 
workflows, discusses various ways of managing workflows with varying degrees of 
reproducibility, and shows how tools like make and snakemake can be used to 
both simplify workflows and make them more reproducible.

## Intended learning outcomes

By the end of this lesson, learners should:
- understand why it's important that research is reproducible
- define multiple levels of reproducibility and the multiple 
  factors which can lead to irreproducible research
- be able to apply well organized directory structure for their project
- remember the FAIR principles
- be able to create a DOI for research output like code or data
- understand that code can have dependencies, and know how to create a requirements file
- describe how to use conda (or another tool) to manage isolated software environments
- have an idea about how containers work
- remember the pros and cons of containers for reproducibility 
- understand that a series of computational steps can be defined as a workflow and 
  that many tools exist to manage workflows
- describe the pros and cons of different methods of performing scientific workflows
- understand the benefits of using a tool like make or snakemake compared to bespoke scripts
- be able to create a simple Makefile or Snakefile to manage a workflow

## List of exercises

1. **"Motivation" episode, "Discuss with your neighbors or among all participants", 5 minutes:**  
   This is a discussion exercise. In online workshops the exercise can be performed 
   using a shared workshop document (e.g. HackMD) where the exercise text is copied to the document and learners are asked to write down their experiences. In in-person workshops learners can discuss in groups around their tables.
2. **"Organizing your projects" episode, "Word count - an example project", 5 minutes:**   
   This exercise is performed as a type-along. The instructor slowly and methodically goes through the steps and explains what's happening.
3. **"Recording dependencies" episode, "Different requirements.txt solutions", 5-10 minutes:**  
   This exercise can be performed as a general discussion (appropriate for online workshops) or as a group discussion (in in-person workshops). For a general discussion in online workshops the instructor can either walk through the exercise or let learners write down answers in a shared document.
4. **"Recording dependencies" episode, "Exploring conda environments", 10 minutes:**  
   This exercise requires learners to perform steps on their own computers. In online workshops it should be done in breakout rooms for around 10 minutes.   
5. **"Recording computational steps" episode, "(Optional) Snakemake in HPC":**  
   This is left as homework for learners who are interested.
6. **"Recording computational steps" episode, "Exercise using Snakemake", 10-15 minutes:**  
   Hands-on exercise for learners to perform in groups or in breakout rooms. The purpose is for learners to understand how Snakemake operates and develop some muscle memory.
7. **"Recording computational steps" episode, "(Optional) Using Snakemake with conda environments":**  
   This is an optional exercise for learners who finish the Snakemake 
   exercise quickly.
8. **"Sharing code and data" episode, "Get a DOI by connecting your 
   repository to Zenodo", 15 minutes:**  
   Hands-on exercise for learners to do in groups or breakout rooms.
   The purpose is for learners to realize how easy it is to upload code or data to Zenodo and mint a DOI.



## How to teach this lesson

### How to start

Everyone knows that scientific results need to be reproducible, but not everyone is using 
appropriate tools to ensure this. Here we're going to get to know tools which help with
preserving the provenance of data and reproducibility on different levels, ranging from
workflow automation to software environment (containers).


### Focus on concepts, and when to use which tool

Try to explain better what the different tools are useful for, but don't go
into details.  In this lesson we are not trying to gain expertise in the
various tools and master the details but rather we want to give an overview and
show that many tools exist and try to give participant the right feel for which
set of tools to approach for which type of problem.


### Questions to involve participants

- Have you ever been unable to reproduce a scientific results from previous research by yourself or others?
- What technical solutions do you use to manage repetitive tasks and/or complicated workflows?


### Timing

Depending on workshop schedule, this lesson can become short on time.
- The Snakemake episode is long. The instructor needs to explain what is snakemake, and why use it.
  Snakefile can be covered quickly. Wildcards and pattern rules should be discussed,
  but the optional further topics can be skipped or just very briefly described.
  The exercise(s) in breakoutroom session is then there for the participants to play around
  and get an understanding of the how.
- Building the container from scratch (fetching the ubuntu image, installing all packages in it)
  can take several minutes. The instructor should in most cases do this before the workshop and 
  only demonstrate how to launch a container based on the existing image


### Sessions which can be skipped if time is tight

- The motivation can be gone through quickly. Researchers know the importance of
  reproducibility and we don't need to spend many words on it


### Typical pitfalls

#### Indentation in Snakefiles

- the body of a rule and the body of an input keyword need to be indented, but the number of spaces doesn't matter
This works:
```python
rule alldata:
     input:
         'processed_data/isles.dat',
         'processed_data/abyss.dat'
```
but this doesn't work:
```python
rule alldata:
     input:
     'processed_data/isles.dat',
     'processed_data/abyss.dat'
```
not this:
```python
rule alldata:
input:
    'processed_data/isles.dat',
    'processed_data/abyss.dat'
```

#### Containers are confusing

Try to use good analogies to explain the concepts of containers, 
images and Dockerfiles.
