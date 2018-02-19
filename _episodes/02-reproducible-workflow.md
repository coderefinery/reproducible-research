---
layout: episode
title: "Creating reproducible workflow"
teaching: 10
exercises: 10
questions:  
  - "How can we create a reproducible workflow?"
  - "How do we repeat an experiment with different data one year later?"
objectives:
  - "Get a basic idea of different approaches for creating reproducible workflows"
  - "You can incorporate some of these tools in your research"
keypoints:
  - Create useful project directory structure
  - Set up version control for your projects
  - Preserve the workflow of generating results
  
---

## Creating a reproducible workflow

Adopting reproducible workflows enables you to figure out precisely what data and what code were used to generate a result
 

### Directory structure for projects

- It is good to keep all files associated with a project in a single folder
- Different project should have separate folders
- Use consistent and informative directory structure (but your mileage may vary)
- Add a README file to describe the project and instructions on reproducing the results
   
A project directory can look something like this:

```bash
project_name/
|-- data/                        contains input data files of our project
|   |-- readme.txt               may contain subdirectories as well
|   |-- sub-folder/
|   |-- ...
|-- manuscript                   will contain the manuscript that we will write to describe the results
|-- results/                     will contain the results of our analysis (including tables and figures)
|-- source/                      will contain all of our code
```


### Tracking source code and data

#### Source code
- Write the core scientific code to perform the analysis, including tests
- Keep the code in the `source` sub-folder
- Track all software/code used in a project in a version control system, for example using Git
- Include appropriate LICENSE file

#### Data files
- You can also track raw data files or input files in version control, placed in the `data` sub-folder 
  - Does it make sense to track generated/processed data?
- Include a README file to describe the data (helping us later)
- If data files are too large or too sensitive to track, one can untrack them using `.gitignore`

As files are added and modified in the project directory, commit your changes frequently as discussed in the [Git introduction](https://coderefinery.github.io/git-intro/).

### Results

- Store the results of the analysis (data files, figures, ...) in the `results` folder
- Consider using Git tags to track specific versions of results (version submitted to a journal, the dissertation version, the poster version, etc.)

```bash
git tag -a <tagname> -m "comment" 
```

#### Manuscript

- It's a good idea to also put your manuscript under version control
- Git can be used to collaborate on manuscripts written in, e.g., LaTeX and other text-based formats but other tools exist:
  - [Overleaf](https://www.overleaf.com/)
  - [Authorea](https://www.authorea.com/)
  - Google Docs


### Documenting and automating the workflow

What steps are followed in creating the results?

#### Provenance of data
   - Provides a historical record of data, its origins and causal relationships
   - Can use it to ensure quality of data based on ancestral data, or find sources of errors
   - Allows automated recreation of data

#### Multiple tools are available for documenting and managing workflows
   - [make](https://www.gnu.org/software/make/), can be used to track the steps we have followed in generating the data
   - [Jupyter](https://jupyter.org/), literate programming, interweaving code, documentation and results
   - [Sumatra](http://sumatra.readthedocs.io/en/0.7.4/), manages and tracks numerical simulations
   - [Snakemake](http://snakemake.readthedocs.io/en/stable/), workflow management system for reproducible and scalable data analyses
   - See [additional tools](#workflow-tools) 
   - [This list of workflow management tools](https://github.com/common-workflow-language/common-workflow-language/wiki/Existing-Workflow-systems) 
     contains over 200 different tools...
   - One problem with workflow tools: "vendor lock-in"

#### Using `make` to automate workflow

- Make is a tool at the heart of many software build systems
- Make uses a domain specific language that the user writes in a Makefile
- Makefile specifies how to build the particular targets from their dependencies

The target/dependencies/command are called as rules

For example:

```makefile
# rule (mind the tab)
target: dependencies
	command(s)
```

We can think of it as follows:
```makefile
outputs: inputs
	command(s)
```



### Type-along exercise: Simple workflow with Git and Make

Let's create an example project which follows the guidelines given above. 
The project is about counting the most frequent characters in a given text and plotting a bar chart of the characters.

> To follow along, clone this [repository](https://github.com/Vathasav/character-count)   

The example project directory is like this:
```bash
character_count/
|-- data/                                
|-- manuscript                           
|-- results/                             
|-- source/
|-- ...                              
```

The input data for the project is in `data/shakespeare.in`. This file contains the text that we want to analyze. 

In addition, we have a following README file:
```bash
Data is gathered from shakespeare.in file found in repository https://github.com/bast/make-pipeline
Date: 12/12/2017
```

and the data directory is like this:
```bash
character_count/
|-- data/
|   |--readme.txt
|   |--shakespeare.in
|-- manuscript                           
|-- ...                            
```

In the `source` directory  we already have two scripts
 - count.py, counts the 10 most frequently used characters in a text 
 - plot.py, plots a bar chart of the results

The project's `source` directory is like this:
```bash
character_count/
|-- data/
|-- manuscript                           
|-- results                             
|-- source
|   |--count.py
|   |--plot.py
|-- ...                              
```

#### Generating results

We extract the 10 most frequently used characters by:

```bash
cat data/shakespeare.in | ./source/count.py > results/charscount.out
```

and generate a bar chart by:
```bash
cat results/charscount.out | ./source/plot.py > results/charsplot.out
```

Let us look at our workflow:

<img src="/reproducible-research/img/wordcount_workflow.png" style="height: 300px;"/>

- In this simple example, we can easily figure out the inputs and ouputs and how they are joined together
- As projects grow, it can become difficult to keep track of all steps of the workflow and how they fit together

Let's re-implement the steps in running character count example using Make.
 
**Step 1**: extract the 10 most frequently used characters in a text

```makefile
results/charscount.out: source/count.py data/shakespeare.in
        cat data/shakespeare.in | ./source/count.py > results/charscount.out
```

The above rule says: I know how to build `results/charscount.out` if I have the `source/count.py` 
script and the `data/shakespeare.in` file, and I do that by calling `source/count.py` on 
`data/shakespeare.in` and redirecting the output

**Step 2**: generate the bar chart
```makefile
results/charsplot.out: source/plot.py results/charscount.out
        cat results/charscount.out | ./source/plot.py > results/charsplot.out
```

**Final step**: we need to build both steps
```makefile
all: results/charscount.out results/charsplot.out
```
   
The whole makefile:
```makefile
all: results/charscount.out results/charsplot.out

results/charscount.out: source/count.py data/shakespeare.in
        cat data/shakespeare.in | ./source/count.py > results/charscount.out

results/charsplot.out: source/plot.py results/charscount.out
        cat results/charscount.out | ./source/plot.py > results/charsplot.out

```


Our example project directory together with the `Makefile` will be like this:
```bash
character_count/
|-- data/
|   |--readme.txt
|   |--shakespeare.in
|-- manuscript                           
|-- results/
|   |--charscount.out
|   |--charsplot.out
|-- source/
|   |--count.py
|   |--plot.py
|--Makefile
```
- Run make (executes the first rule by default) in the cloned directory and see if the results are generated

To summarize:
   - In Makefile, we explicitly define the dependencies of different files needed for executing the workflow
   - Makefile itself can act as a documentation for data generation
   - With a single command we can always generate the results

#### See if we can reproduce the results
- Delete the content in results folder
- Run make and see if we can generate results
- Note: if we have raw data and code, we should be able to regenerate results with a single command



### Exercise: Update Makefile to consider multiple data files

Let's say our requirements have changed and we have to read text from another file (let's say `lorem.in`):
```text
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.
```
- create `lorem.in` file with the above content in `data` folder
- update `readme.txt` to describe where lorem.in comes from
- update `Makefile` to consider multiple input data files
- generate results
- commit changed files and create a new tag

## How to create the environment applied for an experiment?
- Software/code we have used may depend on lots of dependencies and may be difficult to create and use
- Results should be possible to reproduce regardless of platform and with minimal effort
- Many research codes can be problematic to install and configure without experts
- Could we bundle all the necessary dependencies together, so that it is easy to run the software
- Containers can be used to create isolated environments



## References

- This material uses some suggestions from [software carpentry](http://swcarpentry.github.io/2014-03-17-ucb/lessons/jk-python/reproducible_workflow.html) and [software sustainability institute](https://www.software.ac.uk/)
