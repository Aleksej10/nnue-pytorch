%cd nnue-pytorch
!mv ../dataset data
!chmod +x compile_data_loader.bat
!./setup_script.sh
!pip install --no-cache-dir -r requirements.txt
!ROCM_HOME=/opt/rocm CUPY_INSTALL_USE_HIP=1 pip install --no-cache-dir cupy
