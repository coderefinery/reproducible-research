---
layout: default
permalink: /guide/
---

# Instructor guide

## Why we teach this lesson

WRITEME

## Intended learning outcomes

By the end of this lesson, learners should:
- understand why it's important that research is reproducible
- know that there are multiple levels of reproducibility and multiple 
  factors which can lead to irreproducible research
- be motivated to use well organized directory structure for their project
- know that there are multiple tools available for collaborating on 
  writing manuscripts 
- understand the concept of command-line automation (scripts/make) 
  and know  is usually more difficult in GUIs
- know that multiple tools exist to assist researchers with creating automatic and reproducible workflows which preserve the provenance of data 
- get familiar with one such tool (Snakemake)
- understand that using workflow tools can enhance the quality of research and save time
- unlike shell scripts, make/snakemake knows job dependencies and only rebuilds necessary steps

WRITEME

## How to teach this lesson

### How to start

Everyone knows that scientific results need to be reproducible, but not everyone is using 
appropriate tools to ensure this. Here we're going to get to know tools which help with
preserving the provenance of data and reproducibility on different levels, ranging from
workflow automation to software environment (containers).


### Questions to involve participants

- Have you ever been unable to reproduce a scientific results from previous research by yourself or others?
- What technical solutions do you use to manage repetitive tasks and/or complicated workflows?

### Timing

Depending on workshop schedule, this lesson can become short on time. 
- The Snakemake episode is long, but the first steps in constructing the 
  Snakefile can be covered quickly. Enough time should be devoted to the exercise though. 
  Wildcards and pattern rules should be discussed, but the optional further topics can be skipped
  or just very briefly described
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