[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/rSjUbLl5)
# CMPUT 429 - Assignment 2

## Creating a Branch Predictor

Refer to the [gem5 source code](https://github.com/gem5/gem5/tree/stable/src/cpu/pred) and read through one or two examples. The short of it is there are only a few key methods to define:
1. The lookup function
2. The update function

You can apply the patch provided in the repo in order to get some template code. Make sure your gem5 is at version 24.0.0.0 or else the patch will not work.

## What does the patch do?

The patch makes a few small changes to the gem5 source code:
- Add a GShare template to the `BranchPredictor.py` file
- Add the GShare source to the SConscript build system
- Provide template code for `gshare.hh` and `gshare.cc` both in `gem5/src/cpu/pred`

Fortunately, patch files are pretty readable, so if you want any specifics just go and look in the patch file.

## What should I submit?

Submit the following:
- a new `diff.patch` file that contains your changes to the gem5 source code
- a file `answers.pdf` that contains the answers to your questions in the assignment

These files should be in the root directory of your submission.
