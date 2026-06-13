param(
  [Parameter(Mandatory=$true)][string]$Video,
  [Parameter(Mandatory=$true)][string]$Srt,
  [Parameter(Mandatory=$true)][string]$Plan,
  [Parameter(Mandatory=$true)][string]$Output,
  [string]$Ffmpeg = "C:\tmp\video_deps\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe",
  [switch]$DebugFilter
)

$ErrorActionPreference = "Stop"

function Resolve-PlanPath([string]$Path, [string]$BaseDir) {
  if ([string]::IsNullOrWhiteSpace($Path)) { return $null }
  if ([System.IO.Path]::IsPathRooted($Path)) { return $Path }
  return (Join-Path $BaseDir $Path)
}

function New-TextCardPng($Path, [string[]]$Lines, [int]$GoldLine = 0) {
  Add-Type -AssemblyName System.Drawing
  $fontName = "Microsoft YaHei UI"
  $bmp = New-Object System.Drawing.Bitmap 1080,1920,([System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
  $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
  $g.Clear([System.Drawing.Color]::FromArgb(0,0,0,0))
  $shadow = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(210,0,0,0))
  $white = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255,255,255,255))
  $gold = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255,245,197,66))
  $fontBig = New-Object System.Drawing.Font($fontName,92,[System.Drawing.FontStyle]::Bold,[System.Drawing.GraphicsUnit]::Pixel)
  $fontMed = New-Object System.Drawing.Font($fontName,74,[System.Drawing.FontStyle]::Bold,[System.Drawing.GraphicsUnit]::Pixel)
  $y = 250
  for ($i = 0; $i -lt $Lines.Count; $i++) {
    $line = $Lines[$i]
    $font = if ($line.Length -gt 8) { $fontMed } else { $fontBig }
    $size = $g.MeasureString($line, $font)
    $x = [Math]::Max(40, [Math]::Round((1080 - $size.Width) / 2))
    $brush = if ($i -eq $GoldLine) { $gold } else { $white }
    $g.DrawString($line, $font, $shadow, $x + 5, $y + 7)
    $g.DrawString($line, $font, $brush, $x, $y)
    $y += [Math]::Round($size.Height + 8)
  }
  $pen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(220,245,197,66)),6
  $g.DrawLine($pen,300,$y+8,780,$y+8)
  $pen.Dispose(); $fontBig.Dispose(); $fontMed.Dispose()
  $shadow.Dispose(); $white.Dispose(); $gold.Dispose(); $g.Dispose()
  $bmp.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
  $bmp.Dispose()
}

function New-PipAssets($Dir) {
  Add-Type -AssemblyName System.Drawing
  $maskPath = Join-Path $Dir "pip_mask_340.png"
  $ringPath = Join-Path $Dir "pip_gold_ring_380.png"
  if (!(Test-Path $maskPath)) {
    $mask = New-Object System.Drawing.Bitmap 340,340,([System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $g = [System.Drawing.Graphics]::FromImage($mask)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.Clear([System.Drawing.Color]::Black)
    $brush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::White)
    $g.FillEllipse($brush,0,0,339,339)
    $brush.Dispose(); $g.Dispose(); $mask.Save($maskPath,[System.Drawing.Imaging.ImageFormat]::Png); $mask.Dispose()
  }
  if (!(Test-Path $ringPath)) {
    $ring = New-Object System.Drawing.Bitmap 380,380,([System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $g = [System.Drawing.Graphics]::FromImage($ring)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.Clear([System.Drawing.Color]::FromArgb(0,0,0,0))
    $colors = @(
      [System.Drawing.Color]::FromArgb(255,255,238,168),
      [System.Drawing.Color]::FromArgb(255,245,197,66),
      [System.Drawing.Color]::FromArgb(255,148,104,28),
      [System.Drawing.Color]::FromArgb(255,255,252,214)
    )
    $widths = @(8,10,6,3)
    $offsets = @(4,12,22,31)
    for ($i=0; $i -lt $colors.Count; $i++) {
      $pen = New-Object System.Drawing.Pen $colors[$i],$widths[$i]
      $o = $offsets[$i]
      $g.DrawEllipse($pen,$o,$o,379-2*$o,379-2*$o)
      $pen.Dispose()
    }
    $g.Dispose(); $ring.Save($ringPath,[System.Drawing.Imaging.ImageFormat]::Png); $ring.Dispose()
  }
  return @{ mask = $maskPath; ring = $ringPath }
}

function New-Sfx($Path, [string]$FfmpegPath) {
  if (Test-Path $Path) { return }
  & $FfmpegPath -y -hide_banner -loglevel error `
    -f lavfi -i "sine=frequency=880:duration=0.22:sample_rate=48000" `
    -f lavfi -i "sine=frequency=1760:duration=0.16:sample_rate=48000" `
    -f lavfi -i "anoisesrc=color=pink:duration=0.14:sample_rate=48000:amplitude=0.10" `
    -filter_complex "[0:a]afade=t=out:st=0.12:d=0.10,volume=0.55[a0];[1:a]adelay=45|45,afade=t=out:st=0.08:d=0.08,volume=0.32[a1];[2:a]highpass=f=1500,lowpass=f=6500,afade=t=out:st=0.04:d=0.10,volume=0.45[a2];[a0][a1][a2]amix=inputs=3:duration=longest:normalize=0,alimiter=limit=0.9,aformat=channel_layouts=stereo" `
    $Path
  if ($LASTEXITCODE -ne 0) { throw "Failed to create SFX" }
}

if (!(Test-Path $Ffmpeg)) { throw "ffmpeg not found: $Ffmpeg" }
if (!(Test-Path $Video)) { throw "Video not found: $Video" }
if (!(Test-Path $Srt)) { throw "SRT not found: $Srt" }
if (!(Test-Path $Plan)) { throw "Plan not found: $Plan" }

$planPath = (Resolve-Path $Plan).Path
$baseDir = Split-Path $planPath -Parent
$planObj = Get-Content -Raw -Path $planPath | ConvertFrom-Json
$workDir = Join-Path $baseDir "_render_work"
New-Item -ItemType Directory -Path $workDir -Force | Out-Null
$pipAssets = New-PipAssets $workDir
$sfxPath = Join-Path $workDir "text_pop_chime.wav"
New-Sfx $sfxPath $Ffmpeg

$textCards = @($planObj.text_cards)
$broll = @($planObj.broll)
$audio = $planObj.audio
$pip = $planObj.pip
if ($null -eq $pip) { $pip = [pscustomobject]@{ x=660; y=1440; crop="980:980:50:360"; size=340 } }

$textInputs = @()
for ($i=0; $i -lt $textCards.Count; $i++) {
  $card = $textCards[$i]
  $png = Join-Path $workDir ("text_{0:00}.png" -f $i)
  New-TextCardPng $png @($card.lines) ([int]($card.gold_line | ForEach-Object { if ($_ -eq $null) { 0 } else { $_ } }))
  $textInputs += $png
}

$argsList = @("-y","-hide_banner","-loglevel","error","-i",$Video,"-loop","1","-framerate","30","-t","9999","-i",$pipAssets.mask,"-loop","1","-framerate","30","-t","9999","-i",$pipAssets.ring)
foreach ($b in $broll) {
  $img = Resolve-PlanPath $b.image $baseDir
  if (!(Test-Path $img)) { throw "B-roll image not found: $img" }
  $argsList += @("-loop","1","-framerate","30","-t",[string]$b.duration,"-i",$img)
}
foreach ($png in $textInputs) {
  $argsList += @("-loop","1","-framerate","30","-t","8","-i",$png)
}
$bgmPath = Resolve-PlanPath $audio.bgm $baseDir
$hasBgm = $bgmPath -and (Test-Path $bgmPath)
if ($hasBgm) { $argsList += @("-stream_loop","-1","-i",$bgmPath) }
$argsList += @("-i",$sfxPath)

$filters = New-Object System.Collections.Generic.List[string]
$filters.Add("[0:v]split=2[base_src][pip_src]")
$filters.Add("[base_src]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p[base]")
$crop = if ($pip.crop) { $pip.crop } else { "980:980:50:360" }
$size = if ($pip.size) { [int]$pip.size } else { 340 }
$filters.Add("[pip_src]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,crop=$crop,scale=${size}:${size},format=rgba[pip_square]")
$filters.Add("[1:v]format=gray[mask]")
$filters.Add("[pip_square][mask]alphamerge[pip_circle]")
$filters.Add("[2:v]format=rgba[ring]")
$filters.Add("[ring][pip_circle]overlay=x=20:y=20[pipring]")

$inputIndex = 3
for ($i=0; $i -lt $broll.Count; $i++) {
  $start = [double]$broll[$i].start
  $dur = [double]$broll[$i].duration
  $fadeOut = [Math]::Max(0.1, $dur - 0.35)
  $filters.Add("[$inputIndex`:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=rgba,fade=t=in:st=0:d=0.35:alpha=1,fade=t=out:st=$fadeOut`:d=0.35:alpha=1,setpts=PTS-STARTPTS+$start/TB[b$i]")
  $inputIndex++
}

$prev = "base"
for ($i=0; $i -lt $broll.Count; $i++) {
  $start = [double]$broll[$i].start
  $end = $start + [double]$broll[$i].duration
  $next = "vb$i"
  $filters.Add("[$prev][b$i]overlay=x=0:y=0:enable=between(t\,$start\,$end)[$next]")
  $prev = $next
}

$pipEnable = ($broll | ForEach-Object { $st=[double]$_.start; $en=$st+[double]$_.duration; "between(t\,$st\,$en)" }) -join "+"
if ([string]::IsNullOrWhiteSpace($pipEnable)) { $pipEnable = "0" }
$pipX = if ($pip.x -ne $null) { [int]$pip.x } else { 660 }
$pipY = if ($pip.y -ne $null) { [int]$pip.y } else { 1440 }
$filters.Add("[$prev][pipring]overlay=x=${pipX}:y=${pipY}:enable=$pipEnable[withpip]")
$prev = "withpip"

for ($i=0; $i -lt $textCards.Count; $i++) {
  $start = [double]$textCards[$i].start
  $dur = [double]$textCards[$i].duration
  $fadeOut = [Math]::Max(0.1, $dur - 0.25)
  $filters.Add("[$inputIndex`:v]format=rgba,fade=t=in:st=0:d=0.22:alpha=1,fade=t=out:st=$fadeOut`:d=0.25:alpha=1,setpts=PTS-STARTPTS+$start/TB[t$i]")
  $next = "vt$i"
  $end = $start + $dur
  $filters.Add("[$prev][t$i]overlay=x=0:y=0:enable=between(t\,$start\,$end)[$next]")
  $prev = $next
  $inputIndex++
}
$filters.Add("[$prev]format=yuv420p[v]")

$filters.Add("[0:a]highpass=f=80,lowpass=f=12000,dynaudnorm=f=150:g=18:p=0.95:m=12,compand=attacks=0.03:decays=0.20:points=-80/-45|-45/-25|-25/-10|-10/-4|0/-1,volume=2.2,alimiter=limit=0.93[voice]")
$audioInputs = "[voice]"
$mixCount = 1
if ($hasBgm) {
  $bgmIndex = $inputIndex
  $bgmVol = if ($audio.bgm_volume -ne $null) { [double]$audio.bgm_volume } else { 0.24 }
  $filters.Add("[$bgmIndex`:a]atrim=0:9999,asetpts=PTS-STARTPTS,volume=$bgmVol[bgm]")
  $audioInputs += "[bgm]"
  $mixCount++
  $inputIndex++
}
$sfxIndex = $inputIndex
if ($textCards.Count -gt 0) {
  $splitLabels = ($textCards | ForEach-Object -Begin { $j=0 } -Process { "[s$j]"; $j++ }) -join ""
  $filters.Add("[$sfxIndex`:a]asplit=$($textCards.Count)$splitLabels")
  for ($i=0; $i -lt $textCards.Count; $i++) {
    $delay = [int]([Math]::Round(([double]$textCards[$i].start) * 1000))
    $sfxVol = if ($audio.sfx_volume -ne $null) { [double]$audio.sfx_volume } else { 2.4 }
    $filters.Add("[s$i]adelay=$delay|$delay,volume=$sfxVol[sfx$i]")
  }
  $sfxInputs = ($textCards | ForEach-Object -Begin { $j=0 } -Process { "[sfx$j]"; $j++ }) -join ""
  $filters.Add($sfxInputs + "amix=inputs=$($textCards.Count):duration=longest:dropout_transition=0:normalize=0[sfxmix]")
  $audioInputs += "[sfxmix]"
  $mixCount++
}
$filters.Add($audioInputs + "amix=inputs=$mixCount`:duration=first:dropout_transition=0:normalize=0,alimiter=limit=0.96[a]")

$filterComplex = $filters -join ";"
if ($DebugFilter) {
  $debugPath = Join-Path $workDir "filter_complex.txt"
  Set-Content -Path $debugPath -Value $filterComplex -Encoding UTF8
  Write-Host "Filter graph: $debugPath"
}

& $Ffmpeg @argsList -filter_complex $filterComplex -map "[v]" -map "[a]" -r 30 -c:v libx264 -preset ultrafast -crf 23 -c:a aac -b:a 192k -shortest $Output
if ($LASTEXITCODE -ne 0) { throw "ffmpeg render failed with exit code $LASTEXITCODE" }

& $Ffmpeg -hide_banner -loglevel error -i $Output -t 0.1 -f null -
if ($LASTEXITCODE -ne 0) { throw "Output decode validation failed" }

Write-Host "Rendered: $Output"
