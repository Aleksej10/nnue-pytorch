#!/bin/bash

python3 train.py \
  ./data/test80-2024-01-jan-2tb7p.min-v2.v6.binpack \
  ./data/test80-2024-01-jan-2tb7p.min-v2.v6.binpack \
  --gpus "0," \
  --threads 4 \
  --num-workers 4 \
  --batch-size 16384 \
  --progress_bar_refresh_rate 20 \
  --random-fen-skipping 3 \
  --features=HalfKAv2_hm_bishops^ \
  --lambda=1.0 \
  --max_epochs=400 \
  --default_root_dir ./training/runs/run_0
