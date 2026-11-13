# Reproducible notebooks (optional)

```{objectives}
- Understand that saved notebook outputs can depend on earlier kernel state
- Put inputs before the calculations that use them
- Check a notebook by restarting its kernel and running all cells
```

```{questions}
- A notebook shows a nice result. Can the code in it actually recreate that
  result?
- What should we check before sharing a notebook?
```

```{instructor-note}
- 5-10 min exercise
```

A notebook can show a believable result even when its current code cannot
recreate it. Restarting the kernel and running all cells is a quick check
before sharing a notebook with others (or with future you).

```{admonition} New to notebooks?
- A **cell** is a block of text or code in the notebook.
- Running a code cell sends it to the **kernel**, the Python process that
  calculates results and remembers values. Select a code cell and press
  **Shift+Enter** to run it.
- The notebook file saves results from earlier runs. Editing or moving a cell
  does not clear the kernel's memory or update those saved results.
- Restarting the kernel clears that memory. Running all cells afterwards tests
  the current code from top to bottom.

More in the [Jupyter kernel documentation](https://docs.jupyter.org/en/latest/projects/kernels.html).
```

## Example: regional unemployment indicators

Imagine we are preparing a policy briefing with these **fictional** rates:

| Fictional region | Unemployment rate |
| --- | --- |
| River | 20% |
| Hill | 22% |
| Coast | 24% |

We compare each rate with an illustrative target of **10%** and calculate the
average gap across the three regions:

- Subtracting one percentage rate from another gives a gap in **percentage
  points**, not a relative percentage change. For example, River is 10
  percentage points above the target.
- Each region gets equal weight, so this average is not a national unemployment
  rate.
- The data and target are invented for teaching. They are not real statistics or
  an official policy target.

## Try it out

Download {download}`the out-of-order notebook <examples/notebooks/out-of-order.ipynb>`
and {download}`the corrected notebook <examples/notebooks/reproducible.ipynb>`.
Both only use Python's standard library and contain all their inputs, so no
data download is needed. Open the out-of-order notebook in Jupyter.

```{admonition} Hint
The calculation needs both the regional rates and the target. Check where each
of them is defined compared to the cell that uses it: Python needs a value in
memory before it can calculate with it.
```

````{exercise} Notebooks-1: Can you reproduce the saved result?
The saved result is a mean gap of `12.0 percentage points` above the target.

1. Look at code cells A, B and C without running them. Do you think a fresh
   top-to-bottom run will produce the saved result?
2. Use the **Kernel** menu to restart the kernel. Then run code cell A, then C,
   then B. Note the result and the run counters next to the cells.
3. Use the Kernel menu to restart and run all cells from top to bottom. What
   happens, and which input is missing when the calculation runs?
4. Move code cell C above code cell B (drag it by the area to the left of the
   cell). Running the cells in a different order is not enough: the saved
   notebook must work from top to bottom. Restart and run all cells to test
   your change, then compare with the corrected notebook.

```{solution}
- Cell B uses `target_rate`, but cell C defines it below the calculation.
- Running A, C, B puts the target in memory before B runs and gives a mean gap
  of `12.0 percentage points`. A fresh top-to-bottom run reaches B before C and
  raises a `NameError`.
- The fix is to define the target before the calculation. The corrected
  notebook defines both inputs first, calculates the gaps `[10, 12, 14]` and
  checks that their mean is `12.0` percentage points.
- The saved output alone cannot tell us whether the cells are in the right
  order. Run counters are a useful clue, but only restarting and running all
  cells tests the current notebook.
```
````

```{discussion} Before you share
What would a colleague learn from the saved output alone? What does the clean
run add?
```

## Check clean execution automatically

From the repository root, with Python and a Python Jupyter kernel available:

```console
$ python -m pip install nbformat nbclient ipykernel
$ python content/examples/notebooks/check.py
```

The check uses fresh kernels and does not overwrite the notebooks:

- It recreates the saved result by running A, C, B.
- It confirms that a top-to-bottom run of the out-of-order notebook fails with
  the expected `NameError`.
- It checks the output of the corrected notebook.

Any unexpected error or result makes the command fail. Look for the three
`PASS` lines. Recent versions of `ipykernel` may also print a warning that the
kernel is "running over TCP without encryption"; this is expected for a local
check and does not affect the result. More in
[NBClient's execution documentation](https://nbclient.readthedocs.io/en/latest/client.html).

Restarting a kernel clears its memory. It does not reset installed packages,
files or external services. For a real analysis, also record the environment,
input data and random seeds where needed. A successful run shows that the steps
run in that environment, not that the analysis is scientifically valid.

For setup instructions and more notebook practice, see the
[CodeRefinery Jupyter lesson](https://coderefinery.github.io/jupyter/).

```{keypoints}
- Saved outputs show what happened in an earlier session, not what the
  current notebook will produce.
- Define inputs before the cells that use them.
- Restart the kernel and run all cells before sharing a notebook.
```
