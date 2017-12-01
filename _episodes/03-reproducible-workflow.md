---
layout: episode
title: "Creating reproducible workflow"
teaching: 10
exercises: 15
questions:  
  - "How to create a reproducible workflow?"
  - "How to repeat an experiment with different data one year later?"
objectives:
  - "Get a basic idea of different tools that can be used to create reproducible workflow"
  - "You can incorporate some of these tools in your research lifecycle"

---

## Suggestions for creating a reproducible workflow

One should always be able to figure out precisely what data and what code were used to generate the results.
 

### We start by creating a clear and useful directory structure for our project

Our project directory can be something like this:

```bash
project_name/
|-- data/                                All input data files of our project
|   |-- readme.txt                       may contain subdirectories as well
|   |-- sub-folder/
|   |-- ...
|-- manuscript                           The manuscript folder will contain the manuscript that we'll write to describe the results
|-- results/                             The results folder will contain the results of our analysis, including both tables and figures
|-- source/                              The source folder will contain all of our code
```

- Let's create an example project that will count 10 most frequent characters in a given text and plots a bar chart of the characters
- Clone this [example repository](https://github.com/bast/make-pipeline)  
- We begin by creating a directory called character_count (create it somewhere where you store all your research projects)
- Inside the project create **data, mansucript, results and source** folders

Our project directory will be like this:
```bash
character_count/
|-- data/                                
|-- manuscript                           
|-- results/                             
|-- source/                              
```

### Using version control to track our changes

- Since we want to track the software/code we have used in our project
- We will initialize a Git repository for tracking this project

As you add and modify things in the project directory, you'll want to frequently commit your changes as discussed in the [Git introduction](https://coderefinery.github.io/git-intro/).

### Add data to the project
- We often start our experiment with a particular data file, or set of data files
- In the case of character-count example, we will use the file *shakespeare.in* download earlier. It contains the text that we want to analyze. 
- Copy `shakespeare.in` file inside the data subdirectory
- Include a readme file to describe the data (which helps us later)

```bash
Data is gathered from shakespeare.in file found in repository https://github.com/bast/make-pipeline
Date: 15/12/2017
```
- Note: If we have too large files / sensitive files to track, we can untrack those files using gitignore

At this point, our project directory will be like this:
```bash
character_count/
|-- data/
|   |--readme.txt
|   |--shakespeare.in
|-- manuscript                           
|-- results/                             
|-- source/                              
```

### Write code
- Write the core "scientific code" to perform the analysis, including tests
- In the case of character-count example, we will use two scripts downloaded earlier
    - count.py counts the 10 most frequently used characters in a text 
    - plot.py will plot a bar chart of the results
- Copy these scripts inside the source subdirectory

At this point, our project directory will be like this:
```bash
character_count/
|-- data/
|   |--readme.txt
|   |--shakespeare.in
|-- manuscript                           
|-- results/                             
|-- source/
|   |--count.py
|   |--plot.py
```

#### Generate results

We can extract the 10 most frequently used characters by:

```bash
cat data/shakespeare.in | ./source/count.py > results/charscount.out
```

Generate the bar chart by:
```bash
cat results/charscount.out | ./source/plot.py > results/charsplot.out
```

Let us look at our workflow:

<img src="/reproducible-research/img/wordcount_workflow.png" style="height: 300px;"/>

- In this simple example, we can easily generate the results by running the scripts
- As projects grow, it is quite difficult to keep track of all the workflow steps and how they fit together

### Documenting the workflow
- It is difficult to track the workflow:
    -  How we have generated/created the results in the first case
    -  What steps are followed in creating the results

- Multiple tools are available for documenting the workflow
    - For example, we can use `make` to track the steps we have followed in generating the data
    - Makefile itself can act as a documentation for data generation
    - [ ] Sumatra for capturing the workflow

#### Makefile to automate workflow

- Make is a tool often at the heart of many software build systems
- Make uses a Domain Specific Language that the user writes in a Makefile
- Makefile specifies how to build the particular targets from their dependencies

The target/dependencies/command are called as rules

For example:

```makefile
# rule (mind the tab)
target : dependencies
         command(s)
```
We can think of it as follows:

```makefile
outputs : inputs
          command(s)
```

Let's re-implement the steps in running character count example using Make.
 
Step 1: extract the 10 most frequently used characters in a text

```makefile
results/charscount.out: source/count.py data/shakespeare.in
        cat data/shakespeare.in | ./source/count.py > results/charscount.out
```

_The above rule says: I know how to build results/charscount.out if I have the source/count.py script and the data/shakespeare.in file, and I do that by calling source/count.py on it and redirecting the output_


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
Create a Makefile and copy and paste the above content (mind the tabs)

At this point, our project directory will be like this:
```bash
character_count/
|-- data/
|   |--readme.txt
|   |--shakespeare.in
|-- manuscript                           
|-- results/
|   |--format-data.tmp
|   |--format-data.out
|-- source/
|   |--count.py
|   |--plot.py
|--Makefile
```
If our requirement changes and we have to read text from multiple files, we can modify the Makefile as follows:
```makefile
all: results/charscount.out results/charsplot.out

results/charscount.out: source/count.py data/*.in
        cat data/*.in | ./source/count.py > results/charscount.out

results/charsplot.out: source/plot.py results/charscount.out
        cat results/charscount.out | ./source/plot.py > results/charsplot.out

```
    
- In Makefile, we explicitly define the dependencies of different files needed for executing the workflow
- With a single command we can always generate the results
- Run make (executes the first rule by default) and see if we get the results

### See if we can reproduce the results
- Delete the content in results folder
- Run make and see if we can generate results
### Other suggestions
- Use git tags to track specific versions (version submitted to a journal, the dissertation version, the poster version, etc.)

```bash
git tag -a aalto_workshop_2017 -m "results submitted to aalto workshop 2017"
```

## How to create the environment applied for an experiment?
- Software/code we have used may depend on lots of dependencies and may be difficult to create and use
- Results should be possible to reproduce regardless of platform and with minimal effort
- Many research codes can be problematic to install and configure without experts
- Could we bundle all the necessary dependencies together, so that it is easy to run the software
- Containers can be used to create isolated environments

### References

- This material uses some suggestions from [software carpentry](http://swcarpentry.github.io/2014-03-17-ucb/lessons/jk-python/reproducible_workflow.html) and [software sustainability institute](https://www.software.ac.uk/)

