# Recording computational steps

```{questions}
- How can we create a reproducible workflow?
- When to use scientific workflow management systems.
```

```{objectives}
- Discuss pros/cons of GUI vs. manual steps vs. scripted vs. workflow tools.
- Get familiar with Snakemake.
```

```{instructor-note}
- 15 min teaching
- 15 min exercises
```

## One problem solved in 4 different ways

> The following material is partly derived from a [HPC Carpentry lesson](https://hpc-carpentry.github.io/hpc-python/)

In this episode we will work with reproducible workflows for the programs and data in the repository [word-count](https://github.com//coderefinery/word-count). The computing environment needed for performing the exercises can be performed on your own computer as well as on a cloud service.

```{prereq} Exercise preparation
**On your own computer**:
- Activate the [coderefinery conda environment](https://coderefinery.github.io/installation/conda-environment/) with `conda activate coderefinery`.
- Create an exercise repository in your own namespace by
  [generating from a template](https://help.github.com/en/articles/creating-a-repository-from-a-template)
  using this template: <https://github.com//coderefinery/word-count>
  called `word-count`
- Clone the word-count repository with `git clone `.

**On Binder**:
We can also use the cloud service [Binder](https://mybinder.org/) 
to make sure we all have the same computing environment.
This is interesting from a reproducible research point of view and it's explained further in the [Jupyter lesson](https://coderefinery.github.io/jupyter/sharing/) how this is even possible.
- Go to [https://mybinder.org/](https://mybinder.org)
- In the box **GitHub repository name or URL** enter: [https://github.com/coderefinery/word-count](https://github.com/coderefinery/word-count)
- Click on the **Launch** button.
- Once it get started, you can open a new Terminal from the **new** menu (top right) and select **Terminal**.
```

The word count project directory listing is:
```
.
├── binder
│   ├── environment.yml
├── data
│   ├── abyss.txt
│   ├── isles.txt
│   ├── last.txt
│   ├── LICENSE_TEXTS.md
│   └── sierra.txt
├── doc
│   ├── ...
│   ...
├── LICENSE
├── Makefile
├── manuscript
├── matplotlibrc
├── processed_data
├── README.md
├── environment.yml
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
The workflow below can also be [implemented using make](make-alternative).

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

Snakefiles contain rules that relate targets (`output`) 
to dependencies (`input`) and commands (`shell`).
Let's try it out. Since version 5.11 one needs to specify number 
of cores (or jobs) using `-j`, `--jobs` or `--cores`:
```
$ snakemake --delete-all-output -j 1
$ snakemake -j 1
```

Snakemake uses **declarative style**: we describe dependencies but we
let Snakemake figure out the series of steps to produce results
(targets). Fun fact: Excel is also declarative, not imperative.

Try running `snakemake` again and observe that and discuss why it refused to rerun all steps:
```
$ snakemake -j 1

Building DAG of jobs...
Nothing to be done.
```

Make a modification to a txt or a dat file and run `snakemake` again and discuss
what you see. One way to modify files is to use the `touch` command which will
only update its timestamp:

```
$ touch results/results.txt  # make it look like the file has been changed
$ snakemake -j 1
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

### Visualizing the workflow

We can visualize the directed acyclic graph (DAG) of our current Snakefile
using the `--dag` option, which will output the DAG in `dot` language.

**Note**: This requires the [Graphviz software](https://www.graphviz.org/),
which can be installed by `conda install graphviz`). It's not necessary to 
run this step yourself.

```bash
$ snakemake -j 1 --dag | dot -Tpng > dag.png
```
Rules that have yet to be completed are indicated with solid outlines, while already completed rules are indicated with dashed outlines.

```{figure} img/snakemake_dag.png
:alt: Snakemake DAG
:width: 100%
```

````{discussion} Discussion
Discuss the pros and cons of these different approaches. Which are reproducible? Which scale to hundreds of books and which can it be automated?

```{solution}
- GUIs may or may not be reproducible.
- Some GUIs can be automated, many cannot.
- Typing the same series of commands for 100 similar inputs is tedious and error prone.
- Imperative scripts are reproducible and great for automation.
- Declarative workflows such as Snakemake are great for longer multi-step analyses.
- Declarative workflows are often easy to parallelize without you changing anything.
- With declarative workflows it is no problem to add/change things late in the project.
- Interesting modern alternative to Make/Snakemake: [https://taskfile.dev](https://taskfile.dev)
- Many [specialized frameworks](https://github.com/common-workflow-language/common-workflow-language/wiki/Existing-Workflow-systems) exist.
```
````


- There is a lot more: [snakemake.github.io](https://snakemake.github.io/).

---

(using-snakemake)=

### Exercise - Using Snakemake

````{exercise} Workflow-1: Using Snakemake
Having followed the "Exercise preparation" above, make sure that you are in the `word-count` repository.

1. Start by cleaning all output with `snakemake --delete-all-output -j 1`. 
2. Run `snakemake -j 1`. How many jobs are run?
3. Try "touching" the file `data/sierra.txt` (`touch data/sierra.txt` 
   (unix/git bash) or `copy /b data\sierra.txt +,,` (windows cmd /anaconda prompt) ) 
   and rerun snakemake. This makes it look like the file has changed as its 
   timestamp is updated.  
   Which steps of the workflow are run now, and why? 
4. Now touch the file `processed_data/sierra.dat` to update the
   timestamp, and run
   `snakemake -S` (-S stands for summary). Can you make sense of the output?
5. Rerun snakemake. Which steps are run, and why?
6. Finally try touching `source/wordcount.py` and rerun snakemake.
   Which steps are run, and why? Should source codes be considered
   dependencies?
7. Use the `time` command to see if you get any speedup from
   executing snakemake rules on multiple cores. For example to run
   4 parallel threads, use `time snakemake -j 4`.
8. Try archiving the entire workflow with
   `snakemake -j 1 --archive my-workflow.tar.gz`.

```{solution}
1. `snakemake --delete-all-output -j 1`, where `-j 1` (you could also
   use `--cores 1` instead) specifies the number of CPU cores used for
   execution. It should display something like *deleting x*, while
   deleting previously created files (if you ran this before, otherwise
   nothing). 
2. Then run the process again with `snakemake -j 1`. 
   If everything went well, it should have run 11
   jobs in total. Most rules have run once, but count_words and make_plot 
   are run 4 times each (once for each input book). In the text printed below this
   in your terminal you can see when each job was run and what was done
   in each job. 
3. `touch data/sierra.txt` (unix/git bash) or `copy /b data\sierra.txt
   +,,` (windows cmd /anaconda prompt): this command updates the
   timestamp of the file, for the program it looks like the file has been
   updated/changed and will need to be reprocessed by all following steps
   that are depending on this output (i.e. that use this output to do
   something else with it). So, once you call `snakemake -j 1` again,
   only the jobs concerning the sierra dataset will be rerun, not all the
   processes of unchanged files. Snakemake determines which of the
   following processing steps will need to be rerun once an input file is
   updated. Hence e.g. make_plot is also rerun, since its input (the
   output of count_words) 'changed'.
4. `touch processed_data/sierra.dat` (unix/git bash) or `copy /b
   processed_data/sierra.dat +,,` (windows cmd /anaconda prompt), then
   run `snakemake -S` (-S stands for summary). This does not run any jobs
   but gives an overview of what is the status (status column) of each
   step and what will be run the next time snakemake is run (plan
   column). Note that the column headers may appear not right above the
   columns below, check spaces to connect columns with their column
   names). Also note, that the default rule 'all' is not shown in
   summary.
5. `snakemake -j 1`. 4 jobs are run. You may have expected 3 as in the
   summary only 3 steps had the *upadte pending* planned. However, as
   mentioned above, the default rule 'all' was not shown in summary and
   also needs to be executed in order to run the following steps.
6. `touch source/wordcount.py` (unix/git bash) or `copy /b
   source/wordcount.py +,,` (windows cmd /anaconda prompt), then
   `snakemake -j 1`. Until now we only 'changed' the output files. Here
   we actually 'change' a script that produces these output files. Since
   the wordcount.py is the very first script in the workflow on whose
   results all other processes depend on, everything is run again. By
   updating the scripts timestamp, snakemake assumes something has
   changed in the scripts that may influence the output of the script,
   and therefore also the output of every following step. Therefore it
   will run all the following steps again. In this case if you would
   actually change something in the wordcount.py script it would change
   the output, which means if you want your research to be reproducible,
   the source code as is has to be a dependency to get the same results
   as you did now.
7. The speedup achieved with running on 4 instead of 1 core might be
   small but it should still exist is terms of time. The example is only
   small, but when running tasks where each step takes much longer to
   run, this is one possible way of speeding things up.
8. For more information on archiving, see [the official documentation](https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html#sustainable-and-reproducible-archiving)
```
````

(snakemake-with-conda-environments)=

### Exercise - Snakemake with conda environments

`````{exercise} (Optional) Workflow-2: Snakemake and Conda

Let's say that the `make_plot` rule, which runs the 
`source/plotcount.py` script, requires a separate 
software environment. 
1. Create an environment file `plotting.yml` in a new directory `envs/`.
   It should contain `conda-forge` in the `channels` section and the packages
   `numpy=1.17.3` and `matplotlib=3.1.1` in the `dependencies` section.
2. In the `make_plot` rule in the Snakefile, add a `conda` directive 
   where you provide the path to the new environment file.
3. First clear all output and then rerun `snakemake` with the
   `--use-conda --conda-frontend conda` flags (the latter is needed because `snakemake` prefers to use the `mamba` replacement for `conda`). Observe how snakemake downloads and installs
   packages and activates the environment. The new environment is
   stored in `.snakemake/conda/$hash` where $hash is the MD5 hash of
   the environment file content. Updates to the environment definition
   are thus automatically detected.

````{solution}
1. Checkout the [Anaconda
   documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-file-manually)
   on how to manually create a yml file. Make sure to create the
   `plotting.yml` file in the right directory. Open your preferred
   editor, and add the following:
   ```
   name: plotting
   channels:
     - conda-forge
   dependencies:
     - numpy=1.17.3
     - matplotlib=3.1.1
   ```
2. The make plot part of the snakemake file should be something like this:
   ```
   ...
   # create a plot for each book
   rule make_plot:
      input:
          plotcount='source/plotcount.py',
          book='processed_data/{file}.dat'
      output: 'results/{file}.png'
      conda: "envs/plotting.yml"
      shell: 'python {input.plotcount} {input.book} {output}'
   ...
   ```

3. First, run `snakemake --delete-all-output -j 1` to clear all
   output. Then, run `snakemake --use-conda --conda-frontend conda -j 1`. Snakemake now finds
   the envs/plotting.yml file and executes the make_plot rule inside a conda environment.
````
`````

(snakemake-in-hpc)=

### Exercise - Snakemake on High Performance Computers

````{exercise} (Optional) Workflow-3: Snakemake on HPC
- On a cluster node, Snakemake uses as many cores as available on that node. If a program that is run in a rule can only run efficiently up to a given number of CPU threads, it's possible to manually set a maximum in the rule definition:
```
rule count_words:
    input:
        wc='source/wordcount.py',
        book='data/{file}.txt'
    output: 'processed_data/{file}.dat'
    threads: 4
    log: 'processed_data/{file}.log'
    shell: 'python {input.wc} {input.book} {output} >> {log} 2>&1'
```    
- Transferring your workflow to a cluster:
```
$ snakemake --archive myworkflow.tar.gz -j 1
$ scp myworkflow.tar.gz <some-cluster>
$ ssh <some-cluster>
$ tar zxf myworkflow.tar.gz
$ cd myworkflow
$ snakemake -n --use-conda -j 1
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
````


---



```{keypoints}
  - Preserve the steps for re-generating published results.
  - Hundreds of workflow management tools exist.
  - Snakemake is a comparatively simple and lightweight option to create transferable and scalable data analyses.
  - Sometimes a script is enough.
```
