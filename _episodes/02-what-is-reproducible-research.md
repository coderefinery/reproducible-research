---
layout: episode
title: "What is reproducible research"
teaching: 10
exercises: 0
questions:
  - "What does reproducible research mean?"
  - "What tools are available for making research reproducible?"
objectives:
  - "Get a basic idea of different levels of reproducibility"
   
---

## What is reproducible research?

> “reproducibility refers to the ability of a researcher to duplicate the results of a prior study using the same materials as were used by the original investigator. That is, a second researcher might use the same raw data to build the same analysis files and implement the same statistical analysis in an attempt to yield the same results…. Reproducibility is a minimum necessary condition for a finding to be believable and informative.” 
>
> -- <cite> U.S. National Science Foundation (NSF) subcommittee on replicability in science</cite>


- For any research project, an independent researcher should be able to replicate the experiment under the same conditions and obtain the same results.

---

## Main drawbacks of not being able to reproduce research 
- Not able to apply the Software/Code used by the original investigator
- Not able to use the Data used by the author
- No documentation on how data is generated and how the experiment is conducted
- Not able to create software environment (with different libraries) that was originally used to generate results

<!-- - Using same code and data are not necessarily enough for reproducibility. The whole environment needs to be captured. 
-->
## Multiple levels of reproducibility
<img src="/reproducible-research/img/reproducibility_levels.png" style="height: 200px;"/>

- Code level
- Data level
- Environment level
- Documentation level

---
## Multiple tools are available

<img src="/reproducible-research/img/reproducibility_tools.png" style="height: 400px;"/>

- Git, mercurial (code level)
- make, sumatra (data / documentation level)
- Containers (environment level)
 
---
## How we can use these tools to create reproducible workflow?
