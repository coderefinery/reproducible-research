---
layout: episode
title: "Recording computational steps"
teaching: 15
exercises: 15
questions:
  - How can we create a reproducible workflow?
  - When to use scientific workflow management systems.
objectives:
  - Discuss pros/cons of GUI vs. manual steps vs. scripted vs. workflow tools.
  - Get familiar with Snakemake.
keypoints:
  - Preserve the steps for re-generating published results.
  - Hundreds of workflow management tools exist.
  - Snakemake is a comparatively simple and lightweight option to create transferable and scalable data analyses.
  - Sometimes a script is enough.
---

## One problem solved in 4 different ways

> The following material is adapted from a [HPC Carpentry lesson](https://hpc-carpentry.github.io/hpc-python/)

If you haven't already done so, please clone the
[word-count project that you imported earlier](../02-organizing-projects/#word-count---an-example-project)
(replace "username"):
```shell
$ git clone https://github.com/username/word-count.git
$ cd word-count
```

The example project directory listing is:
```
.
├── data
│   ├── abyss.txt
│   ├── isles.txt
│   ├── last.txt
│   ├── LICENSE_TEXTS.md
│   └── sierra.txt
├── doc
│   ├── ...
│   ...
├── Dockerfile
├── LICENSE
├── Makefile
├── manuscript
├── matplotlibrc
├── processed_data
├── README.md
├── requirements.txt
├── results
├── Snakefile
└── source
    ├── plotcount.py
    ├── wordcount.py
    └── zipf_test.py
```

In this example we wish to:
1. Analyze word frequencies using `wordcount.py` for 4 books (they are all in the `data` directory).
2. Plot a histogram using `plotcount.py`.
3. Print the ratio between most common and second most common word for all books.

Example (for one book only) - let us test this out:

```
$ python source/wordcount.py data/isles.txt processed_data/isles.dat
$ python source/plotcount.py processed_data/isles.dat processed_data/isles.png
$ python source/zipf_test.py processed_data/isles.dat
```

Can you relate? Are you using similar setups in your research?

This was for one book - how about 3 books? How about 3000 books?

**We will solve this in four different ways and discuss pros and cons.**

---

## Solution 1: Graphical user interface (GUI)

Disclaimer: not all GUIs behave this way - there exist very good GUI solutions which enable
reproducibility and automation.

Imagine we have programmed a GUI with a nice interface with icons where you can select scripts and input files by clicking:
- Click on counting script
- Select book txt file
- Give a name for the dat file
- Click on a run symbol
- Click on plotting script
- Select book dat file
- Give a name for the image file
- Click on a run symbol
- ...
- Go to next book ...
- Click on counting script
- Select book txt file
- ...

---

## Solution 2: Manual steps

It is not too much work:
```
$ python source/wordcount.py data/abyss.txt processed_data/abyss.dat
$ python source/plotcount.py processed_data/abyss.dat processed_data/abyss.png

$ python source/wordcount.py data/isles.txt processed_data/isles.dat
$ python source/plotcount.py processed_data/isles.dat processed_data/isles.png

$ python source/wordcount.py data/last.txt processed_data/last.dat
$ python source/plotcount.py processed_data/last.dat processed_data/last.png

$ python source/wordcount.py data/sierra.txt processed_data/sierra.dat
$ python source/plotcount.py processed_data/sierra.dat processed_data/sierra.png

$ python source/zipf_test.py processed_data/abyss.dat processed_data/isles.dat processed_data/last.dat processed_data/sierra.dat
```

This is **imperative style**: first do this, then to that, then do that, finally do ...

---

## Solution 3: Script

Let's express it more compactly with a shell script (Bash). Let's call it `script.sh`:
```
#!/usr/bin/env bash

# loop over all books
for title in abyss isles last sierra; do
    python source/wordcount.py data/${title}.txt processed_data/${title}.dat
    python source/plotcount.py processed_data/${title}.dat processed_data/${title}.png
done

# this could be done using variables but nevermind
python source/zipf_test.py processed_data/abyss.dat processed_data/isles.dat processed_data/last.dat processed_data/sierra.dat
```

We can run it with:
```
$ bash script.sh
```

This is still **imperative style**: we tell the script to run these steps in precisely this order.

---

## Solution 4: Using [Snakemake](https://snakemake.readthedocs.io/en/stable/index.html)

Snakemake is inspired by [GNU Make](https://www.gnu.org/software/make/),
but based on Python and is more general and has easier syntax.
The workflow below can also be [implemented using make](../extra/make-alternative).

First study the `Snakefile`:

```python
# a list of all the books we are analyzing
DATA = glob_wildcards('data/{book}.txt').book

# this is for running on HPC resources
localrules: all, make_archive

# the default rule
rule all:
    input:
        'zipf_analysis.tar.gz'

# count words in one of our books
# logfiles from each run are put in .log files"
rule count_words:
    input:
        wc='source/wordcount.py',
        book='data/{file}.txt'
    output: 'processed_data/{file}.dat'
    log: 'processed_data/{file}.log'
    shell: 'python {input.wc} {input.book} {output} >> {log} 2>&1'

# create a plot for each book
rule make_plot:
    input:
        plotcount='source/plotcount.py',
        book='processed_data/{file}.dat'
    output: 'results/{file}.png'
    shell: 'python {input.plotcount} {input.book} {output}'

# generate summary table
rule zipf_test:
    input:
        zipf='source/zipf_test.py',
        books=expand('processed_data/{book}.dat', book=DATA)
    output: 'results/results.txt'
    shell:  'python {input.zipf} {input.books} > {output}'

# create an archive with all of our results
rule make_archive:
    input:
        expand('results/{book}.png', book=DATA),
        expand('processed_data/{book}.dat', book=DATA),
        'results/results.txt'
    output: 'zipf_analysis.tar.gz'
    shell: 'tar -czvf {output} {input}'
```

<img src="{{ site.baseurl }}/img/snakemake.png" style="height: 250px;"/>

Snakemake contains rules that relate targets to dependencies and commands:

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


Try it out:
```
$ snakemake --delete-all-output
$ snakemake
```

Snakemake uses **declarative style**: we describe dependencies but we
let Snakemake figure out the series of steps to produce results
(targets). Fun fact: Excel is also declarative, not imperative.

Try running `snakemake` again and observe that and discuss why it refused to rerun all steps:
```
$ snakemake

Building DAG of jobs...
Nothing to be done.
```

Make a modification to a txt or a dat file and run `snakemake` again and discuss
what you see. One way to modify files is to use the `touch` command which will
only update its timestamp:

```
$ touch results/results.txt
$ snakemake
```

### Why Snakemake?

- Gentle learning curve.
- Free, open-source, and installs easily via conda or pip.
- Cross-platform (Windows, MacOS, Linux) and compatible with all HPC schedulers
  - same workflow works without modification and scales appropriately whether on a laptop or cluster.
- [Heavily used in bioinformatics](https://twitter.com/carl_witt/status/1103951128046301185), but is completely general.


### Snakemake vs. Make

- Workflows defined in Python scripts extended by declarative code to define rules:
  - anything that can be done in Python can be done with Snakemake
  - rules work much like in GNU Make (can call any commands/executables)
- Possible to define isolated software environments per rule.
- Also possible to run workflows in Docker or Singularity containers.
- Workflows can be pushed out to run on a cluster or in the cloud without modifications to scale up.


### Visualizing the workflow

We can visualize the directed acyclic graph (DAG) of our current Snakefile
using the `--dag` option, which will output the DAG in `dot` language (a
plain-text format for describing graphs used by [Graphviz software](https://www.graphviz.org/),
which can be installed by `conda install graphviz`)

```bash
$ snakemake --dag | dot -Tpng > dag.png
```
Rules that have yet to be completed are indicated with solid outlines, while already completed rules are indicated with dashed outlines.

<img src="{{ site.baseurl }}/img/snakemake_dag.png" style="height: 300px;"/>

> ## Discussion
>
> Discuss the pros and cons of these different approaches. Which are reproducible? Which scale to hundreds of books and which can it be automated?
{: .challenge}

> ## Exercise using Snakemake
>
> - Start by cleaning all output, and run snakemake.
>   How many jobs are run?
> - Try "touching" the file `data/sierra.txt` and rerun snakemake.
>   Which steps of the workflow are run now, and why?
> - Now touch the file `processed_data/sierra.dat`, and run
>   `snakemake -S`. Can you make sense of the output?
> - Rerun snakemake. Which steps are run, and why?
> - Finally try touching `source/wordcount.py` and rerun snakemake.
>   Which steps are run, and why? Should source codes be considered
>   dependencies?
> - Use the `time` command to see if you get any speedup from
>   executing snakemake rules on multiple cores. For example to run
>   4 parallel threads, use `time snakemake -j 4`.
> - Try archiving the entire workflow with
>   `snakemake --archive my-workflow.tar.gz`.
{: .challenge}

> ## (Optional) Using Snakemake with conda environments
> 
> Let's say that the `make_plot` rule, which runs the 
> `source/plotcount.py` script, requires a separate 
> software environment. 
> - Create an environment file `plotting.yml` in a new directory `envs/`.
>   It should contain `conda-forge` in the `channels` section and the packages
>   `numpy=1.17.3` and `matplotlib=3.1.1` in the `dependencies` section.
> - In the `make_plot` rule in the Snakefile, add a `conda` directive 
>   where you provide the path to the new environment file.
> - First clear all output and then rerun `snakemake` with the `--use-conda` 
>   flag. Observe how snakemake downloads and installs packages and 
>   activates the environment. 
> - The new environment is stored in `.snakemake/conda/$hash` where $hash is 
>   the MD5 hash of the environment file content. Updates to the environment 
>   definition are thus automatically detected.
{: .challenge}



### Graphical user interface

- Snakemake has an experimental GUI feature which can be invoked by:
```
$ snakemake --gui
```

### Integrated package management

- Isolated software environments per rule using conda. Invoke by `snakemake --use-conda`. Example:
```python
rule NAME:
    input:
        "table.txt"
    output:
        "plots/myplot.pdf"
    conda:
        "envs/ggplot.yaml"
    script:
        "scripts/plot-stuff.R"
```

### Snakemake in HPC

- It is possible to address and offload to non-CPU resources:
```
$ snakemake --delete-all-output
$ snakemake -j 4 --resources gpu=1
```

- Transferring your workflow to a cluster:
```
$ snakemake --archive myworkflow.tar.gz
$ scp myworkflow.tar.gz <some-cluster>
$ ssh <some-cluster>
$ tar zxf myworkflow.tar.gz
$ cd myworkflow
$ snakemake -n --use-conda
```

- Interoperability with Slurm:
```json
{
    "__default__":
    {
        "account": "a_slurm_submission_account",
        "mem": "1G",
        "time": "0:5:0"
    },
    "count_words":
    {
        "time": "0:10:0",
        "mem": "2G"
    }
}
```

  The workflow can now be executed by:
```bash
$ snakemake -j 100 --cluster-config cluster.json --cluster "sbatch -A {cluster.account} --mem={cluster.mem} -t {cluster.time} -c {threads}"
```

Note that in this case `-j` does not correspond to the number of cores
used, instead it represents the maximum number of jobs that Snakemake
is allowed to have submitted at the same time.  The `--cluster-config`
flag specifies the config file for the particular cluster, and the
`--cluster` flag specifies the command used to submit jobs on the
particular cluster.

### Running jobs in containers

- Jobs can be run in containers. Execute with `snakemake --use-singularity`. Example:
```python
rule NAME:
    input:
        "table.txt"
    output:
        "plots/myplot.pdf"
    singularity:
        "docker://joseespinosa/docker-r-ggplot2"
    script:
        "scripts/plot-stuff.R"
```

---

- There is a lot more: [snakemake.readthedocs.io](https://snakemake.readthedocs.io/en/stable/).

---

## Comparison and summary

- GUIs may or may not be reproducible.
- Some GUIs can be automated, many cannot.
- Typing the same series of commands for 100 similar inputs is tedious and error prone.
- Imperative scripts are reproducible and great for automation.
- Declarative workflows such as Snakemake are great for longer multi-step analyses.
- Declarative workflows are often easy to parallelize without you changing anything.
- With declarative workflows it is no problem to add/change things late in the project.
- Interesting modern alternative to Make/Snakemake: [https://taskfile.dev](https://taskfile.dev)
- Many [specialized frameworks](https://github.com/common-workflow-language/common-workflow-language/wiki/Existing-Workflow-systems) exist.
