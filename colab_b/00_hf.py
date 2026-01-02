import os
from huggingface_hub import hf_hub_download
import shutil


def download_data(repo_id: str, filename: str, out_dir: str):
  local_path = os.path.join(out_dir, filename)
  os.makedirs(out_dir, exist_ok=True)

  if os.path.exists(local_path):
    print(f"{filename} already exists, skipping download.")
    return

  hf_path = hf_hub_download(
    repo_id=repo_id,
    filename=filename,
    repo_type="dataset"
  )
  shutil.copy(hf_path, local_path)
  print(f"Downloaded {filename}")
