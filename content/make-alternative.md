# Solution 4: Using [GNU Make](https://www.gnu.org/software/make/)

First study the `Makefile`:

```makefile
# directory containing source data
SRCDIR := data

# directory containing intermediate data
TMPDIR := processed_data

# results directory
RESDIR := results

# all source files (book texts)
SRCS = $(wildcard $(SRCDIR)/*.txt)

# all intermediate data files
DATA = $(patsubst $(SRCDIR)/%.txt,$(TMPDIR)/%.dat,$(SRCS))

# all images
IMAGES = $(patsubst $(SRCDIR)/%.txt,$(RESDIR)/%.png,$(SRCS))

all: $(DATA) $(IMAGES) $(RESDIR)/results.txt

$(TMPDIR)/%.dat: $(SRCDIR)/%.txt source/wordcount.py
        python source/wordcount.py $< $@

$(RESDIR)/%.png: $(TMPDIR)/%.dat source/plotcount.py
        python source/plotcount.py $< $@

$(RESDIR)/results.txt: $(DATA) source/zipf_test.py
        python source/zipf_test.py $(DATA) > $@

clean:
        @$(RM) $(TMPDIR)/*
        @$(RM) $(RESDIR)/*

.PHONY: clean directories
```

- A tool from the 70s often used to build software.
- Uses specific syntax that the user writes in a Makefile.
- Makefile specifies how to build targets from their dependencies.
- Observe that we use wildcards instead of explicit book names.

It contains rules that relate targets to dependencies and commands:

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
$ make clean
$ make
```

Make uses **declarative style**: we describe dependencies but we let Make
figure out the series of steps to produce results (targets). Fun fact: Excel is also
declarative, not imperative.

Try running `make` again and discuss why it refused to rerun all steps:
```
$ make

make: Nothing to be done for 'all'.
```

Make a modification to a txt or a dat file and run `make` again and discuss
what you see. One way to modify files is to use the `touch` command which will
only update its timestamp:

```
$ touch data/sierra.txt
$ make
```

How did Make know which steps to rerun?

Finally try to run the pipeline on several cores in parallel (here we will try 4):

```shell
$ make clean
$ make -j 4
```

```{discussion}
Discuss the pros and cons of this approach. Is it reproducible? Does it scale to hundreds of books? Can it be automated?
```


