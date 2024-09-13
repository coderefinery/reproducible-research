# Where to go from here

```{objectives}
- Understand when tools discussed in this episode can be useful
```

```{instructor-note}
- 10 min teaching/discussion
```

This episode presents a lot of different tools and opportunities for your research software project.
However, you will not always need all of them. As with so many things, it again depends on your project.

## Workflow tools will maybe make sense in the future

- In many cases, it is probably not needed
- You will want to consider workflow tools:
  - When processing many files with many steps
  - Steps or files may change
  - Your main script, connecting your steps gets very long
  - You are still collecting your input data
  - ...

## Containers seem amazing, but do I have use for them?

- Maybe not yet, but knowing that you can ...
  - Run Linux tools on your Windows computer
  - Run different versions of same software on your computer
  - Follow the "easy installation instructions" for an operating system that is not your own
  - Get a fully configured environment instead of only installing a tool
  - Share your setup and configurations with others
    
  ... can be very beneficial :)

## Important for every project

- Clear file structure for your project
- Record your workflow and write it down in a script file.
- Create a dependency list and keep it updated, optimally in an environment file
- At least consider the possibility that someone, maybe you may want to reproduce your work
  - Can you do something (small) to make it easier?
  - If you have ideas, but no time: add an issue to your repository; maybe someone else wants to help.

```{keypoints}
- Not everything in this lesson might be useful right now, but it is good to know that these things exist if you ever get in a situation that would require such solution.
- Caring about reproducibility makes work easier for the next person working on the project - and that might be you in a few years!
```
