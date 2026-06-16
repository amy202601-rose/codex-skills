---
name: voxcpm
description: Generate speech, design voices, clone voices, or launch the VoxCPM WebUI using the local OpenBMB/VoxCPM installation. Use when the user asks to use VoxCPM, VoxCPM2, TTS, text-to-speech, voice cloning, voice design, reference-audio cloning, or a local speech-generation WebUI.
---

# VoxCPM

Use the local install at:

`C:\Users\admin\Documents\Skills\VoxCPM`

Python environment:

`C:\Users\admin\Documents\Skills\VoxCPM\.venv\Scripts\python.exe`

CLI:

`C:\Users\admin\Documents\Skills\VoxCPM\.venv\Scripts\voxcpm.exe`

## Quick Checks

Before generation, verify the install if needed:

```powershell
& "C:\Users\admin\Documents\Skills\VoxCPM\.venv\Scripts\python.exe" -c "import voxcpm, torch; print(torch.__version__, torch.cuda.is_available())"
```

The verified local install currently uses CUDA PyTorch and should see the RTX 3060.

## Generate A Voice

Use voice design for text-only synthesis:

```powershell
& "C:\Users\admin\Documents\Skills\VoxCPM\.venv\Scripts\voxcpm.exe" design `
  --text "Text to synthesize." `
  --control "natural, clear, warm Mandarin female voice" `
  --output "C:\Users\admin\Documents\Skills\VoxCPM\outputs\out.wav" `
  --device cuda `
  --no-denoiser
```

## Clone A Voice

Use clone mode when the user provides a reference audio file:

```powershell
& "C:\Users\admin\Documents\Skills\VoxCPM\.venv\Scripts\voxcpm.exe" clone `
  --text "Text to read with the reference voice." `
  --reference-audio "C:\path\to\reference.wav" `
  --output "C:\Users\admin\Documents\Skills\VoxCPM\outputs\clone.wav" `
  --device cuda `
  --no-denoiser
```

If the user provides exact prompt text for the reference audio, pass it with `--prompt-text` or `--prompt-file` when appropriate.

## Launch WebUI

Use the bundled helper:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\admin\Documents\Skills\VoxCPM\run_webui.ps1"
```

Then open `http://127.0.0.1:7860`.

## Notes

- The first real generation may download VoxCPM2 model weights from Hugging Face unless `--model-path` points to a local model.
- Prefer `--device cuda` on this machine.
- Use `--no-denoiser` unless the task specifically needs denoising; it avoids loading an extra model.
- Save generated audio under `C:\Users\admin\Documents\Skills\VoxCPM\outputs` unless the user gives another path.
