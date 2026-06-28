param(
  [Parameter(Mandatory=$true)][string]$PhotoPath,
  [Parameter(Mandatory=$true)][string]$OutPath,
  [string]$Eyebrow = "认知复盘",
  [Parameter(Mandatory=$true)][string]$TitleLine1,
  [string]$TitleLine2 = "",
  [string]$TitleLine3 = "",
  [string]$SubtitleLine1 = "",
  [string]$SubtitleLine2 = "",
  [string]$NoteLine1 = "",
  [string]$NoteLine2 = "",
  [string]$Footer = "Wallace · 一个创业者的真心话"
)

Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms

function New-RoundRectPath([float]$x, [float]$y, [float]$w, [float]$h, [float]$r) {
  $p = New-Object System.Drawing.Drawing2D.GraphicsPath
  $d = $r * 2
  $p.AddArc($x, $y, $d, $d, 180, 90)
  $p.AddArc($x + $w - $d, $y, $d, $d, 270, 90)
  $p.AddArc($x + $w - $d, $y + $h - $d, $d, $d, 0, 90)
  $p.AddArc($x, $y + $h - $d, $d, $d, 90, 90)
  $p.CloseFigure()
  return $p
}

function New-Font([System.Drawing.FontFamily]$family, [float]$size, [System.Drawing.FontStyle]$style = [System.Drawing.FontStyle]::Regular) {
  return New-Object System.Drawing.Font($family, $size, $style, [System.Drawing.GraphicsUnit]::Pixel)
}

function Draw-CenteredText($g, [string]$text, $font, $brush, [float]$x, [float]$y, [float]$w, [float]$h) {
  if ([string]::IsNullOrWhiteSpace($text)) { return }
  $fmt = New-Object System.Drawing.StringFormat
  $fmt.Alignment = [System.Drawing.StringAlignment]::Center
  $fmt.LineAlignment = [System.Drawing.StringAlignment]::Center
  $g.DrawString($text, $font, $brush, (New-Object System.Drawing.RectangleF($x,$y,$w,$h)), $fmt)
}

function Draw-LeftText($g, [string]$text, $font, $brush, [float]$x, [float]$y, [float]$w, [float]$h) {
  if ([string]::IsNullOrWhiteSpace($text)) { return }
  $fmt = New-Object System.Drawing.StringFormat
  $fmt.Alignment = [System.Drawing.StringAlignment]::Near
  $fmt.LineAlignment = [System.Drawing.StringAlignment]::Center
  $fmt.Trimming = [System.Drawing.StringTrimming]::EllipsisCharacter
  $g.DrawString($text, $font, $brush, (New-Object System.Drawing.RectangleF($x,$y,$w,$h)), $fmt)
}

if (!(Test-Path -LiteralPath $PhotoPath)) { throw "PhotoPath not found: $PhotoPath" }
$outDir = Split-Path -Parent $OutPath
if ($outDir -and !(Test-Path -LiteralPath $outDir)) { New-Item -ItemType Directory -Force -Path $outDir | Out-Null }

$W = 1080; $H = 1920
$bmp = New-Object System.Drawing.Bitmap($W, $H, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

$paper = [System.Drawing.ColorTranslator]::FromHtml('#f5f0e8')
$grid = [System.Drawing.Color]::FromArgb(90, [System.Drawing.ColorTranslator]::FromHtml('#c8bfa0'))
$brown = [System.Drawing.ColorTranslator]::FromHtml('#3a2e1e')
$softBrown = [System.Drawing.ColorTranslator]::FromHtml('#7a6a50')
$red = [System.Drawing.ColorTranslator]::FromHtml('#c0392b')
$yellow = [System.Drawing.Color]::FromArgb(170, 255, 223, 83)
$white = [System.Drawing.Color]::FromArgb(245, 255, 252, 240)

$g.Clear($paper)
$gridPen = New-Object System.Drawing.Pen($grid, 1)
for ($x = 0; $x -le $W; $x += 40) { $g.DrawLine($gridPen, $x, 0, $x, $H) }
for ($y = 0; $y -le $H; $y += 40) { $g.DrawLine($gridPen, 0, $y, $W, $y) }
$linePen = New-Object System.Drawing.Pen(([System.Drawing.Color]::FromArgb(32, 122, 106, 80)), 1)
for ($y = 22; $y -le $H; $y += 76) { $g.DrawLine($linePen, 0, $y, $W, $y) }

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$fontPath = Join-Path $scriptDir '..\..\wwfs-covergen-lifestyle\fonts\ZCOOLKuaiLe.ttf'
$pfc = New-Object System.Drawing.Text.PrivateFontCollection
$handFamily = $null
if (Test-Path -LiteralPath $fontPath) {
  $pfc.AddFontFile((Resolve-Path -LiteralPath $fontPath).Path)
  $handFamily = $pfc.Families[0]
} else {
  $handFamily = New-Object System.Drawing.FontFamily('Microsoft YaHei UI')
}
$uiFamily = New-Object System.Drawing.FontFamily('Microsoft YaHei UI')

$fontEyebrow = New-Font $uiFamily 38 ([System.Drawing.FontStyle]::Bold)
$fontTitle = New-Font $handFamily 132 ([System.Drawing.FontStyle]::Regular)
$fontTitleSmall = New-Font $handFamily 116 ([System.Drawing.FontStyle]::Regular)
$fontSub = New-Font $uiFamily 48 ([System.Drawing.FontStyle]::Bold)
$fontNote = New-Font $uiFamily 38 ([System.Drawing.FontStyle]::Bold)
$fontFooter = New-Font $uiFamily 28 ([System.Drawing.FontStyle]::Regular)

$brushBrown = New-Object System.Drawing.SolidBrush($brown)
$brushSoft = New-Object System.Drawing.SolidBrush($softBrown)
$brushRed = New-Object System.Drawing.SolidBrush($red)
$brushYellow = New-Object System.Drawing.SolidBrush($yellow)
$brushWhite = New-Object System.Drawing.SolidBrush($white)

# Right-side rounded photo sticker.
$photo = [System.Drawing.Image]::FromFile($PhotoPath)
$dest = New-Object System.Drawing.RectangleF(430, 170, 600, 1450)
$shadowPath = New-RoundRectPath ($dest.X + 14) ($dest.Y + 18) $dest.Width $dest.Height 48
$g.FillPath((New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(55, 58, 46, 30))), $shadowPath)
$clipPath = New-RoundRectPath $dest.X $dest.Y $dest.Width $dest.Height 48
$oldClip = $g.Clip
$g.SetClip($clipPath)
$srcRatio = $photo.Width / $photo.Height
$dstRatio = $dest.Width / $dest.Height
if ($srcRatio -gt $dstRatio) {
  $cropW = [int]($photo.Height * $dstRatio)
  $cropH = $photo.Height
  $cropX = [int](($photo.Width - $cropW) * 0.54)
  $cropY = 0
} else {
  $cropW = $photo.Width
  $cropH = [int]($photo.Width / $dstRatio)
  $cropX = 0
  $cropY = [int](($photo.Height - $cropH) * 0.08)
}
if ($cropX -lt 0) { $cropX = 0 }
if ($cropY -lt 0) { $cropY = 0 }
if ($cropX + $cropW -gt $photo.Width) { $cropX = $photo.Width - $cropW }
if ($cropY + $cropH -gt $photo.Height) { $cropY = $photo.Height - $cropH }
$src = New-Object System.Drawing.Rectangle($cropX, $cropY, $cropW, $cropH)
$g.DrawImage($photo, $dest, $src, [System.Drawing.GraphicsUnit]::Pixel)
$g.Clip = $oldClip
$borderPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(245,255,255,248), 18)
$g.DrawPath($borderPen, $clipPath)

# Left translucent note panel.
$card = New-RoundRectPath 45 300 520 1120 38
$g.FillPath($brushWhite, $card)
$g.DrawPath((New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(115, 122, 106, 80), 3)), $card)

# Eyebrow marker.
$eyebrowPath = New-RoundRectPath 86 340 355 72 22
$g.FillPath($brushYellow, $eyebrowPath)
Draw-CenteredText $g $Eyebrow $fontEyebrow $brushBrown 96 342 335 68

# Main title with marker strokes.
$g.FillRectangle($brushYellow, 96, 540, 330, 50)
Draw-LeftText $g $TitleLine1 $fontTitle $brushBrown 86 470 455 180
if (![string]::IsNullOrWhiteSpace($TitleLine2)) {
  $g.FillRectangle($brushYellow, 110, 735, 310, 50)
  Draw-LeftText $g $TitleLine2 $fontTitle $brushBrown 86 660 455 180
}
if (![string]::IsNullOrWhiteSpace($TitleLine3)) {
  Draw-LeftText $g $TitleLine3 $fontTitleSmall $brushBrown 86 835 455 160
}

# Subtitle block.
$subY = if ([string]::IsNullOrWhiteSpace($TitleLine2)) { 720 } else { 900 }
if (![string]::IsNullOrWhiteSpace($SubtitleLine1)) { Draw-LeftText $g $SubtitleLine1 $fontSub $brushRed 96 $subY 420 64 }
if (![string]::IsNullOrWhiteSpace($SubtitleLine2)) { Draw-LeftText $g $SubtitleLine2 $fontSub $brushBrown 96 ($subY + 72) 430 64 }

# Small note.
if (![string]::IsNullOrWhiteSpace($NoteLine1) -or ![string]::IsNullOrWhiteSpace($NoteLine2)) {
  $note = New-RoundRectPath 100 1130 380 150 28
  $g.FillPath((New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(232,255,251,218))), $note)
  $g.DrawPath((New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(160,240,192,64), 3)), $note)
  Draw-LeftText $g $NoteLine1 $fontNote $brushBrown 126 1150 325 54
  Draw-LeftText $g $NoteLine2 $fontNote $brushSoft 126 1205 325 54
}

# Dashed red arrow and doodle accents.
$arrowPen = New-Object System.Drawing.Pen($red, 5)
$arrowPen.DashPattern = @(10, 7)
$g.DrawBezier($arrowPen, 400, 1295, 525, 1260, 620, 1190, 695, 1080)
$g.FillPolygon((New-Object System.Drawing.SolidBrush($red)), @(
  (New-Object System.Drawing.PointF(690,1084)),
  (New-Object System.Drawing.PointF(718,1050)),
  (New-Object System.Drawing.PointF(724,1098))
))
# Keep the arrow unlabelled by default to avoid covering the portrait.

# Footer strip.
$footerPath = New-RoundRectPath 74 1735 550 66 24
$g.FillPath((New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(210,255,255,248))), $footerPath)
Draw-CenteredText $g $Footer $fontFooter $brushSoft 88 1740 520 58

$bmp.Save($OutPath, [System.Drawing.Imaging.ImageFormat]::Png)

$photo.Dispose(); $bmp.Dispose(); $g.Dispose(); $pfc.Dispose()
Write-Output $OutPath

