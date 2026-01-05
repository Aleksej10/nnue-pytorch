from config import ModelConfig
from features import FeatureSet

import model as M
import torch

VERSION = 0x7AF32F20

def header(model: M.NNUEModel):
  fc_hash = hash(model)

  print("fc_hash ^ model.feature_set.hash ^ (model.L1 * 2)")
  print(f"{fc_hash} ^ {model.feature_set.hash} ^ ({model.L1} * 2)")
  # 1664316490 ^ 1082167927 ^ (3072 * 2)

  hash = fc_hash ^ model.feature_set.hash ^ (model.L1 * 2)
  # 598998589

  print(f"Final hash: {hash}")


def fc_hash(model: M.NNUEModel):
  print("prev_hash = 0xEC42E90D")
  prev_hash = 0xEC42E90D

  print(f"prev_hash ^= model.L1 * 2; model.L1 = {model.L1}") # 3072
  prev_hash ^= model.L1 * 2

  print("""
  layers = [
    model.layer_stacks.l1.linear.out_features,
    model.layer_stacks.l2.linear.out_features,
    model.layer_stacks.output.linear.out_features,
  ]
        """)

  layers = [
    model.layer_stacks.l1.linear.out_features,
    model.layer_stacks.l2.linear.out_features,
    model.layer_stacks.output.linear.out_features,
  ]
  print(layers) # [128, 256, 8]

  print("""
  for layer in layers:
    layer_hash = 0xCC03DAE4
    layer_hash += layer // model.num_ls_buckets
    layer_hash ^= prev_hash >> 1
    layer_hash ^= (prev_hash << 31) & 0xFFFFFFFF
    if layer // model.num_ls_buckets != 1:
      # Clipped ReLU hash
      layer_hash = (layer_hash + 0x538D24C7) & 0xFFFFFFFF
    prev_hash = layer_hash
       """)

  print(f"model.num_ls_buckets = {model.num_ls_buckets}") # 8

  for layer in layers:
    layer_hash = 0xCC03DAE4
    layer_hash += layer // model.num_ls_buckets
    layer_hash ^= prev_hash >> 1
    layer_hash ^= (prev_hash << 31) & 0xFFFFFFFF
    if layer // model.num_ls_buckets != 1:
      # Clipped ReLU hash
      layer_hash = (layer_hash + 0x538D24C7) & 0xFFFFFFFF
    prev_hash = layer_hash

  return layer_hash # 1664316490

def load_model():
  source = "./checkpoints/last.ckpt"
  feature_set = M.get_feature_set_from_name("HalfKAv2_hm_bishops")
  l1 = M.ModelConfig().L1

  nnue = M.NNUE.load_from_checkpoint(
    source,
    feature_set=feature_set,
    config=M.ModelConfig(L1=l1),
    quantize_config=M.QuantizationConfig(),
    map_location=torch.device("cpu"),
  )
  nnue.eval()
