---
layout: default
permalink: /guide/
---

# Instructor guide


## Detailed day schedule

Some example schedules for this lesson: 

2024 edition plan (times in EET, Helsinki time), **no exercises**, just demos: 

- 09:50 - 10:00 Soft start and icebreaker question
    - Page: collaborative notes document
    - Give more space to the icebreaker and see what people are writing and talk about our own experiences
- 10:00 - 10:03 Collab document intro 
- 10:03 - 10:05 Learning outcomes: https://coderefinery.github.io/reproducible-research/ 
- 10:05 - 10:10 Overview of CR and how it all fits together 
    - Page: https://coderefinery.github.io/reproducible-research/intro
    - Learning outcomes from index
- 10:10 - 10:20 Reproducible research, Motivation
    - Exercise in notes doc with the discussions in bottom of motivation page 
    - Page: https://coderefinery.github.io/reproducible-research/motivation/
- 10:20 - 10:30 Organizing your projects
    - Copy the discussion on the notes and if we have time we can highlight some answers
    - Page: https://coderefinery.github.io/reproducible-research/organizing-projects/
- 10:30 - 10:35  ask in collab document and discuss
    - https://coderefinery.github.io/reproducible-research/organizing-projects/#discussion-on-reproducibility
        - Are you using version control for academic papers?
          - ...
          - ...
        - How do you handle collaborative issues e.g. conflicting changes?
          - ...
          - ...
- 10:35 - 10:55 Recording computational steps 
    - Page: https://coderefinery.github.io/reproducible-research/workflow-management/
- 10:55 - 11:05 Real break
- 11:05 - 11:25 Recording dependencies
    - https://coderefinery.github.io/reproducible-research/dependencies/#exercises
        - ask first one in collab doc and discuss on stream
        - show difference between created env from env file vs exported env file on stream
- 11:25 - 11:30 ask in collaborative document
    - Are you using any dependency and/or environment management tool in your work?
        - No: o
            - why not?
                - ..
                - ..
        - Yes: o
            - which?
                - ..
                - ..
    - Have you heard about or been in contact with containers (docker, singularity, podman) in your work? How did you come across them?
        - No: o
        - Yes: 
            - ..
            - ..
            - ..    
- 11:30 - 11:50 Recording environments 
    - The first contact with containers is often: Take this and run this command and then when you need to share/build. 
    - Discuss setup issues, permissions if docker wants root, bandwidth, etc
    - Pros and cons of containers 
    - Demo of two pre-made containers e.g. expand the R studio optional exercise? 
- 11:50 - 12.00 Wrapup 
    - where to go from here: idea would be to give it more practical focus: what to do with these tools? Project level reproducibility. Time-scales of what changes (short time changes of code, long time years changes of OS-s, libraries).
    - Bring your code session advertisement
    - Material + recording available
- 12:00 - long break starts

This is the planned schedule for the workshop in September 2023 (2 hours and 5 minutes including 10 min break) ; note that for this workshop, sharing code and data was moved to social coding lesson:

- 08:50 - 09:00 Soft start and icebreaker question
- 09:00 - 09:10 Overview of CR and how it all fits together
- 09:10 - 09:20 Reproducible research, [Motivation](https://coderefinery.github.io/reproducible-research/motivation/)
- 09:20 - 09:27 [Organizing your projects](https://coderefinery.github.io/reproducible-research/organizing-projects/)
- 09:27 - 09:35 [Recording computational steps](https://coderefinery.github.io/reproducible-research/workflow-management/) - discussion
- 09:35 - 10:00 Snakemake exercise (25 min)
- 10:00 - 10:10 Break
- 10:10 - 10:15 Summary of workflows and the exercise
- 10:15 - 10:30 [Recording dependencies](https://coderefinery.github.io/reproducible-research/dependencies/)
- 10:30 - 10:40 [Recording environments](https://coderefinery.github.io/reproducible-research/environments/)
- 10:40 - 11:00 Container-1 exercise (20 min)
- 11:00 - 11.05 Wrapup

This was the schedule at workshop in March 2023 (2 hours and 15 minutes including 2x 10 min break):

- 08:50 - 09:00 Soft start and icebreaker question
- 09:00 - 09:10 Interview with an invited guest
- 09:10 - 09:20 [Motivation](https://coderefinery.github.io/reproducible-research/motivation/)
- 09:20 - 09:30 [Organizing your projects](https://coderefinery.github.io/reproducible-research/organizing-projects/)
- 09:30 - 10:00 [Recording dependencies](https://coderefinery.github.io/reproducible-research/dependencies/)
   - discussion (5 min)
   - exercise (20 min)
   - discussion (5 min)
- 10:00 - 10:10 Break
- 10:10 - 10:40 [Recording computational steps](https://coderefinery.github.io/reproducible-research/workflow-management/)
   - discussion (5 min)
   - exercise (20 min)
   - discussion (5 min)
- 10:40 - 10:50 [Recording environments](https://coderefinery.github.io/reproducible-research/environments/)
   - an exercise exists but is typically not done as part of a standard workshop
- 10:50 - 11:05 [Sharing code and data](https://coderefinery.github.io/reproducible-research/sharing/)
    - [demo (15 min)](https://coderefinery.github.io/reproducible-research/sharing/#connecting-repositories-to-zenodo)
- 11:05 - 11:15 Break


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
reproducibility, and shows how tools like Snakemake can be used to
both simplify workflows and make them more reproducible.


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


## Typical pitfalls

### Indentation in Snakefiles

- the body of a rule and the body of an input keyword need to be indented, but the number of spaces doesn't matter
This works:
```python
rule all:
    input:
        expand('statistics/{book}.data', book=DATA),
        expand('plot/{book}.png', book=DATA)
```
but this doesn't work:
```python
rule all:
    input:
    expand('statistics/{book}.data', book=DATA),
    expand('plot/{book}.png', book=DATA)
```
nor this:
```python
rule all:
input:
    expand('statistics/{book}.data', book=DATA),
    expand('plot/{book}.png', book=DATA)
```


## Field reports

### 2022 September

We used the strategy "absolutely minimal introductions, most time
for exercise".  Overall, it was probably the right thing to do since
there is so little time and so much to cover.

There wasn't enough time for the conda exercise (we could give only 7
minutes), but also I wonder how engaging it is.  We should look at how
to optimize the start of that episode.

The Snakemake episode went reasonably well.  Our goal was 5 minutes
intro, long exercise, 5 minutes outro.  The intro was actually a bit
longer, and there was the comment that we didn't really explain what
Snakemake was before it started (though we tried).  The start of this
episode should get particular focus in the future, since this is the
main exercise of the day.

