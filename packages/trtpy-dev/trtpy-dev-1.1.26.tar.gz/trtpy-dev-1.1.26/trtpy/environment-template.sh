#!/bin/bash

# enable trtpy library environment
# source environment.sh
export LD_LIBRARY_PATH=${@CUDA_HOME}/lib64:${@PYTHON_LIB}:${@TRTPRO_LIB}:${@CPP_PKG}/opencv4.2/lib:${@SYS_LIB}:$LD_LIBRARY_PATH
export PATH=${@CUDA_HOME}/bin:$PATH