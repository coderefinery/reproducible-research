---
layout: episode
title: "Motivation"
teaching: 10
exercises: 0
questions:
  - "Should research software and data be reproducible?"
  - "Are they?"
objectives:
  - "Discuss factors affecting reproducibility in research"
keypoints:
  - "Many factors on multiple levels influence reproducibility"
---

<img src="{{ site.baseurl }}/img/research_comic_phd.gif" style="height: 300px;"/>

## A scary anecdote

- A group of researchers obtain great results and submit their work to a high-profile journal.
- Reviewers ask for new figures and additional analysis.
- The researchers start working on revisions and generate modified figures, but find inconsistencies with old figures.
- The researchers can't find some of the data they used to generate the original results, and
  can't figure out which parameters they used when running their analyses.
- The manuscript is still languishing in the drawer ...
  
---

## What is reproducible research?

> “reproducibility refers to the ability of a researcher to duplicate the results of a prior study using the same materials as were used by the original investigator. That is, a second researcher might use the same raw data to build the same analysis files and implement the same statistical analysis in an attempt to yield the same results. Reproducibility is a minimum necessary condition for a finding to be believable and informative.”
>
> -- <cite> U.S. National Science Foundation (NSF) subcommittee on replicability in science</cite>

- For any research project, an independent researcher should be able to replicate an experiment under the same conditions and obtain the same results
  - the same results should be obtained under the same contitions
  - it should be possible to recreate the same conditions!
- "Experiment" is interpreted in a wide sense, encompassing also computational work

---

<!--
   <img src="{{ site.baseurl }}/img/reproducibility_figure.jpg" style="height: 200px;"/>
-->

## Why all the talk about reproducible research?
   - A recent [survey](http://www.nature.com/news/1-500-scientists-lift-the-lid-on-reproducibility-1.19970) in Nature revealed that irreproducible experiments are a problem across all domains of science.
 
 <img src="{{ site.baseurl }}/img/reproducibility_nature.png" style="height: 400px;"/>

---

## Factors behind irreproducible research

- Not enough documentation on how experiment is conducted and data is generated
- Data used to generate original results unavailable
- Software used to generate original results unavailable
- Difficult to recreate software environment (libraries, versions) used to generate original results
   
 <img src="{{ site.baseurl }}/img/Miracle.jpg" style="height: 200px;"/>
 
## Levels of reproducibility

Ensuring that one's research is fully reproducible can be a challenging task,
but multiple tools exist to make it easier.

<img src="{{ site.baseurl }}/img/repro-pyramid.png" style="height: 300px;"/>



> ## Exercise: Examples of non-reproducibility
>
> Computer programs are supposed to be exact and always give the same
> output for the same inputs, so we have perfect reproducibility.  Is
> that true in science?
>
> Discuss with your neighbors.  What are some examples of how software
> can be non-reproducible?  What can be done about it?
>
{: .task}

