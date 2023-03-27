# Recording computational steps

```{questions}
- You have some steps that need to be run to do your work.  How do you
  actually run them?  Does it rely on your own memory and work, or is it
  reproducible? **How do you communicate the steps** for future you and others?
- How can we create a reproducible workflow?
- When to use scientific workflow management systems.
```

```{instructor-note}
- 10 min teaching
- 20 min exercises
```


## Several steps from input data to result

*The following material is partly derived from a [HPC Carpentry lesson](https://hpc-carpentry.github.io/hpc-python/).*

In this episode, we will use an [example
project](https://github.com/coderefinery/word-count) which finds most frequent
words in books and plots the result from those statistics.  In this example we
wish to:
1. Analyze word frequencies using [statistics/count.py](https://github.com/coderefinery/word-count/blob/main/statistics/count.py)
   for 4 books
   (they are all in the [data](https://github.com/coderefinery/word-count/tree/main/data) directory).
2. Plot a histogram using [plot/plot.py](https://github.com/coderefinery/word-count/blob/main/plot/plot.py).

(here we can add an image that summarizes book -> counts -> plot)

Example (for one book only):

```console
$ python statistics/count.py data/isles.txt > statistics/isles.data
$ python plot/plot.py --data-file statistics/isles.data --plot-file plot/isles.png
```

```{discussion}
We have two steps and 4 books. But **imagine having 4 steps and processing 500 books**.
Can you relate? Are you using similar setups in your research? How do you record them?
```

---

## Exercise

````{prereq} Exercise preparation
The exercise (below) and pre-exercise discussion uses a simple
word-count repository
(<https://github.com/coderefinery/word-count>). We should clone the
repository already to prepare to work on it.

You could do the exercise either on your own computer, or the [Binder](https://mybinder.org/)
cloud service:

**On your own computer**:
- Activate the [coderefinery conda environment](https://coderefinery.github.io/installation/conda-environment/) with `conda activate coderefinery`.
- Clone the word-count repository:
  ```console
  $ git clone https://github.com/coderefinery/word-count.git
  ```

**On Binder**:
We can also use the cloud service [Binder](https://mybinder.org/) to make sure
we all have the same computing environment.  This is interesting from a
reproducible research point of view and it's explained further in the [Jupyter
lesson](https://coderefinery.github.io/jupyter/sharing/) how this is even
possible.
- Go to <https://github.com/coderefinery/word-count> and click on the "launch binder" badge in the README.
- Once it get started, you can open a new Terminal from the **new** menu (top right) and select **Terminal**.
````

````{exercise} Workflow-1: Scripted solution for processing 4 books
Somebody wrote a script (`script.sh`) to process all 4 books:

```{code-block} bash
---
emphasize-lines: 4
---

#!/usr/bin/env bash

# loop over all books
for title in abyss isles last sierra; do
    python statistics/count.py data/${title}.txt > statistics/${title}.data
    python plot/plot.py --data-file statistics/${title}.data --plot-file plot/${title}.png
done
```

We can run it with:
```console
$ bash script.sh
```

- What are the advantages of this solution compared to processing all one by one?
- Is the scripted solution reproducible?
- Imagine adding more steps to the analysis and imagine the steps being time consuming. What problems do you anticipate
  with a scripted solution?

```{solution}
Will be added ...
```
````

````{exercise} Workflow-2: Workflow solution using Snakemake

```{figure} img/snakemake.png
:alt: How Snakemake works
:width: 100%
```

Somebody wrote a [Snakemake](https://snakemake.readthedocs.io) solution
and the interesting file here is the [Snakefile](https://github.com/coderefinery/word-count/blob/main/Snakefile):
```
# a list of all the books we are analyzing
DATA = glob_wildcards('data/{book}.txt').book

rule all:
    input:
        expand('statistics/{book}.data', book=DATA),
        expand('plot/{book}.png', book=DATA)

# count words in one of our books
rule count_words:
    input:
        script='statistics/count.py',
        book='data/{file}.txt'
    output: 'statistics/{file}.data'
    conda: 'environment.yml'
    log: 'statistics/{file}.log'
    shell: 'python {input.script} {input.book} > {output}'

# create a plot for each book
rule make_plot:
    input:
        script='plot/plot.py',
        book='statistics/{file}.data'
    output: 'plot/{file}.png'
    conda: 'environment.yml'
    log: 'plot/{file}.log'
    shell: 'python {input.script} --data-file {input.book} --plot-file {output}'
```

Snakemake uses **declarative style**: we describe dependencies but we let
Snakemake figure out the series of steps to produce results (targets).
Snakefiles contain rules that relate targets (`output`) to dependencies
(`input`) and commands (`shell`).

Exercise goals:
1. Clone the example to your computer: `$ git clone https://github.com/coderefinery/word-count.git`
2. Study the Snakefile. How does it know what to do first and what to do then?
3. Try to run it. Since version 5.11 one needs to specify number of cores (or
   jobs) using `-j`, `--jobs` or `--cores`:
   ```console
   $ snakemake --delete-all-output -j 1
   $ snakemake -j 1
   ```
   The `--delete-all-output` part makes sure that we remove all generated files before we start.
4. Try running `snakemake` again and observe that and discuss why it refused to rerun all steps:
   ```console
   $ snakemake -j 1

   Building DAG of jobs...
   Nothing to be done (all requested files are present and up to date).
   ```
5. Make a tiny modification to the plot.py script and run `$ snakemake -j 1` again and observe how it will only re-run the plot steps.
6. Make a tiny modification to one of the books and run `$ snakemake -j 1` again and observe how it only regenerates files for this book.
7. Discuss possible advantages compared to a scripted solution.
8. **Question for R developers**: Imagine you want to rewrite the two Python scripts and use R instead. Which lines in
   the [Snakefile](https://github.com/coderefinery/word-count/blob/main/Snakefile) would you have to modify so that it uses your R code?
9. If you make changes to the Snakefile, validate it using `$ snakemake --lint`.

```{solution}
Will be added ...
```
````


## Why [Snakemake](https://snakemake.readthedocs.io/)?

- Gentle learning curve.
- Free, open-source, and installs easily via conda or pip.
- Cross-platform (Windows, MacOS, Linux) and compatible with all HPC schedulers:
  same workflow works without modification and scales appropriately whether on a laptop or cluster.
- [Heavily used in bioinformatics](https://twitter.com/carl_witt/status/1103951128046301185), but is completely general.
- Is is possible to define isolated software environments per rule, see [here](https://github.com/coderefinery/word-count/blob/f4ca47440751dd2c65f55fef1a8d9f181ecdd2f6/Snakefile#L15).
- Also possible to run workflows in Docker or Apptainer containers.
- Workflows can be pushed out to run on a cluster or in the cloud without modifications to scale up.
- If several workflow steps are independent of each other, and you have multiple cores available, Snakemake can run them in parallel.
- Nice functionality for archiving the workflow, see: [the official documentation](https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html#sustainable-and-reproducible-archiving)


## Similar tools

- [Make](https://www.gnu.org/software/make/)
- [Nextflow](https://www.nextflow.io/)
- [Task](https://taskfile.dev/)
- [Common Workflow Language](https://www.commonwl.org/)
- Many [specialized frameworks](https://github.com/common-workflow-language/common-workflow-language/wiki/Existing-Workflow-systems) exist.


## Visualizing the workflow

We can visualize the directed acyclic graph (DAG) of our current Snakefile
using the `--dag` option, which will output the DAG in `dot` language.

**Note**: This requires the [Graphviz software](https://www.graphviz.org/),
which can be installed by `conda install graphviz`). It's not necessary to
run this step yourself.

```console
$ snakemake -j 1 --dag | dot -Tpng > dag.png
```
Rules that have yet to be completed are indicated with solid outlines, while already completed rules are indicated with dashed outlines.

```{figure} img/snakemake_dag.png
:alt: Snakemake DAG
:width: 100%
```
