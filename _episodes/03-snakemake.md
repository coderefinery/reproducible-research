---
layout: episode
title: "Workflow management tools"
teaching: 5
exercises: 5
questions:
  - "What are scientific workflow management systems?"
  - "Can such tools be adopted to your research?"
objectives:
  - "Get familiar with Snakemake"
keypoints:
  - "Snakemake is a tool to create reproducible and scalable data analyses"
   
---

## Scientific workflows

- Home-made workflows: scripts that call in data, programs and other inputs and produce outputs
- Make can be used to manage workflows, but it has limitations
- Many specialized frameworks exist for managing scientific workflows
  - user-friendly environment to create workflows
  - automatic job execution
  - interactive tools to execute workflows and view results in real-time
  - simplify sharing and reusing workflows
  - enable researchers to track the provenance of workflow execution results and the workflow creation steps
  - can enable scaling across nodes, clusters, cloud

## Tools

- [Hundreds of workflow tools have been 
  developed](https://github.com/common-workflow-language/common-workflow-language/wiki/Existing-Workflow-systems)
- Each has its own specialities, benefits and user communities, some are domain-specific while others domain-independent
- Some open-source, multi-disciplinary alternatives:
  - [Taverna](https://taverna.incubator.apache.org/):
  "open source multi-platform tool for designing and executing workflows. Taverna is discipline independent and used in many domains, such as bioinformatics, cheminformatics, medicine, astronomy, social science, music, and digital preservation"
  - [Pegasus](https://pegasus.isi.edu/):
    "runs on various environments including personal computers, campus clusters, grids, and clouds. It is quite flexible, but more difficult to learn than Taverna. No graphical design tool is available."
  - [NextFlow](https://www.nextflow.io/):
    "Nextflow enables scalable and reproducible scientific workflows using software containers. It allows the adaptation of pipelines written in the most common scripting languages."
- Different workflow engines are generally not interchangeable -> vendor lock-in
  - A community-led effort to overcome this limitation is the [common workflow language (CWL)](http://www.commonwl.org)

## Managing workflows with [Snakemake](https://snakemake.readthedocs.io/en/stable/index.html)

#### Why Snakemake?
- Gentle learning curve
- Free, open-source, and installs easily via pip
- Cross-platform (Windows, MacOS, Linux) and compatible with all HPC schedulers
  - same workflow works without modification and scales appropriately whether on a laptop or cluster 
- Heavily used in bioinformatics, but is completely general

#### Snakemake vs. make

- Workflows defined in Python scripts extended by declarative code to define rules 
  - anything that can be done in Python can be done with Snakemake
- Rules work much like in GNU Make - describe how to create output files from input files 
- Possible to define isolated software environments per rule
  - uses conda to obtain and deploy software packages in the specified versions
- Also possible to run workflows in Docker or Singularity containers
- Workflows can be pushed out to run on a cluster without modifications to scale up
- Workflows can be pushed out to run on cloud

<br>
<img src="/reproducible-research/img/snakemake.png" style="height: 250px;"/>

> The following material is based on a [HPC Carpentry lesson](https://hpc-carpentry.github.io/hpc-python/)

### Type-along exercise: Snakemake for counting words

> This exercise is based on the [same example project](https://github.com/wikfeldt/word-count) as in the previous episode

We create a file called `Snakefile` with the following contents:
```python
# Count words.
rule count_words:
    input: 'data/isles.txt'
    output: 'processed_data/isles.dat'
    shell: './source/wordcount.py data/isles.txt processed_data/isles.dat'
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
     shell:  './source/wordcount.py data/abyss.txt processed_data/abyss.dat'
```
and try running `snakemake` again. It gives

```bash
Nothing to be done.
```

This is because, just like make, snakemake only tries to build the first rule in the Snakefile. 
But we can build the new target by

```bash
$ snakemake processed_data/abyss.dat
```

It's useful to have a rule to remove all data files to be able to explicitly recreate them. 
It can be called `clean`, as this is a common name for rules that delete auto-generated files:

```python
rule clean:
    shell: 'rm -f processed_data/*.dat'
```

This rule can be run by `$ snakemake clean`.

A similar command can be added to create all the data files. 
This rule should be at the top of the Snakefile so that it is the default target, 
which is executed by default if no target is given to the snakemake command:

```python
rule alldata:
     input:
         'processed_data/isles.dat',
         'processed_data/abyss.dat'
```

- Dependencies (inputs) of this rule are targets of other rules. Snakemake will 
  check to see if the dependencies exist and, if not, will see if rules are available that will create them. 
  If such rules exist it will invoke them first, otherwise it will raise an error
- An example of a rule that has no actions - used only to trigger the build of its dependencies if needed
- Dependencies must form a directed acyclic graph (DAG). 
  A target cannot depend on a dependency which itself, or one of its dependencies, depends on that target (cyclic dependency)

We can visualize the DAG of our current Snakefile using the `--dag` option, which will output the DAG 
in `dot` language (a plain-text format for describing graphs used by [Graphviz software](https://www.graphviz.org/))

```bash
$ snakemake --dag | dot -Tpng > dag.png
```
Rules that have yet to be completed are indicated with solid outlines, while already completed rules are indicated with dashed outlines.

<img src="/reproducible-research/img/snakemake_simpledag.png" style="height: 150px;"/>

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

./source/wordcount.py data/isles.txt processed_data/isles.dat

rule count_words_abyss:
    input: data/abyss.txt
    output: processed_data/abyss.dat
    jobid: 1

./source/wordcount.py data/abyss.txt processed_data/abyss.dat

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

### Exercise


1. Write a new rule for `last.dat,` created from `data/last.txt`
2. Update the `alldata` rule with this target.
3. Write a new rule for `results.txt,` which creates a table from the Zipf analysis. The rule needs to:
  - Depend upon each of the three .dat files.
  - Invoke the action:
  ```python
./source/zipf_test.py processed_data/abyss.dat processed_data/isles.dat processed_data/last.dat > results/results.txt
  ```
4. Put this rule at the top of the Snakefile so that it is the default target.
5. Update clean so that it removes results.txt.



### Wildcards 

The Snakefile created above contains a lot of unnecessary 
repetition which requires more typing and is more error-prone.
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
         './source/zipf_test.py processed_data/isles.dat processed_data/abyss.dat processed_data/last.dat > results/results.txt'
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
         './source/zipf_test.py {input} > {output}'
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

It worked.

**Questions**
- What steps does Snakemake perform if we now do the following steps?
```bash
$ touch processed_data/*.dat
$ snakemake 
```
- What if we instead do this?
```bash
$ touch data/*.txt
$ snakemake 
```
- Are the following three commands equivalent?
```bash
$ snakemake
$ snakemake zipf_test
$ snakemake results/results.txt
```
- What happens if we do the following? 
```bash
$ touch source/wordcount.py
$ snakemake
```
  - should we do something about that?

#### Naming dependencies

Sometimes one needs to treat different dependencies of a rule differently. This can be done in two ways, either by 
enumeration:
```python
rule count_words:
    input: './source/wordcount.py', 'data/isles.txt'
    output: 'processed_data/isles.dat'
    shell: '{input[0]} {input[1]} processed_data/isles.dat'
```
or by naming:
```python
rule count_words:
    input:
           wc = './source/wordcount.py',
           book = 'data/isles.txt'
    output: 'processed_data/isles.dat'
    shell: '{input.wc} {input.book} processed_data/isles.dat'
```

### Pattern rules

The Snakefile at this point looks something like the following:

```python
rule zipf_test:
     input: 'processed_data/isles.dat', 'processed_data/abyss.dat', 'processed_data/last.dat'
     output: 'results/results.txt'
     shell: './source/zipf_test.py {input} > {output}'

rule alldata:
     input: 'processed_data/isles.dat',	'processed_data/abyss.dat', 'processed_data/last.dat'

# Count words.
rule count_words:
    input:
           wc = './source/wordcount.py',
           book = 'data/isles.txt'
    output: 'processed_data/isles.dat'
    shell: '{input.wc} {input.book} {output}'

rule count_words_abyss:
     input:  'data/abyss.txt'
     output: 'processed_data/abyss.dat'
     shell:  './source/wordcount.py data/abyss.txt processed_data/abyss.dat'

rule count_words_last:
     input:  'data/last.txt'
     output: 'processed_data/last.dat'
     shell:  './source/wordcount.py data/last.txt processed_data/last.dat'

rule clean:
    shell: 'rm -f processed_data/*.dat results/results.txt'
```
 
It still contains lots of repetition, i.e. there's a separate rule for each `.dat` target. 
We can replace all these rules with a single *pattern rule* which can be used to build 
any `.dat` file from a `.txt` file in `data/`:
```python
rule count_words:
    input:
           wc = './source/wordcount.py',
           book = 'data/{file}.txt'
    output: 'processed_data/{file}.dat'
    shell: '{input.wc} {input.book} {output}'
```

This general rule uses the wildcard `{file}` as a placeholder for any book in the `data/` directory.

