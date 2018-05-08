---
layout: episode
title: "Workflow management and tracking tools"
teaching: 5
exercises: 5
questions:
  - "What are scientific workflow management systems all about?"
  - "Can such tools be adopted to your research?"
objectives:
  - "Get familiar with Snakemake"
keypoints:
  - "Snakemake is a tool to create reproducible and scalable data analyses"
   
---

## Scientific workflows

- Home-made workflows: scripts that call in data, programs and other inputs and produce outputs
- Many specialized frameworks exist for managing scientific workflows
  - user-friendly environment to create workflows
  - automatic job execution
  - interactive tools to execute workflows and view results in real-time
  - simplify sharing and reusing workflows
  - enable researchers to track the provenance of workflow execution results and the workflow creation steps
  - can enable scaling across nodes, clusters, cloud

### Tools

- [Hundreds of workflow tools have been 
  developed](https://github.com/common-workflow-language/common-workflow-language/wiki/Existing-Workflow-systems)
- Each has its own specialities, benefits and user communities, some are domain-specific while others domain-independent
- Two open-source, multi-disciplinary alternatives:
  - [Taverna](https://taverna.incubator.apache.org/):
  "open source multi-platform tool for designing and executing workflows. Taverna is discipline independent and used in many domains, such as bioinformatics, cheminformatics, medicine, astronomy, social science, music, and digital preservation"
  - [Pegasus](https://pegasus.isi.edu/):
    "runs on various environments including personal computers, campus clusters, grids, and clouds. It is quite flexible, but more difficult to learn than Taverna. No graphical design tool is available."
- Different workflow engines are generally not interchangeable -> vendor lock-in
  - A community-led effort to overcome this limitation is the [common workflow language (CWL)](http://www.commonwl.org)

### [Snakemake](https://snakemake.readthedocs.io/en/stable/index.html)

- Snakemake workflows are essentially Python scripts extended by declarative code to define rules 
- Rules (following that of GNU Make) describe how to create output files from input files 
- Heavily used in bioinformatics, but is completely general



### Snakefiles vs. Makefiles

$ snakemake --use-singularity
will execute the job within a singularity container that is spawned from the given image

- Components can be run in Docker containers without the details of getting data into/out of the container
- Workflows can be pushed out to run on a cluster
- Workflows can run unmodified on multiple cluster platforms


<img src="/reproducible-research/img/snakemake.png" style="height: 200px;"/>


snakemake --dag | dot -Tpng > test.png