---
layout: episode
title: "Creating reproducible workflow"
teaching: 10
exercises: 10
questions:  
  - "How to create a reproducible workflow?"
  - "How to repeat an experiment with different data one year later?"
objectives:
  - "Get a basic idea of different tools that can be used to create reproducible workflow"
  - "You can incorporate some of these tools in your research lifecycle"
keypoints:
  - Create useful project directory structure
  - Setup version control
  - Preserve the workflow of generating results
  
---

## Suggestions for creating a reproducible workflow

One should always be able to figure out precisely what data and what code were used to generate what results.
 

### Create useful directory structure for project

- It is good to keep all the files associated with a project in a single folder
- Make a folder for every project
- Use consistent and informative directory structure (Note: there is no single best way to organize a project)
   
Our project directory can be something like this:

```bash
project_name/
|-- data/                        All input data files of our project
|   |-- readme.txt               may contain subdirectories as well
|   |-- sub-folder/
|   |-- ...
|-- manuscript                   The manuscript folder will contain the manuscript that we will write to describe the results
|-- results/                     The results folder will contain the results of our analysis (including both tables and figures)
|-- source/                      The source folder will contain all of our code
```

- Let's create an example project that will count 10 most frequent characters in a given text and plots a bar chart of the characters
- To follow along, clone this [repository](https://github.com/Vathasav/character-count)   


The example project directory will be like this:
```bash
character_count/
|-- data/                                
|-- manuscript                           
|-- results/                             
|-- source/
|-- ...                              
```

### Using version control to track our changes

- Since we want to track the software/code we have used in our project
- Use version control for tracking this project
- For example, initialize a Git repository 

As you add and modify things in the project directory, you'll want to frequently commit your changes as discussed in the [Git introduction](https://coderefinery.github.io/git-intro/).

### Track data used in the project
- We often start our experiment with a particular data file, or set of data files (i.e., raw data)
- We can track the data files by placing in **data** sub-folder
- Include a readme file to describe the data (which helps us later)
- Note: If we have too large files / sensitive files to track, we can untrack those files using **gitignore**


In the case of character-count example, we already have a data file, i.e., *data/shakespeare.in*. It contains the text that we want to analyze. 

In addition, we have a following readme file:
```bash
Data is gathered from shakespeare.in file found in repository https://github.com/bast/make-pipeline
Date: 12/12/2017
```


Our example project's data directory is like this:
```bash
character_count/
|-- data/
|   |--readme.txt
|   |--shakespeare.in
|-- manuscript                           
|-- ....                             
|-- ....                              
```

### Write code
- Write the core "scientific code" to perform the analysis, including tests
- Keep the code in **source** sub-folder

In the case of character-count example, we already have two scripts:
 - count.py, counts the 10 most frequently used characters in a text 
 - plot.py, plots a bar chart of the results

Our example project's source directory is like this:
```bash
character_count/
|-- data/
|   |--readme.txt
|   |--shakespeare.in
|-- manuscript                           
|-- results                             
|-- source
|   |--count.py
|   |--plot.py
|-- ...                              
```
#### Generate results

- Store the results of the analysis in the results folder

In the case of character-count example, we can extract the 10 most frequently used characters by:

```bash
cat data/shakespeare.in | ./source/count.py > results/charscount.out
```

Generate the bar chart by:
```bash
cat results/charscount.out | ./source/plot.py > results/charsplot.out
```

Let us look at our workflow:

<img src="/reproducible-research/img/wordcount_workflow.png" style="height: 300px;"/>

- In this simple example, we can easily figure out the inputs and ouputs and how they are joined together
- As projects grow, it is quite difficult to keep track of all the workflow steps and how they fit together

### Documenting and automating the workflow

##### It is difficult to track the workflow:
   -  How we have generated/created the results in the first case
   -  What steps are followed in creating the results

#### Provenance of workflow
   - Provides a historical record of data, its origins and causal relationships
   - Can use it to ensure quality of data based on ancestral data, or find sources of errors
   - Allows automated recreation of data

#### Multiple tools are available for documenting and managing the workflow
   - [make](https://www.gnu.org/software/make/), can be used to track the steps we have followed in generating the data
   - [Sumatra](http://sumatra.readthedocs.io/en/0.7.4/), manages and tracks numerical simulations.
   - [Snakemake](http://snakemake.readthedocs.io/en/stable/), a workflow management system to create reproducible and scalable data analyses.
   - See [additional tools](#workflow-tools) 
   
#### Using make to automate workflow

- Make is a tool often at the heart of many software build systems
- Make uses a Domain Specific Language that the user writes in a Makefile
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

Let's re-implement the steps in running character count example using Make.
 
Step 1: extract the 10 most frequently used characters in a text

```makefile
results/charscount.out: source/count.py data/shakespeare.in
        cat data/shakespeare.in | ./source/count.py > results/charscount.out
```

_The above rule says: I know how to build results/charscount.out if I have the source/count.py script and the data/shakespeare.in file, and I do that by calling source/count.py on data/shakespeare.in and redirecting the output_


Step 2: generate the bar chart
```makefile
results/charsplot.out: source/plot.py results/charscount.out
        cat results/charscount.out | ./source/plot.py > results/charsplot.out
```
Final step: we need to build both steps
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


Our example project directory together with Makefile will be like this:
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

### See if we can reproduce the results
- Delete the content in results folder
- Run make and see if we can generate results
- Note: if we have raw data and code, we should be able to regenerate results with a single command

### Other suggestions
- Use git tags to track specific versions (version submitted to a journal, the dissertation version, the poster version, etc.)

```bash
git tag -a <tagname> -m "comment" 
```
- Add a README file to describe the project and instructions on reproducing the results
- Include appropriate LICENSE file

### Exercise: Update Makefile to consider multiple data files
Let's say our requirements have changed and we have to read text from another file (let's say lorem.in):
```text
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.
```
- create lorem.in file with the above content in **data** folder
- update readme.txt to describe where lorem.in comes from
- update make to consider multiple input data files
- generate results
- commit changed files and create a new tag

## How to create the environment applied for an experiment?
- Software/code we have used may depend on lots of dependencies and may be difficult to create and use
- Results should be possible to reproduce regardless of platform and with minimal effort
- Many research codes can be problematic to install and configure without experts
- Could we bundle all the necessary dependencies together, so that it is easy to run the software
- Containers can be used to create isolated environments

### Additional tools for managing workflow {#workflow-tools}

- [Common Workflow Language](https://github.com/common-workflow-language/common-workflow-language), a specification for describing analysis workflows and tools which are portable and scalable across software and hardware environments.
- [Ruffus](https://code.google.com/archive/p/ruffus/), a lightweight python module for running computational pipelines.
- [AiiDA](http://www.aiida.net/), a flexible and scalable informatics' infrastructure to manage, preserve, and disseminate the simulations, data, and workflows of modern-day computational science (electronic structure calculations).
- [Kepler](https://kepler-project.org/), GUI tool to help scientists, analysts, and programmers create, execute, and share models and analyses across a broad range of scientific and engineering disciplines.
- [VisTrails](https://www.vistrails.org/index.php/Main_Page), an open-source scientific workflow and provenance management system that provides support for simulations, data exploration and visualization (GUI).
- [Pegasus](https://pegasus.isi.edu/), workflow management system to automate, recover, and debug scientific computations (command line and browser interface tool automating).

## References

- This material uses some suggestions from [software carpentry](http://swcarpentry.github.io/2014-03-17-ucb/lessons/jk-python/reproducible_workflow.html) and [software sustainability institute](https://www.software.ac.uk/)
