---
layout: episode
title: "Organizing your projects"
teaching: 10
exercises: 5
questions:  
  - "How should we organize files in a research project?"
  - "How can I share and collaborate on research data?"
objectives:
  - "Get overview on how to organize research projects"
  - "Discuss the pros and cons of open science"
keypoints:
  - "Create useful project directory structure"
  - "Set up version control for your projects"
  - "Consider sharing other research outputs"

---

## Directory structure for projects

- It is good to keep all files associated with a project in a single folder
- Different projects should have separate folders
- Use consistent and informative directory structure
- If part public/part private/part secret, separate these by folder (and git repo)
- Add a README file to describe the project and instructions on reproducing the results
- Talk to others in the project about what you do.  Write it down!
- But your mileage may vary, it's not a one-size-fits-all

A project directory can look something like this:
```
project_name/
|-- README.md                    overview of the project
|-- data/                        data files used in the project
|   |-- README.md                describes where data came from
|   |-- sub-folder/              may contain subdirectories
|   |-- ...
|-- processed_data/              intermediate files from the analysis
|-- manuscript/                  your manuscript describing the results
|-- results/                     results of the analysis (including tables and figures)
|-- source/                      contains all code in the project
|   |-- LICENSE                  license for your code
|   |-- requirements.txt         software requirements and dependencies
|   |-- ...

```

## Tracking source code, data and results

- All code is version controlled and goes in the `source/` directory
- Include appropriate LICENSE file and information on software requirements 
- You can also version control data files or input files under `data/`
- If data files are too large (or sensitive) to track, untrack them using `.gitignore`
- Intermediate files from the analysis are kept in `processed_data/`
- Consider using Git tags to track specific versions of results (and/or the code that gives the particular results)
  - version submitted to a journal, the dissertation version, the poster version, etc.
  ```bash
  $ git tag -a <tagname> -m "comment" 
  ```
- It's a good idea to also put your manuscript under version control
- Git can be used to collaborate on manuscripts written in, e.g., LaTeX and other text-based formats but other tools exist:
  - [Overleaf](https://www.overleaf.com/) (has git integration!)
  - [Authorea](https://www.authorea.com/) (apparently also has git integration)
  - Google Docs

## Documenting and automating your workflow

Reproducible workflows enable you to figure out precisely what data and what code were used to generate a result:

 - Provide a historical record (provenance) of data, its origins and causal relationships
 - Can be used to ensure quality of data based on ancestral data, or find sources of errors
 - Allow automated recreation of data
 - Implemented in many [workflow management tools](https://github.com/common-workflow-language/common-workflow-language/wiki/Existing-Workflow-systems) 
 - We will practice reproducible workflows in the next episode

## Sharing research data

The Open Science movement encourages researchers 
to share research output beyond the contents of a 
published academic article (and possibly supplementary information).

 <img src="/reproducible-research/img/Open_Science_Principles.png" style="height: 200px;"/>

Sharing research data has pros and cons [(from Wikipedia)](https://en.wikipedia.org/wiki/Open_science):
- Open access publication of research reports and data allows for rigorous peer-review
- Science is publicly funded so all results of the research should be publicly available
- Open Science will make science more reproducible and transparent
- Open Science has more impact
- Open Science will help answer uniquely complex questions
- Too much unsorted information overwhelms scientists
- Potential misuse
- The public will misunderstand science data
- Increasing the scale of science will make verification of any discovery more difficult
- Low-quality science

### Research data buzzwords

"FAIR" is the current buzzword for data management.  You may be asked
about it in, for example, making data management plans for grants

- **F**indable
  - Will anyone else know that your data exists?
  - Solutions: put it in a standard repository, or at least a
    description of the data.
- **A**ccessible
  - Once someone can know data exists, can they get it?
  - Usually solved by being in a repository, but for non-open data,
    may require more procedures.
- **I**nteroperable
  - Is your data in a format that can be used by others, like csv
    instead of PDF?
  - Or better than csv: Example: [5-star open data](https://5stardata.info/en/)
- **R**eusable
  - Is there a license allowing others to re-use?

Even though this is usually referred to as "open data", it means
considering and making good decisions, even if non-open.

### Exercise: Discuss Open Science
- Do you share any other research outputs besides published articles and possibly source code?
- Discuss pros and cons of sharing research data. 


### Services for sharing and collaborating on research data
- [Zenodo](https://zenodo.org/): A general-purpose open access repository 
  created by OpenAIRE and CERN. Integration with GitHub, allows 
  researchers to upload files up to 50 GB.
- [Figshare](https://figshare.com/): Online digital repository where researchers 
  can preserve and share their research outputs (figures, datasets, images and videos).
  Users can make all of their research outputs available in a citable, 
  shareable and discoverable manner.
- [EUDAT](https://eudat.eu): European platform for researchers and practitioners from any research discipline to preserve, find, access, and process data in a trusted environment.
- [Dryad](https://datadryad.org/): A general-purpose home for a wide diversity of datatypes, 
  governed by a nonprofit membership organization.
  A curated resource that makes the data underlying scientific publications discoverable, 
  freely reusable, and citable.  
- [The Open Science Framework](https://osf.io/): Gives free accounts for collaboration 
  around files and other research artifacts. Each account can have up to 5 GB of files 
  without any problem, and it remains private until you make it public.

