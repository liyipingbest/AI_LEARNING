#!/bin/bash

export PKG_CONFIG_PATH=/path/to/opencv4.pc:$PKG_CONFIG_PATH

g++ -o mnist mnist.cpp `pkg-config --cflags --libs opencv4` -ltensorflow