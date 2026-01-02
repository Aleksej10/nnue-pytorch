!python3 train.py \
  ./data/test80-2024-01-jan-2tb7p.min-v2.v6.binpack \
  ./data/test80-2024-01-jan-2tb7p.min-v2.v6.binpack \
  --resume_from_checkpoint ./checkpoints/last.ckpt \
  --gpus "0," \
  --threads 4 \
  --num-workers 4 \
  --batch-size 16384 \
  --random-fen-skipping 3 \
  --features=HalfKAv2_hm_bishops \
  --lambda=1.0 \
  --network-save-period 2 \
  --max_epochs=400
