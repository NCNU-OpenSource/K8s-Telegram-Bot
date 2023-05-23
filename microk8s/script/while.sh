#!/bin/bash
x=1
while [ $x -le 1000000 ]
  do
    while [ $x -le 10 ]
      do
        x=$(( $x + 1 ))
      done
  done
