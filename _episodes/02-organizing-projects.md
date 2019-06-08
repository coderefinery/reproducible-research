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
├── README.md			# overview of the project
├── data			# data files used in the project
│   ├── README.md		# describes where data came from
│   └── sub-folder/		# may contain subdirectories
├── processed_data/		# intermediate files from the analysis
├── manuscript/			# manuscript describing the results
├── results/			# results of the analysis (data, tables, figures)
├── source			# contains all code in the project
│   ├── LICENSE			# license for your code
│   ├── requirements.txt	# software requirements and dependencies
│   └── ...
└── doc/			# documentation for your project
    ├── mydocs.rst
    └── ...
```
---

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

---

## Documenting and automating your workflow

Reproducible workflows enable you to figure out precisely what data and what code were used to generate a result:

 - Provide a historical record (provenance) of data, its origins and causal relationships
 - Can be used to ensure quality of data based on ancestral data, or find sources of errors
 - Allow automated recreation of data
 - Implemented in many [workflow management tools](https://github.com/common-workflow-language/common-workflow-language/wiki/Existing-Workflow-systems)
 - We will practice reproducible workflows in the next episode
