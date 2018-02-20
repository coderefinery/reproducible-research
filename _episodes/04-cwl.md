---
layout: episode
title: "Workflow management and tracking tools"
teaching: 5
exercises: 5
questions:
  - "What are scientific workflow management systems all about?"
  - "Can such tools be adopted to your research?"
objectives:
  - "Get familiar with the common workflow language as a common standard for workflow tools"
keypoints:
  - "CWL describes command line tools and workflows"
  - "Descriptions in CWL aid portability between environments"
   
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
- Each has its own specialities, benefits and user communities
- Some are domain-specific, others are domain-independent
- Different workflow engines are generally not interchangeable -> vendor lock-in
- A community-led effort to overcome this limitation is the common workflow language (CWL)

## [Common workflow language](http://www.commonwl.org/#Implementations)

- CWL is not a workflow tool, it's a **common standard**
- Describes analysis workflows and tools in a way that makes them portable and scalable across different software and hardware
  environments, from workstations to cloud and high-performance computing (HPC) environments
- Designed for data-intesive sciences like bioinformatics, medical imaging, astronomy, physics, chemistry...
- To experiment with CWL, we will use the reference implementation of CWL, `cwltool`
  - `cwltool` runs natively on Linux and OSX systems. On Windows all workflows and tools are run inside Docker container
- In many applications, one will not need to explicitly write CWL files, which is instead managed by a workflow tool
- [A wide range of workflow tools](http://www.commonwl.org/#Implementations) support CWL


### CWL vs. Makefiles

- Components can be run in Docker containers without the details of getting data into/out of the container
- Workflows can be pushed out to run on a cluster
- Workflows can run unmodified on multiple cluster platforms
- But CWL is more complex

### Type-along exercise: Hello World

   > This material has been adapted from [an online tutorial](http://www.commonwl.org/user_guide/)

- CWL documents are written in [JSON](http://json.org/) or [YAML](http://yaml.org/)

Save the following CWL *tool wrapper* in a file `1st-tool.clw`:

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

The *input object* which describes the input of a run goes into a separate YAML file:

```shell
message: Hello world!
```

- What's going on?
  - `cwlVersion` indicates the version of the CWL spec used by the document
  - `class` field indicates this document describes a command line tool
  - `baseCommand` provides the name of program that will actually run (echo)
  - `inputs` section describes the inputs of the tool, i.e. a list of input parameters. Each parameter includes
    -  an identifier 
    - a data type, 
    -  (optionally) an inputBinding which describes how this input parameter should appear on the command line
  - `outputs` describes outputs of the tool (here there is no output, so the list is empty)


### Running workflows inside Docker container

- As we saw in the previous episode, 
  Docker containers simplify software installations by providing complete runtime environment for software and dependencies
- Since containers are isolated from host system, extra work is needed to make input files available inside container, and output files 
  recoverable from container
- A CWL runner can perform this work automatically

### Type-along exercise: Docker

   > This material has been adapted from [an online tutorial](http://www.commonwl.org/user_guide/)

This example runs a simple Node.js script inside a Docker container. The tool wrapper looks like this (save it to `docker.cwl`):

```shell
#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: node
hints:
  DockerRequirement:
    dockerPull: node:slim
inputs:
  src:
    type: File
    inputBinding:
      position: 1
outputs:
  output:
    type: stdout
stdout: output.txt
```

and the *input object* looks like this (save it to `docker-job.yml`):

```shell
src:
  class: File
  path: hello.js
```

- What's going on?
  - the base command is `node`
  - the Docker specs are in the `hints` section 
    - `hints` is used for soft requirements, `requirements` for hard requirements
  - the input section specifies one input source file
  - the output is stdout, which is redirected to a file

We then provide a `hello.js` file:
```shell
$ echo "console.log(\"Hello World\");" > hello.js
```

and run it with:
```shell
$ cwltool docker.cwl docker-job.yml
```

- The CWL runner constructed a Docker command line to run the script!

### Take-home exercise

- implement the character-count example project in CWL!

