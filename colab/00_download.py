import os
from huggingface_hub import hf_hub_download
import shutil

REPO_ID = "linrock/test80-2024"
filename = "test80-2024-01-jan-2tb7p.min-v2.v6.binpack.zst"

def download_data(filename: str):
  local_path = os.path.join("dataset/", filename)
  os.makedirs("dataset/", exist_ok=True)

  if os.path.exists(local_path):
    print(f"{filename} already exists, skipping download.")
    return

  hf_path = hf_hub_download(
    repo_id=REPO_ID,
    filename=filename,
    repo_type="dataset"
  )
  shutil.copy(hf_path, local_path)
  print(f"Downloaded {filename}")

download_data(filename)
