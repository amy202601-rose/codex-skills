$ErrorActionPreference = "Stop"

$Python = "C:\Users\admin\Documents\Skills\VoxCPM\.venv\Scripts\python.exe"
& $Python -c "import voxcpm, torch; print('voxcpm ok'); print(torch.__version__, torch.cuda.is_available(), torch.version.cuda)"
