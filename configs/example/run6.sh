#!/bin/bash

# Path to your gem5 binary
GEM5_PATH=~/gem5/build/X86/gem5.opt

# The Python config script you posted
CONFIG_SCRIPT=./test5.py

# Where to put your stats files
STATS_DIR="stats_multi_workload"
mkdir -p "${STATS_DIR}"

# List all the workloads you want to simulate (absolute paths)
workloads=(
  "/home/sphoo/gem5/configs/example/add"
  "/home/sphoo/gem5/configs/example/fft"
  "/home/sphoo/gem5/configs/example/hello"
  "/home/sphoo/gem5/configs/example/ml_infer"
  "/home/sphoo/gem5/configs/example/sparse"
)

for cmdpath in "${workloads[@]}"; do
  name=$(basename "${cmdpath}")
  out="${STATS_DIR}/${name}_results6.txt"

  echo "---- Running ${name} → ${out} ----"
  "${GEM5_PATH}" "${CONFIG_SCRIPT}" \
    --cpu-type TimingSimpleCPU \
    --num-cpus 2 \
    --l1-size 32kB \
    --l2-size 512kB \
    --sys-clock 2GHz \
    --cpu-clock 1.5GHz \
    --mem-size 512MB \
    --stats-file "${out}" \
    --verbose \
    --cmd "${cmdpath}"

  echo "Completed ${name}"
  echo
done
