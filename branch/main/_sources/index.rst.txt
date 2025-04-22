.. _index:

Reproducible research - Preparing code to be usable by you and others in the future
===================================================================================

Have you ever spent days **trying to repeat the results from few weeks or months
ago**?  Or you have to do paper revisions, but you just can't get the results to
match up? It's unpleasant for both you and science.

In this lesson we will explore different methods and tools for better
reproducibility in research software and data. We will demonstrate how version
control, workflows, containers, and package managers can be used to **record
reproducible environments and computational steps** for our future selves and others.


.. admonition:: Learning outcomes

  By the end of this lesson, learners should:
    - Be able to apply well organized directory structure for their project
    - Understand that code can have dependencies, and know how to document them
    - Be able to document computational steps, and have an idea when it can be useful
    - Know about use cases for containers

.. prereq::

   You need to install
   `Git, Python, and Snakemake <https://coderefinery.github.io/installation/>`__.

   If you wish to follow in the terminal and are new to the command line, we
   recorded a `short shell crash course <https://youtu.be/xbTTDLA3txI>`__.


.. toctree::
   :maxdepth: 1
   :caption: Core episodes

   intro.md
   motivation.md
   organizing-projects.md
   workflow-management.md
   dependencies.md
   environments.md
   where-to-go.md


.. toctree::
   :maxdepth: 1
   :caption: Reference

   Shell crash course <https://youtu.be/xbTTDLA3txI>
   exercises
   guide


.. toctree::
   :maxdepth: 1
   :caption: About

   All lessons <https://coderefinery.org/lessons/core/>
   CodeRefinery <https://coderefinery.org/>
   Reusing <https://coderefinery.org/lessons/reusing/>
