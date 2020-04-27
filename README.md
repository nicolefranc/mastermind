---
title: "Mastermind"
author: Nicole Yu
---

# Mastermind

A command line version of the classic puzzle game applying the concept of state machines utilising the [libdw library](https://github.com/kurniawano/libdw/blob/master/libdw/sm.py).

## Table of Contents

[TOC]

## Requirements

Run this script in your terminal or command prompt for best results.

```bash
pip install libdw
python mastermind.py
```

## How to Play

### Objective

To decode the key that the script has generated

### Game Play

1. Script generates the key. Game begins.

2. You are given a set of colors to choose from.

   ![](https://i.imgur.com/P0iuyP6.png)

3. Enter one color at a time and confirm your choice.
4. After confirming, a set of hints is provided.
   _What the hints mean?_
   > x - one of the guessed pegs is correct, and is in the right hole
   > o - one of the guessed pegs is correct, but is in the wrong hole
   > _Take note: the order of the hints does not matter_

5) Repeat this until you've successfully decoded or have run out of rows

### How to Win?

Decode the key in the shortest amount of time with the lowest possible number of turns

## Demo

![](https://i.imgur.com/M2JWLzg.gif)

> To view my demonstration video go to: [https://youtu.be/dxSaCalvObQ](https://)

## Code Breakdown

```python
'''
  This class inherits the functions from the sm library
  Attr: start_state, start_time
''''
class Mastermind(sm.SM):
  run()
    # Starts the state machine and trigger input from the user
    # Subsequently, it passes the input to the get_next_values function
    # args: -/-
    # return: -/-

  get_next_values()
    # Processes the given input and returns the next state
    #   and output based on the said input
    # args: list state, string inp
    # return: list next_state, string output

  done()
    # Checks whether the whole process is done based on the state
    # args: state
    # return: boolean

'''
  This class encapsulates the entire functionality of the board
    in the context of the physical game.
  Attr: palette, rounds, board
'''
class Board:
  generate_code()
    # Generates a random 4-color combination that represents the key
    # args: -/-
    # return: -/-

  display_board()
    # Processes the string that is to be used to display the board
    # args: tuple peg_data, tuple key_data
    # return: string display_str

  add_color()
    # changes the color of the text
    # args: string inp, string str_to_color
    # return string colored_str

  show_code()
    # accesses and reveals the code
    # args: -/-
    # return: string reveal_str

 '''
  This class inherits the methods and attributes of the class Board.
  An instance of this class represents one row in the board
  Attr: pegs, key_pegs, row_length
 '''
class RowPegs(Board):
  add_peg()
    # Adds the peg to the pegs attribute
    # args: string peg
    # return: -/-

  get_peg_length()
    # Retrieves the current number of pegs in the row
    # args: -/-
    # return: string peg_length

  undo()
    # Removes the last item (peg) in the pegs list
    # args: -/-
    # return: boolean

  validate_pegs()
    # Check whether the input combination matches that of the key,
    # Identifies the corresponding hints
    # args: -/-
    # return: boolean is_decoded

  reset()
    # Resets lists of pegs and key pegs to start another row
    # args: -/-
    # return: -/-

def convert_time()
  # converts the elapsed time into the desired format
  # args: float elapsed_time
  # return: string time

def clear_terminal()
  # checks the os the script is running in and uses the
  #   appropriate function call to clear the terminal
  # args: -/-
  # return: -/-
```

## Roadmap

- [ ] Create a Leaderboard (local and global)
- [ ] Option to choose different levels of difficulty
- [ ] Allow PvP or vs CPU
- [ ] Offer a non-colored interface for the color-deficient
- [ ] Add support to other shells that do not support ANSI sequences by utilising other libraries _i.e colorama_

###### tags: `readme` `documentation` `python` `mastermind`
