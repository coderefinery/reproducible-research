---
layout: episode
title: "Workflow management tools"
teaching: 15
exercises: 25
questions:
  - "How can we create a reproducible workflow?"
  - "What are scientific workflow management systems?"
objectives:
  - "Get familiar with Make and Snakemake"
keypoints:
  - "Preserve the workflow of generating results"
  - "Hundreds of workflow management tools exist"
  - "Make and Snakemake are a comparatively simple and lightweight options to create transferable and scalable data analyses"
   
---

# Scientific workflows

- Orchestrated and repeatable pattern for a series of computational or data manipulation steps.
- Typical homemade workflows: series of scripts that read data and input, call programs and produce outputs.
- [Many specialized frameworks exist](https://github.com/common-workflow-language/common-workflow-language/wiki/Existing-Workflow-systems) 
  for managing scientific workflows
  - environments to create and execute workflows and monitor results
  - enable sharing and reusing workflows
  - enable tracking the provenance of workflow results 
  - can enable scaling across nodes, clusters, cloud
  - each has its own specialities, benefits and user communities
  - the [common workflow language (CWL)](http://www.commonwl.org) tries to 
    overcome "vendor lock-in"
    

## [GNU Make](https://www.gnu.org/software/make/)

- Old tool often used to build software.
- Uses specific syntax that the user writes in a Makefile.
- Makefile specifies how to build targets from their dependencies.
- Example of command-line automation - can be easier to ensure reproducibility compared to GUIs.

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

#### Advantages of make
 - Ability to conduct partial steps of the workflow, skipping any unnecessary steps
 - Ability to parallelize the jobs, e.g. `$ make -j 2`
 - Makefile itself can act as a documentation for data generation
 - With a single command we can generate all or parts of the results 

> We will now switch to Snakemake, but a similar step-by-step guide to Make is [given below](#make).

## [Snakemake](https://snakemake.readthedocs.io/en/stable/index.html)

#### Why Snakemake?
- Gentle learning curve.
- Free, open-source, and installs easily via pip.
- Cross-platform (Windows, MacOS, Linux) and compatible with all HPC schedulers
  - same workflow works without modification and scales appropriately whether on a laptop or cluster .
- Heavily used in bioinformatics, but is completely general.

#### Snakemake vs. make

- Workflows defined in Python scripts extended by declarative code to define rules:
  - anything that can be done in Python can be done with Snakemake
  - rules work much like in GNU Make (can call any commands/executables)
- Possible to define isolated software environments per rule.
- Also possible to run workflows in Docker or Singularity containers.
- Workflows can be pushed out to run on a cluster or in the cloud without modifications to scale up.

<br>
<img src="/reproducible-research/img/snakemake.png" style="height: 250px;"/>



### Simple workflow with Snakemake

> The following material is adapted from a [HPC Carpentry lesson](https://hpc-carpentry.github.io/hpc-python/)

Let's look at an example project which follows the project structure guidelines given in the previous episode.
The project is about counting the frequency distribution of words in a given text, plotting bar charts and testing 
[Zipf's law](https://en.wikipedia.org/wiki/Zipf%27s_law).

> To follow along, **fork and clone** this [repository](https://github.com/coderefinery/word-count):
> ```shell
> $ git clone https://github.com/user/word-count.git
> ```

The example project directory is like this:
```bash
word_count/
|-- data/                                
|-- processed_data/                                
|-- manuscript                           
|-- results/                             
|-- source/
|-- README.md
|-- requirements.txt
|-- license.md
|-- ...                              
```

Note that we include a README, a requirements file with software dependencies, and a license file.

The texts that we want to analyze for the project is in the `data/` directory (four books in plain text), 
along with LICENSE_TEXTS.md which contains the license for the texts and their origins. 

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
 - `wordcount.py`, finds the frequency distribution of words used in a text 
 - `plotcount.py`, plots a bar chart of the results
 - `zipf_test.py`, calculates the ratio between the counts of the two most common words

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

- In simple cases it's easy to figure out what the input is and how results are computed from it.
- As projects grow, it becomes more difficult to keep track of all steps of a workflow.
- Shell scripts can be used to automate workflows
  - drawback: scripts are unaware of dependencies between steps 
    and typically all (possibly time-consuming) steps need to be rerun whenever a single file changes.
- Build files for make and snakemake can store the workflow information and create a replicable workflow.

#### Defining rules

We create a file called `Snakefile` with the following contents:
```python
# Count words.
rule count_words:
    input: 'data/isles.txt'
    output: 'processed_data/isles.dat'
    shell: 'python source/wordcount.py data/isles.txt processed_data/isles.dat'
```
and run it with
```bash
$ snakemake
```
and get
```bash
Building DAG of jobs...
Using shell: /bin/bash
Provided cores: 1
Rules claiming more threads will be scaled down.
Job counts:
    count	jobs
    1		count_words
    1

rule count_words:
    input: data/isles.txt
    output: processed_data/isles.dat
    jobid: 0

Finished job 0.
1 of 1 steps (100%) done
```

What just happened? 
The rule told Snakemake how to build the **target** `processed_data/isles.dat` using the **action** `source/wordcount.py` 
and the **dependency** `data/isles.txt`.

Let's try to build another target by adding a new rule (with a unique name) to the Snakefile:

```python
rule count_words_abyss:
     input:  'data/abyss.txt'
     output: 'processed_data/abyss.dat'
     shell:  'python source/wordcount.py data/abyss.txt processed_data/abyss.dat'
```
and try running `snakemake` again. It gives

```bash
Nothing to be done.
```

This is because `snakemake` (like `make`) only tries to build the first rule in the Snakefile. 
But we can build the new target by

```bash
$ snakemake processed_data/abyss.dat
```

#### Building all targets

To generalize, we need a rule to create all the data files. 
This rule should be at the *top* of the Snakefile so that it is the default target:

```python
rule alldata:
     input:
         'processed_data/isles.dat',
         'processed_data/abyss.dat'
```

- Dependencies (inputs) of this rule are targets (outputs) of other rules. 
  Snakemake will 
  check to see if the dependencies exist and, if not, will check if rules 
  are defined that will create them and invoke those first. 
- An example of a rule that has no actions - used only to trigger the build of its dependencies if needed
- Dependencies must form a directed acyclic graph (DAG) - cyclic dependencies will not work

#### Cleaning up

It's useful to have a rule to remove all data files to be able to explicitly recreate them. 
It can be called `clean`, as this is a common name for rules that delete auto-generated files:

```python
rule clean:
    shell: 'rm -f processed_data/*.dat'
```

This rule can be run by `$ snakemake clean`.

#### Visualizing the workflow

We can visualize the DAG of our current Snakefile using the `--dag` option, which will output the DAG 
in `dot` language (a plain-text format for describing graphs used by [Graphviz software](https://www.graphviz.org/), 
which can be installed by `conda install graphviz`)

```bash
$ snakemake --dag | dot -Tpng > dag.png
```
Rules that have yet to be completed are indicated with solid outlines, while already completed rules are indicated with dashed outlines.

<img src="/reproducible-research/img/snakemake_simpledag.png" style="height: 150px;"/>

#### Testing before running

There is also an option to print out all commands that will be run (`-p`), and 
another to perform a dry-run (`-n`):

```bash
$ snakemake clean
$ snakemake -n -p
```

```bash
Job counts:
    count	jobs
    1		alldata
    1		count_words
    1		count_words_abyss
    3

rule count_words:
    input: data/isles.txt
    output: processed_data/isles.dat
    jobid: 2

python source/wordcount.py data/isles.txt processed_data/isles.dat

rule count_words_abyss:
    input: data/abyss.txt
    output: processed_data/abyss.dat
    jobid: 1

python source/wordcount.py data/abyss.txt processed_data/abyss.dat

localrule alldata:
    input: processed_data/isles.dat, processed_data/abyss.dat
    jobid: 0

Job counts:
    count	jobs
    1		alldata
    1		count_words
    1		count_words_abyss
    3
```

### Exercise: Building a workflow with Snakemake

1. Write a new rule for `last.dat,` created from `data/last.txt`, and 
   update the `alldata` rule with this target. Run `snakemake`.
2. The `touch` command updates the modification time of a file, in the 
   same way as if you modified and saved the file.
    - What steps does Snakemake perform if you modify the processed data?
    ```bash
    $ touch processed_data/abyss.dat
    $ snakemake 
    ```
    - What if you instead modify the raw data?
    ```bash
    $ touch data/abyss.txt
    $ snakemake 
    ```
    - What if you modify the source code? Is this correct?
    ```bash
    $ touch source/wordcount.py
    $ snakemake
    ```
      - Add the missing dependency to the appropriate rules!

3. Write a new rule for `results.txt,` which creates a table with results from 
   analysis of Zipf's law.
  - It needs to depend upon each of the three .dat files, and the source file.
  - It should invoke the action:
  ```python
python source/zipf_test.py processed_data/abyss.dat processed_data/isles.dat processed_data/last.dat > results/results.txt
  ```
  - Put this rule at the top of the Snakefile so that it is the default target.
  - Update clean so that it removes results.txt.
  - Now run `snakemake` (you can test it with a dry-run first)

4. Snakemake can execute rules in parallel with the flag `-j N`, where `N` 
   is the number of cores used. Try timing `snakemake` with the `time` 
   command (`time snakemake ...`) and compare running with 1, 2 and 3 cores 
   (remember to clean the output in between).

5. (OPTIONAL) Create a new rule to plot one of the processed 
   datafiles using the command 
   ```python
   python source/plotcount.py processed_data/abyss.dat results/abyss.png
   ```
   - Make sure that when you run the workflow from scratch (after cleaning), 
     both the plot and the results.txt file get generated.

### Wildcards 

The Snakefile created above contains a lot of unnecessary 
repetition which requires lots of typing and is error-prone.
*Wildcards* can be used to avoid this situation.
For example, the following code block:
```python
rule zipf_test:
     input:
         'processed_data/isles.dat',
         'processed_data/abyss.dat',
         'processed_data/last.dat'
     output:
         'results/results.txt'
     shell:
         'python source/zipf_test.py processed_data/isles.dat processed_data/abyss.dat processed_data/last.dat > results/results.txt'
```

can be replaced by 
```python
rule zipf_test:
     input:
         'processed_data/isles.dat',
         'processed_data/abyss.dat',
         'processed_data/last.dat'
     output:
         'results/results.txt'
     shell:
         'python source/zipf_test.py {input} > {output}'
```

Let's test if this works:
```bash
$ snakemake clean
$ snakemake 
```

```bash
... [more output] ...
rule zipf_test:
    input: processed_data/isles.dat, processed_data/abyss.dat, processed_data/last.dat
    output: results/results.txt
    jobid: 0

Finished job 0.
4 of 4 steps (100%) done
```

#### Naming dependencies

Sometimes one needs to treat different dependencies of a rule differently. This can be done in two ways, either by 
enumeration:
```python
rule count_words:
    input: 'source/wordcount.py', 'data/isles.txt'
    output: 'processed_data/isles.dat'
    shell: 'python {input[0]} {input[1]} processed_data/isles.dat'
```
or by naming:
```python
rule count_words:
    input:
           wc = 'source/wordcount.py',
           book = 'data/isles.txt'
    output: 'processed_data/isles.dat'
    shell: 'python {input.wc} {input.book} processed_data/isles.dat'
```

**Note that here the source file `wordcount.py` is a dependency.** This is 
important since any changes of the source code should trigger a rebuild of all
targets that depend on it!

### Pattern rules

Even after introducing wildcards, our Snakefile still contains a lot 
of repetitions. Particularly, each .dat target has a separate rule:

```python
# Count words.
rule count_words:
    input:
           wc = 'source/wordcount.py',
           book = 'data/isles.txt'
    output: 'processed_data/isles.dat'
    shell: 'python {input.wc} {input.book} {output}'

rule count_words_abyss:
     input: 
           wc = 'source/wordcount.py',
           book = 'data/abyss.txt'
     output: 'processed_data/abyss.dat'
     shell:  'python {input.wc} {input.book} {output}'

rule count_words_last:
     input:  
           wc = 'source/wordcount.py',
           book = 'data/last.txt'
     output: 'processed_data/last.dat'
     shell:  'python {input.wc} {input.book} {output}'
```
 
We can replace all these rules with a single *pattern rule* which 
can be used to build any `.dat` file from a `.txt` file in `data/`:
```python
rule count_words:
    input:
           wc = 'source/wordcount.py',
           book = 'data/{file}.txt'
    output: 'processed_data/{file}.dat'
    shell: 'python {input.wc} {input.book} {output}'
```

This general rule uses the wildcard `{file}` as a placeholder for any book in the `data/` directory.

### Exercise: Introducing wildcards and pattern rules

Starting from your Snakefile at this point, introduce wildcards and 
pattern rules to remove all repetitions!


### OPTIONAL: further topics

#### Python functions

Snakefiles are more or less just Python code, and we can add Python code anywhere:
```python
# at the top of the file
import os
import glob

# add this wherever
rule print_book_names:
    run:
        print('These are all the book names:')
        for book in glob.glob('data/*.txt'):
            print(book)
```

The `snakemake.io` modules comes with a set of useful functions. To generalize our Snakefile further,
we can use the `glob_wildcards()` an `expand()` functions:
```python
DATA = glob_wildcards('data/{book}.txt').book
...
rule zipf_test:
    input:
        zipf='source/zipf_test.py',
	books=expand('processed_data/{book}.dat', book=DATA)
    output: 'results/results.txt'
    shell:  'python {input.zipf} {input.books} > {output}'
```
This is particularly useful if a rule has lots of dependencies.

#### Resources and parallelism

If multiple rules can be run independently of each other,
Snakemake can run a workflow in parallel:
```bash
$ snakemake -j 4
```
which gives the output:
```bash
Provided cores: 4
Rules claiming more threads will be scaled down.
... more output ...
```

This will allow Snakemake to execute multiple instances of rules at the same time 
and speed up the run.

Apart from `input`, `output` and `shell`, rules can have a number of other keywords.
Among other things, one can explicitly specify how many cores (or threads) a rule needs:
```python
# count words in one of our "books"
rule count_words:
    input:
        wc='source/wordcount.py',
        book='data/{file}.txt'
    output: 'processed_data/{file}.dat'
    threads: 4
    shell: 'python {input.wc} {input.book} {output}'
```
This will run each instance of the rule using 4 theads.

Non-CPU resources are handled with the `resources` keyword. Pretending that we have a plotting 
routine which can use a GPU, this can be specified in the Snakefile as:
```python
# create a plot for each book
rule make_plot:
    input:
        plotcount='source/plotcount.py',
        book='processed_data/{file}.dat'
    output: 'results/{file}.png'
    resources: gpu=1
    shell: 'python {input.plotcount} {input.book} {output}'
```

The workflow can now be executed on 4 cores and one GPU by:
```bash
$ snakemake clean
$ snakemake -j 4 --resources gpu=1
```

Note however that `gpu` does not actually represent a GPU, it is simply an arbitrary limit 
used to prevent multiple tasks that use a `gpu` from executing at the same time.

#### Running on a cluster

Moving a workflow to a cluster or between clusters can be a tedious task; batch scripts need
to be written and adapted to possibly different job schedulers, jobs that depend on each 
other need to be executed in the right order, etc. 
But Snakemake can manage this for you - it writes the batch scripts, submits and monitors jobs!

To facilitate the transfer of a workflow to a cluster, Snakemake has the `--archive` flag 
which will archive all files under version control (scripts, Snakefile, config files, 
conda environment file), and in addition all input files, to a specified tar archive file. 
On the cluster, Snakemake can then use the conda package manager to recreate the software
environment:
```bash
$ snakemake --archive myworkflow.tar.gz
$ scp myworkflow.tar.gz <some-cluster>
$ ssh <some-cluster>
$ tar zxf myworkflow.tar.gz
$ cd myworkflow
$ snakemake -n --use-conda
```

Snakemake uses a JSON configuration file to specify cluster-specific parameters. 
An example file for a SLURM system is:
```bash
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

In this case, rules will by default use 5 minute jobs requiring 1 GB, while the `count_words` rule requires
more time and memory. 

Some rules do not need to run in a separate job on the cluster (since they take only seconds to complete),
and should rather be completed locally where the `snakemake` command is run (e.g. login node).
One can add such exceptions with the `localrules` rule:
```python
localrules: all, clean, make_archive
```

The workflow can now be executed by:
```bash
snakemake -j 100 --cluster-config cluster.json --cluster "sbatch -A {cluster.account} --mem={cluster.mem} -t {cluster.time} -c {threads}"
```

Note that in this case `-j` does not correspond to the number of cores used, instead it represents the maximum 
number of jobs that Snakemake is allowed to have submitted at the same time.  
The `--cluster-config` flag specifies the config file for the particular cluster, and the `--cluster` flag specifies
the command used to submit jobs on the particular cluster.

#### Various other features

- Snakemake has an experimental GUI feature which can be invoked by:
  ```bash
  $ snakemake --gui
  ```
- Isolated software environments per rule using conda. Invoke by 
  `snakemake --use-conda`. Example:
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

- Jobs can be run in containers. Execute with `snakemake --use-singularity`.
  Example:
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

- Archive a workflow into a tarball:
```shell  
$ snakemake --archive my-workflow.tar.gz
```

#### Final version of our Snakefile {#finalversion}
```python
# a list of all the books we are analyzing
DATA = glob_wildcards('data/{book}.txt').book

# this is for running on HPC resources
localrules: all, clean, make_archive

# the default rule
rule all:
    input:
        'zipf_analysis.tar.gz'

# delete everything so we can re-run things
rule clean:
    shell:
        '''
        rm -rf source/__pycache__
        rm -f zipf_analysis.tar.gz processed_data/* results/*
        '''

# count words in one of our books
# logfiles from each run are put in .log files"
rule count_words:
    input:
        wc='source/wordcount.py',
        book='data/{file}.txt'
    output: 'processed_data/{file}.dat'
    threads: 4
    log: 'processed_data/{file}.log'
    shell:
        '''
        echo "Running {input.wc} with {threads} cores on {input.book}." &> {log} &&
            python {input.wc} {input.book} {output} >> {log} 2>&1
        '''

# create a plot for each book
# shows example usage of the resources keyword
rule make_plot:
    input:
        plotcount='source/plotcount.py',
	book='processed_data/{file}.dat'
    output: 'results/{file}.png'
    resources: gpu=1
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

<img src="/reproducible-research/img/snakemake_dag.png" style="height: 300px;"/>

#### Further documentation

Visit [snakemake.readthedocs.io](https://snakemake.readthedocs.io/en/stable/).


### Simple workflow with Make {#make}

> This exercise is based on the [same example project](https://github.com/coderefinery/word-count) as in the previous section.

The workflow for a single raw data file is composed of the following commands:

```bash
$ python source/wordcount.py data/abyss.txt  processed_data/abyss.dat
$ python source/plotcount.py processed_data/abyss.dat results/abyss.png
$ python source/zipf_test.py processed_data/abyss.dat > results/results.txt
```

#### Writing a Makefile
 
In Makefile syntax, a rule to run the first step of the workflow looks like this:

```makefile
processed_data/isles.dat: data/isles.txt
        python source/wordcount.py data/isles.txt processed_data/isles.dat
```

Mind the tab! The action to be executed needs to be indented with exactly one tab character.

Another rule can be added for a second datafile:

```makefile
processed_data/abyss.dat: data/abyss.txt
        python source/wordcount.py data/abyss.txt processed_data/abyss.dat
```

To run both of these rules, we need to define a new rule and place it at the top of the Makefile:

```makefile
all: processed_data/isles.dat processed_data/abyss.dat
```

We can also add a rule to clean the output:

```makefile
clean:
        @$(RM) processed_data/*
```   

The Makefile now looks like this:

```makefile
all: processed_data/isles.dat processed_data/abyss.dat

processed_data/isles.dat: data/isles.txt
        python source/wordcount.py data/isles.txt processed_data/isles.dat

processed_data/abyss.dat: data/abyss.txt
        python source/wordcount.py data/abyss.txt processed_data/abyss.dat

clean:
        @$(RM) processed_data/*
```   

and it can be run with:

```shell
$ make
```

and to clean the output:
```shell
$ make clean
```

### Exercise: Building a workflow with GNU Make

1. Write a new rule for `last.dat,` created from `data/last.txt`, and 
   update the `all` rule with this target. Run `make`.
2. The `touch` command updates the modification time of a file, in the 
   same way as if you modified and saved the file.
    - What steps does Make perform if you modify the processed data?
    ```bash
    $ touch processed_data/abyss.dat
    $ make 
    ```
    - What if you instead modify the raw data?
    ```bash
    $ touch data/abyss.txt
    $ make 
    ```
    - What if you modify the source code? Is this correct?
    ```bash
    $ touch source/wordcount.py
    $ make
    ```
      - Add the missing dependency to the appropriate rules!

3. Write a new rule for `results.txt,` which creates a table with results from 
   analysis of Zipf's law.
  - It needs to depend upon each of the three .dat files, and the source file.
  - It should invoke the action:
  ```python
python source/zipf_test.py processed_data/abyss.dat processed_data/isles.dat processed_data/last.dat > results/results.txt
  ```
  - Put this rule at the top of the Makefile so that it is the default target.
  - Update clean so that it removes results.txt.
  - Now run `make` (you can test it with a dry-run first using `make -n`)

4. Make can execute rules in parallel with the flag `-j N`, where `N` 
   is the number of cores used. Try timing `make` with the `time` 
   command (`time make ...`) and compare running with 1, 2 and 3 cores 
   (remember to clean the output in between).

5. (OPTIONAL) Create a new rule to plot one of the processed 
   datafiles using the command 
   ```python
   python source/plotcount.py processed_data/abyss.dat results/abyss.png
   ```
   - Make sure that when you run the workflow from scratch (after cleaning), 
     both the plot and the results.txt file get generated.

### Wildcards

Just as with Snakemake, Make supports wildcards to reduce repetition.  
For example, the following block:

```makefile
results/zipf_test: processed_data/isles.dat processed_data/abyss.dat processed_data/last.dat
	python source/zipf_test.py processed_data/isles.dat processed_data/abyss.dat processed_data/last.dat > results/results.txt
```

can be replaced by:

```makefile
SRCDIR := data
TMPDIR := processed_data
RESDIR := results

SRCS = $(wildcard $(SRCDIR)/*.txt)
DATA = $(patsubst $(SRCDIR)/%.txt,$(TMPDIR)/%.dat,$(SRCS))

$(RESDIR)/results.txt: $(DATA) source/zipf_test.py
       python source/zipf_test.py $(DATA) > $@
```

Note that we have used the functions `wildcard` and `pathsubst`, and also introduced the variables 
`SRCDIR`, `TMPDIR` and `RESDIR`.

### Pattern rules

Implicit rules can be defined by writing pattern rules. A pattern rule looks like an ordinary rule, 
except that its target contains the character `%`. 

For example, the following three rules (where we have introduced the variables `TMPDIR` 
and `SRCDIR` and used the wildcards, as described above):

```makefile
$(TMPDIR)/isles.dat: $(SRCDIR)/isles.txt source/wordcount.py
        python source/wordcount.py $<  $@

$(TMPDIR)/abyss.dat: $(SRCDIR)/abyss.txt source/wordcount.py
        python source/wordcount.py $<  $@

$(TMPDIR)/last.dat: $(SRCDIR)/last.txt source/wordcount.py
        python source/wordcount.py $<  $@
```

can be replaced by a single *pattern rule* which will build any `.dat` file from a `.txt` file:

```makefile
$(TMPDIR)/%.dat: $(SRCDIR)/%.txt source/wordcount.py
		 python source/wordcount.py $<  $@
```

### Exercise: Introducing wildcards and pattern rules in the Makefile

Starting from your Makefile at this point, introduce wildcards and pattern rules to remove all repetitions!

#### Makefile to process all data files

- A Makefile to process all the data files can be found in the file `Makefile_all` and run 
with `$ make -f Makefile_all`. 
