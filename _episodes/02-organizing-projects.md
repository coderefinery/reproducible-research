---
layout: episode
title: "Organizing your projects"
teaching: 10
exercises: 0
questions:
  - "How should we organize files in a research project?"
objectives:
  - "Get overview on how to organize research projects"
keypoints:
  - "An organized project directory structure can help with reproducibility."

---

## Directory structure for projects

- A good starting point is to keep all files associated with a project in a **single folder**
- **Different projects** should have **separate folders**
- Use **consistent and informative directory structure**
- If you need to separate public/private/secret, separate these by folder (and Git repo)
- Add a **README file** to describe the project and instructions on reproducing the results
- Talk to others in the project about what you do and write it down
- Your mileage may vary: it's not a one-size-fits-all
- When software is reused in several projects it can make sense to put them in own repo

A project directory can look something like this:
```shell
project_name/
├── README.md             # overview of the project
├── data/                 # data files used in the project
│   ├── README.md         # describes where data came from
│   └── sub-folder/       # may contain subdirectories
├── processed_data/       # intermediate files from the analysis
├── manuscript/           # manuscript describing the results
├── results/              # results of the analysis (data, tables, figures)
├── src/                  # contains all code in the project
│   ├── LICENSE           # license for your code
│   ├── requirements.txt  # software requirements and dependencies
│   └── ...
└── doc/                  # documentation for your project
    ├── index.rst
    └── ...
```
---

## Tracking source code, data, and results

- All code is version controlled and goes in the `src/` or `source/` directory
- Include appropriate LICENSE file and information on software requirements
- You can also version control data files or input files under `data/`
- If data files are too large (or sensitive) to track, untrack them using `.gitignore`
- Intermediate files from the analysis are kept in `processed_data/`
- Consider using Git tags to mark specific versions of results (version
  submitted to a journal, dissertation version, poster version, etc.):
```bash
$ git tag -a thesis-submitted -m "this is the submitted version of my thesis"
```

---

## Reproducible publications

- Git can be used to collaborate on manuscripts written in, e.g., LaTeX and other text-based formats but other tools exist:
  - [Overleaf](https://www.overleaf.com) (has Git integration)
  - [Authorea](https://www.authorea.com) (apparently also has Git integration)
  - Google Docs can be a good alternative

- Many tools exist to assist in making scholarly output reproducible:
  - [rttols](https://github.com/benmarwick/rrtools): Instructions, templates, and functions for making a basic compendium suitable for writing a reproducible journal article or report with R.
  - [Jupyter Notebooks](https://jupyter.org): Web-based interactive
    computational environment for creating notebook documents. Can be used for
    supplementary material with journal articles.
  - [Binder](https://mybinder.org): Make a repository with Jupyter
    notebooks available in an executable environment.
  - ["Research compendia"](http://inundata.org/talks/rstd19/#/): A set of good practices for 
    reproducible data analysis in R, but much is transferable to other languages.

- Do you want to practice your reproducibility skills and get inspired by working with other 
  people's code/data? Join a [ReproHack event](https://github.com/reprohack/reprohack-hq)!

---

> ## Discussion: How do you collaborate on writing academic papers?
>
> - Are you using version control?
> - How do you handle collaborative issues?
> - How would you like it to work if you could decide?
{: .discussion}

> ## Word count - an example project
>
> Let's look at an [example project](https://github.com/coderefinery/word-count) 
> which follows the project structure guidelines given above. 
> - Since we'll continue working with this repo, **import** it to your GitHub namespace 
>   by clicking "Use this template".
> This project is about counting the frequency
> distribution of words in a given text, plotting results and
> testing [Zipf's law](https://en.wikipedia.org/wiki/Zipf%27s_law).  
> We have subdirectories for raw data, source files, documentation,
> processsed data and results, and README and LICENSE files.
> - What are the `requirements.txt`, `Dockerfile`, and `Snakefile` files for?
> - Do you think this project is reproducible?
{: .challenge}
