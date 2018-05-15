---
layout: default
permalink: /guide/
---

# Instructor guide

### How to start




### How to wrap up



### Questions to involve participants

- q1
- q2


### Timing



### Core aspects

- a1


### Sessions which can be skipped if time is tight



### Typical pitfalls

#### Confusion during `git bisect` exercise

Learners may get stuck in the `git bisect` exercise if they incorrectly assign a commit
as *bad* or *good*. 
To leave the bisect mode and return to the commit before `git bisect start` was issued,
one can do
```shell
$ git bisect reset
```
and start over if needed.