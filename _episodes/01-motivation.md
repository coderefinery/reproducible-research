---
layout: episode
title: "Motivation"
teaching: 5
exercises: 0
questions:
  - "Why should research be reproducible?"
  - "What tools are available for making research reproducible?"
objectives:
  - "Discuss reasons for why research should be reproducible"
  - "Get a basic idea of different levels of reproducibility"   

---

## Food for thought

Mark and Mary are researchers at a university. They got some great results, which they submitted to a high-profile journal. The reviews were positive, but reviewers asked for some new figures, alternative analysis and a change to existing figures.
Mark and Mary started to work on revisions, but when they tried to generate modified figures, it didn't match with previous results. The new figures were different from what they found before and didn't show the same trends. Mary usually keeps track of which code has generated which figures, but she was in a rush to submit the paper before a deadline. She forgot to keep track of the files as usual.
Mary has left university for a job in industry and ever since the manuscript is languishing in the drawer.
  
---

## What is reproducible research?

> “reproducibility refers to the ability of a researcher to duplicate the results of a prior study using the same materials as were used by the original investigator. That is, a second researcher might use the same raw data to build the same analysis files and implement the same statistical analysis in an attempt to yield the same results…. Reproducibility is a minimum necessary condition for a finding to be believable and informative.” 
>
> -- <cite> U.S. National Science Foundation (NSF) subcommittee on replicability in science</cite>

- For any research project, an independent researcher should be able to replicate the experiment under the same conditions and obtain the same results.

---

In many cases, we have to start from existing work.

<img src="/reproducible-research/img/research_comic_phd.gif" style="height: 300px;"/>

---

## Factors behind irreproducible research 

- Not enough documentation on how experiment is conducted and data is generated 
- Data used to generate original results unavailable
- Software used to generate original results unavailable
- Difficult/impossible to recreate software environment (libraries, versions) used to generate original results


## Why reproducible research?

 - Demonstrating correctness of results
 - Long-term value of data
 - Uniqueness of data, i.e., data collected today may be invalid/inappropriate 6 months
   from now
 - Publishing 2 years after data collection and analysis ends
 - Repeating the same experiment with different data and settings, many months later 
 - Saves a lot of time in transmitting knowledge to future researchers
   
<!--
   <img src="/reproducible-research/img/reproducibility_figure.jpg" style="height: 200px;"/>
-->
   
## Why all the talk about reproducible research?
   - A recent [survey](http://www.nature.com/news/1-500-scientists-lift-the-lid-on-reproducibility-1.19970) in Nature revealed that irreproducible experiments are a problem across all domains of science.
 
 <img src="/reproducible-research/img/reproducibility_nature.png" style="height: 400px;"/>
   
 
## Multiple levels of reproducibility
<img src="/reproducible-research/img/reproducibility_levels.png" style="height: 200px;"/>

- Code level
- Data level
- Environment level
- Documentation level (documenting the workflow)

---
## Multiple tools are available

<img src="/reproducible-research/img/reproducibility_tools.png" style="height: 400px;"/>

- Git, mercurial (code level)
- Git or mercurial, sumatra (data level)
- make, sumatra (documentation level)
- Containers (environment level)
- [Jupyter notebooks](http://jupyter.org/), [R Markdown](http://rmarkdown.rstudio.com/) (article/report level)
 
---
## How we can use these tools to create reproducible workflow?
   
   
