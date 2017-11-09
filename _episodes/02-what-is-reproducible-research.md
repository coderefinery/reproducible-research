
---
layout: episode
title: "Making research reproducible"
teaching: 10
exercises: 10
questions:
  - "How to repeat an experiment with different data after one year later?"
  - "How to make results reproducible regardless of platforms with minimal effort?"
objectives:
  - "The goal is to get a basic idea of different tools that can be used to make research reproducible"
  - "You can incorporate some of these tools in your research lifecycle"
keypoints:
  -
 
---

## What is reproducible research?

> “reproducibility refers to the ability of a researcher to duplicate the results of a prior study using the same materials as were used by the original investigator. That is, a second researcher might use the same raw data to build the same analysis files and implement the same statistical analysis in an attempt to yield the same results…. Reproducibility is a minimum necessary condition for a finding to be believable and informative.” 
>
> -- <cite> U.S. National Science Foundation (NSF) subcommittee on replicability in science</cite>


- For any research project, an independent researcher should be able to replicate the experiment under the same conditions and receive the same results.

---

## Main drawbacks of not able to reproduce research 
- Software/code used to produce research
- Data used to produce research
- Documentation on how data is generated
- How to create software environment (with different libraries) the researcher has used?
- Using same code and data are not necessarily enough for reproducibility. The whole environment needs to be captured. 

## Multiple layers of reproducibility
<img src="img/reproducibility_levels.png" style="height: 200px;"/>

- code level
- data level
- Environment level
- documentation level

---
## Multiple tools are available
<img src="img/reproducibility_tools.png" style="height: 400px;"/>

- git, mercurial (code level)
- make, sumatra (data / documentation level)
- Containers (environment level) 
---
##Could we apply the tools used in the workshop to create reproducible research?

### Tracking the software/code we have used in an experiment
- Using git for tracking the code. 
- Multiple ways to track a specific piece of code.
- For example, using git tags to mark a specific piece of code we have used in an experiment
- [ ] Example: use already discussed example in early sessions

### Documentation on data generation  

- As projects grow, it is quite difficult to keep track of all the workflow steps and how they fit together
- How we have generated/created the data in the first case
- The steps we have followed in creating the data
- for example, we can use ```make``` to track the steps we have followed in generating the data
- makefile itself can act as a documentation for data generation
- [ ] Example: use already discussed example in early sessions
- [ ] Example: show overview of sumatra
---

## How to create the environment applied for an experiment?
- Software/code we have used may depend on lot of dependencies and may be difficult to create and use
- Many research softwares can be problematical to install and configure without experts 
- Could we bundle all the necessary dependencies together, so that it is easy to run the software
- Containers can be used to create isolation environments. 

