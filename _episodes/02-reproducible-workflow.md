---
layout: episode
title: "Creating a reproducible workflow"
teaching: 10
exercises: 10
questions:  
  - "How can we create a reproducible workflow?"
  - "How do we repeat an experiment with different data one year later?"
objectives:
  - "Get an overview of different approaches for creating reproducible workflows"
  - "Learn the basics of make"
keypoints:
  - Create useful project directory structure
  - Set up version control for your projects
  - Preserve the workflow of generating results
  
---

## Directory structure for projects

- It is good to keep all files associated with a project in a single folder
- Different projects should have separate folders
- Use consistent and informative directory structure 
- Add a README file to describe the project and instructions on reproducing the results
- But your mileage may vary, it's not a one-size-fits-all

A project directory can look something like this:
```bash
project_name/
|-- data/                        contains input data files of the project
|   |-- README.md                describes where input data came from
|   |-- sub-folder/              may contain subdirectories as well
|   |-- ...
|-- processed_data/              will contain intermediate files from the analysis
|-- manuscript/                  will contain the manuscript describing the results
|-- results/                     will contain the results of the analysis (including tables and figures)
|-- source/                      will contain all code
```

## Tracking source code and data

#### `source/`
- Write the core scientific code to perform the analysis, including tests
- Keep the code in the `source` sub-folder
- Track all code used in a project in a version control system, for example Git
- Include appropriate LICENSE file

#### `data/`
- You can also track raw data files or input files in version control, placed in the `data` sub-folder 
- Include a README file to describe the data (helping us later)
- If data files are too large (or too sensitive) to track, one can untrack them using `.gitignore`

As files are added and modified in the project directory, commit your changes frequently as discussed in the [Git introduction](https://coderefinery.github.io/git-intro/).

#### `processed_data/`
- Intermediate files from the analysis are kept here
- Does it make sense to track generated/processed data?

#### `results/`

- Store the results of the analysis (data files, figures, ...) in the `results` folder
- Consider using Git tags to track specific versions of results (and/or the code that gives the particular results)
  - version submitted to a journal, the dissertation version, the poster version, etc.

```bash
$ git tag -a <tagname> -m "comment" 
```

#### `manuscript/`

- It's a good idea to also put your manuscript under version control
- Git can be used to collaborate on manuscripts written in, e.g., LaTeX and other text-based formats but other tools exist:
  - [Overleaf](https://www.overleaf.com/)
  - [Authorea](https://www.authorea.com/)
  - Google Docs


## Documenting and automating your workflow

Adopting reproducible workflows enables you to figure out precisely what data and what code were used to generate a result.

### Provenance of data
   - Provides a historical record of data, its origins and causal relationships
   - Can use it to ensure quality of data based on ancestral data, or find sources of errors
   - Allows automated recreation of data
   - Directed acyclic graphs (DAGs)
     - representation of data and their provenance
     - nodes can represent data, calculations, etc. - links represent their connections
     - used in many workflow management systems  

### Multiple tools are available for documenting and managing workflows
   - [This list of workflow management tools](https://github.com/common-workflow-language/common-workflow-language/wiki/Existing-Workflow-systems) 
     contains over 200 different tools...

### Using [GNU Make](https://www.gnu.org/software/make/) to automate workflow

- Make is a tool at the heart of many software build systems, but is more general than that
- Make uses a domain specific language that the user writes in a Makefile
- Makefile specifies how to build the particular targets from their dependencies
- Example of command-line automation - easier to ensure reproducibility compared to graphical user interfaces

The target/dependencies/command are called rules

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

Let's look at an example project which follows the guidelines given above. 
The project is about counting the frequency distribution of words in a given text, plotting bar charts and testing 
[Zipf's law](https://en.wikipedia.org/wiki/Zipf%27s_law).

> To follow along, clone this [repository](https://github.com/coderefinery/word-count)

The example project directory is like this:
```bash
word_count/
|-- data/                                
|-- processed_data/                                
|-- manuscript                           
|-- results/                             
|-- source/
|-- ...                              
```

The texts that we want to analyze for the project is in the `data/` directory (four books in plain text).

In addition, we have a LICENSE_TEXTS.md file which contains the license for the texts and their origins. 
Normally, you would instead include a README file describing where the data comes from.

The data directory is like this:
```bash
word_count/
|-- data/
|   |--LICENSE_TEXTS.md
|   |--abyss.txt
|   |--isles.txt
|   |--last.txt
|   |--sierra.txt
|-- ...                            
```

In the `source` directory  we have three scripts:
 - wordcount.py, finds the frequency wdistribution of ords used in a text 
 - plotcount.py, plots a bar chart of the results
 - zipf_test.py, calculates the ratio between the counts of the two most common words

The project's `source` directory is like this:
```bash
word_count/
|-- source
|   |--plotcount.py
|   |--wordcount.py
|   |--zipf_test.py
|-- ...                              
```

#### Generating results

We count the number of times each word appears by:

```bash
$ python source/wordcount.py data/abyss.txt  processed_data/abyss.dat
```

and generate a plot by:
```bash
$ python source/plotcount.py processed_data/abyss.dat results/abyss.png
```

and finally compute the ratio between the frequencies of the two most common words (Zipf's law predicts this ratio to be 2)
```bash
$ python source/zipf_test.py processed_data/abyss.dat > results/results.txt
```

- In simple cases it's easy to figure out what the input is and how results are computed from it
- As projects grow, it becomes more difficult to keep track of all steps of a workflow 
- Shell scripts can be used to automate workflows, but the drawback is that scripts are unaware of dependencies between steps 
  and typically all (possibly time-consuming) steps need to be rerun whenever a single file changes 
- Makefiles are a good choice when there is a need to store the workflow information and create a replicable workflow

#### Writing a Makefile
 
**Step 1**: calculate frequency distribution of words used in a text

```makefile
processed_data/abyss.dat: data/abyss.txt
        python source/wordcount.py data/abyss.txt processed_data/abyss.dat
```

The above rule says: This is how to build `processed_data/abyss.dat` if I have the `source/wordcount.py` 
script and the `data/abyss.txt` inputfile.

**Step 2**: generate the bar chart
```makefile
results/abyss.png: processed_data/abyss.dat
        python source/plotcount.py processed_data/abyss.dat results/abyss.png
```

**Step 3**: calculate the ratio between the two most common words:
```makefile
results/results.txt: processed_data/abyss.dat
        python source/zipf_test.py processed_data/abyss.dat > results/results.txt
```

**Final step**: we need to build all three steps
```makefile
all: processed_data/abyss.dat results/abyss.png results/results.txt
```
   
**Makefile for running the analysis for one input file:**
```makefile
all: processed_data/abyss.dat results/abyss.png results/results.txt

processed_data/abyss.dat: data/abyss.txt
        python source/wordcount.py data/abyss.txt processed_data/abyss.dat

results/abyss.png: processed_data/abyss.dat
        python source/plotcount.py processed_data/abyss.dat results/abyss.png

results/results.txt: processed_data/abyss.dat
        python source/zipf_test.py processed_data/abyss.dat > results/results.txt
```

The Makefile is executed by running make:
```
$ make 
```
This executes the first rule in the Makefile by default, which will trigger the 
execution of all the other rules to build the dependencies of `all`.

#### Advantages of make
 - Ability to conduct partial steps of the workflow, skipping any unnecessary steps
 - Ability to parallelize the jobs, e.g. `$ make -j 2`
 - `Makefile` itself can act as a documentation for data generation
 - With a single command we can generate all or parts of the results 

### Makefile to process all data files

In this project we have three more books to analyze, and in reality we may have many 
more input files and more complicated dependencies.

A more general Makefile for this project can look like this (see `Makefile_all`):

```makefile
SRCDIR := data
TMPDIR := processed_data
RESDIR := results

SRCS = $(wildcard $(SRCDIR)/*.txt)
OBJS = $(patsubst $(SRCDIR)/%.txt,$(TMPDIR)/%.dat,$(SRCS))
OBJS += $(patsubst $(SRCDIR)/%.txt,$(RESDIR)/%.png,$(SRCS))
OBJS += $(RESDIR)/results.txt
DATA = $(patsubst $(SRCDIR)/%.txt,$(TMPDIR)/%.dat,$(SRCS))

all: $(OBJS)

$(TMPDIR)/%.dat: $(SRCDIR)/%.txt
        python source/wordcount.py $<  $@

$(RESDIR)/%.png: $(TMPDIR)/%.dat
        python source/plotcount.py $<  $@

$(RESDIR)/results.txt: $(DATA)
        python source/zipf_test.py $^ > $@

clean:
        @$(RM) $(TMPDIR)/*
        @$(RM) $(RESDIR)/*

.PHONY: clean directories
```

#### Short exercise
- Build all the results using `$ make -f Makefile_all`
- Try removing one of the plots (e.g. `results/abyss.png`) and re-build by re-running `make`. What happens?
- Try removing one of the intermediate results (e.g. `processed_data/abyss.dat`) and re-build. Did you expect this to happen?
- Remove all processed data and results (`$ make -f Makefile_all clean`) and try parallelizing the process with `$ make -j 2`. Is is faster?

