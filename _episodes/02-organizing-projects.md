---
layout: episode
title: "Organizing your projects"
teaching: 5
exercises: 0
questions:
  - "How should we organize files in a research project?"
objectives:
  - "Get overview on how to organize research projects"
keypoints:
  - "An organized project directory structure can help with reproducibility"

---

## Directory structure for projects

- A good starting point is to keep all files associated with a project in a single folder
- Different projects should have separate folders
- Use consistent and informative directory structure
- If you need to separate public/private/secret, separate these by folder (and Git repo)
- Add a README file to describe the project and instructions on reproducing the results
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

- All code is version controlled and goes in the `src/` directory
- Include appropriate LICENSE file and information on software requirements
- You can also version control data files or input files under `data/`
- If data files are too large (or sensitive) to track, untrack them using `.gitignore`
- Intermediate files from the analysis are kept in `processed_data/`
- Consider using Git tags to mark specific versions of results (and/or the code that gives the particular results)
  - version submitted to a journal, the dissertation version, the poster version, etc.
  ```bash
  $ git tag -a <tagname> -m "comment"
  ```
- Git can be used to collaborate on manuscripts written in, e.g., LaTeX and other text-based formats but other tools exist:
  - [Overleaf](https://www.overleaf.com) (has Git integration)
  - [Authorea](https://www.authorea.com) (apparently also has Git integration)
  - Google Docs can be a good alternative
