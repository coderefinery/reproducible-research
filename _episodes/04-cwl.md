---
layout: episode
title: "Workflow management and tracking tools"
teaching: 10
exercises: 10
questions:
  - "What tools are out there for managing projects based on numerical simulations or analysis?"
  - "Can such workflow tools be adopted to your research?"
objectives:
  - "Get familiar with the common workflow language as a common standard for workflow tools"
   
---

## Scientific workflows

- Home-made workflows: scripts that call in data, programs and other inputs and produce outputs.
- Many specialized frameworks exist for managing scientific workflows
  - provide user-friendly environment to create workflows
  - provide interactive tools to execute workflows and view results in real-time
  - simplify sharing and reusing workflows between researchers
  - enable researchers to track the provenance of workflow execution results and the workflow creation steps

## Provenance of data

- Provides a historical record of data, its origins and causal relationships.
- Can use it to ensure quality of data based on ancestral data, or find sources of errors.
- Allows automated recreation of data.
- Directed acyclic graphs (DAGs)
  - Useful representation of data and their provenance
  - Nodes can represent data, calculations, etc. - links represent their connections
  - Used in many workflow management systems  

![]({{ site.baseurl }}/img/wordcount_workflow.png)

## What tools are out there?

- [Hundreds of workflow tools have been 
  developed](https://github.com/common-workflow-language/common-workflow-language/wiki/Existing-Workflow-systems)
- Each has its own specialities, benefits and user communities
- Some are domain-specific, others are domain-independent
- Different workflow engines are generally not interchangeable -> vendor lock-in
- A community-led effort to overcome this limitation is the [common workflow language (CWL)](http://www.commonwl.org/)

## Common workflow language

- CWL is not a workflow tool, it's a **standard** (specification)
- Describes analysis workflows and tools in a way that makes them portable and scalable across different software and hardware
  environments, from workstations to cloud and high-performance computing (HPC) environments
- Designed for data-intesive sciences like bioinformatics, medical imaging, astronomy, physics, chemistry...
- To experiment with CWL, we will use the reference implementation of CWL, `cwltool`
  - `cwltool` runs natively on Linux and OSX systems. On Windows all workflows and tools are run inside Docker container
- In many applications, one will not need to explicitly write CWL files, which is instead managed by a workflow tool
- A wide range of tools now support CWL: Arvados, Toil, Rabix Bunny, Galaxy, Cromwell, Xenon, Consonance, Apache Taverna,
  yacle, REANA


## Type-along exercise: Hello World

   > This material has been adapted from [an online tutorial](http://www.commonwl.org/user_guide/)

- CWL documents are written in [JSON](http://json.org/) or [YAML](http://yaml.org/)
- Save the following CWL document in a file `1st-tool.clw`:

```shell
cwlVersion: v1.0
class: CommandLineTool
baseCommand: echo
inputs:
  message:
    type: string
    inputBinding:
      position: 1
outputs: []
```

- Use a YAML object in a separate file to describe the input of a run:

```shell
message: Hello world!
```

- What's going on?
  - `cwlVersion` indicates the version of the CWL spec used by the document
  - `class` field indicates this document describes a command line tool
  - `baseCommand` provides the name of program that will actually run (echo)
  - `inputs` section describes the inputs of the tool, i.e. a list of input parameters and each parameter includes an identifier, a data type, 
  and (optionally) an inputBinding which describes how this input parameter should appear on the command line
  - `outputs` describes outputs of the tool (here there is no output, so the list is empty)


## Running tools inside Docker container

- Docker containers simplify software installations by providing complete runtime environment for software and dependencies
- Since containers are isolated from host system, extra work is needed to make input files available inside container, and output files 
  recoverable from container
- A CWL runner can perform this work automatically
- TODO: insert example here



