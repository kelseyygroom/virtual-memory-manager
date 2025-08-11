# Virtual Memory Manager

## Overview
This is a virtual memory manager simulator that models the translation of virtual addresses to physical addresses using segment tables, page tables, and demand paging.

It supports initialization from input files, on-demand loading of page tables and pages from disk, and simulates a physical memory (PM) array alongside a disk (D) array.

## Features

* Physical Memory Simulation
  * Simulates PM (physical memory) with configurable frame size and number of frames
* Demand Paging
  * Handles page faults by loading missing page tables or pages from a simulated disk
* Free Frame Management
  * Tracks and allocates free frames dynamically using a linked list
* Virtual to Physical Address Translation
  * Implements address translation using (s, p, w) decomposition of the virtual address:
    * s: Segment number
    * p: Page number within segment
    * w: Word offset within page
* Error Handling
  * Returns -1 for invalid addresses outside segment bounds.

## How To Run

Download the code and sample input and init files. In the terminal, navigate to the directory where these files are stored and type:
```shell
python virtualMemoryManager.py init.txt input.txt
```
Output is written to output-dp.txt or output-no-dp.txt.
