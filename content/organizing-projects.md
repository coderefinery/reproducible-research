# Organizing your projects

```{questions}
- How should we organize files in a research project?
```

```{objectives}
- Get an overview on how to organize research projects
```

```{instructor-note}
- 10 min teaching
- 0 min exercises
```

One of the most basic steps to make your work reproducible is to organize your projects well.  
Let's go over some of the basic things which people have found to work (and not to work).


## Directory structure for projects

- Project files in a **single folder**
- **Different projects** should have **separate folders**
- Use **consistent and informative directory structure**
- If you need to separate public/private/secret, separate these by folder (and Git repo)
- Add a **README file** to describe the project and instructions on reproducing the results
- If a software is reused in several projects it can make sense to put them in own repo

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
  ```console
  $ git tag -a thesis-submitted -m "this is the submitted version of my thesis"
  ```
* We went over all of this in [Git-intro](https://coderefinery.github.io/git-intro/)

---

## Reproducible publications

- Git can be used to collaborate on manuscripts written in, e.g., LaTeX and other text-based formats but other tools exist:
  - [Overleaf](https://www.overleaf.com): an online, collaborative LaTeX editor (has Git integration)
  - [Authorea](https://www.authorea.com): collaborative platform for preprints (apparently also has Git integration)
  - [HackMD](https://hackmd.io/): an online collaborative Markdown editor (has Git integration)
  - [Manuscripts.io](https://www.manuscripts.io/): a collaborative authoring tool that support scientific content and reproducibility.
  - Google Docs can be a good alternative

- Many tools exist to assist in making scholarly output reproducible:
  - [rrtools](https://github.com/benmarwick/rrtools): instructions, templates, and functions for writing a reproducible article or report with R.
  - [Jupyter Notebooks](https://jupyter.org): web-based computational environment for creating code and text based notebooks that can be used as
    supplementary material for articles.
  - [Binder](https://mybinder.org): makes a repository with Jupyter notebooks available in an executable environment (discussed later in the [Jupyter lesson](https://coderefinery.github.io/jupyter/)).
  - ["Research compendia"](http://inundata.org/talks/rstd19/#/): a set of good practices for
    reproducible data analysis in R, but much is transferable to other languages.

```{seealso}
Do you want to practice your reproducibility skills and get inspired by working with other people's code/data? Join a [ReproHack event](https://www.reprohack.org/event/)!
```


---

## Discussion on reproducability

ℹ️ During the workshop we collect answers in the collaborative document.

````{discussion} How do you collaborate on writing academic papers?
- Are you using version control for manuscripts?
- How do you handle collaborative issues eg. conflicting changes?
- How would you like it to work if you could decide?

> Please write or discuss your ideas before opening solution!

```{solution}
- Consider using version control for manuscripts as well. It may help you when keeping track of edits + if you sync it online then you don't have to worry about losing your work.
- Collaboration can be done efficiently by 
  - real time collaboration tools like HackMD/HedgeDoc where conflicts are resolved on yhe fly
  - version control where conflicts are detected and shown – and solved manually
```
````



````{discussion} What tools are you using when organizing your projects?
Write your answers 

```{solution}
Let's look at an [example project](https://github.com/coderefinery/word-count)
which follows the project structure guidelines given above.

This project is about counting the frequency
distribution of words in a given text, plotting results and
testing [Zipf's law](https://en.wikipedia.org/wiki/Zipf%27s_law).
We have subdirectories for raw data, source files, documentation,
processsed data and results, and README and LICENSE files.
- What are the `environment.yml` and `Snakefile` files for?
- Do you think this project is reproducible?

- `environment.yml` specifies dependencies of the project, i.e. all
  packages and their version numbers (discussed later in
  {doc}`dependencies`). The `Snakefile` is a record of all
  computational steps and is used to generate all results with
  `Snakemake` ({doc}`workflow-management`).

- The Word-count project ticks most of the reproducibility boxes!
  - Clear directory structure
  - README file with general project description
  - Documented, with link to ReadTheDocs
  - All dependencies recorded in `environment.yml`
  - Computational steps recorded in `Makefile` and `Snakefile`
```
````


```{keypoints}
- An organized project directory structure helps with reproducibility.
```
