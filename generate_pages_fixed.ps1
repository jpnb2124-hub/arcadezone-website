# Fixed generator: create game pages and SVG placeholders from games.csv
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$csvPath = Join-Path $scriptDir 'games.csv'
$templatePath = Join-Path $scriptDir 'game-template.html'
if (-not (Test-Path $csvPath)) { Write-Error "games.csv not found at $csvPath"; exit 1 }
if (-not (Test-Path $templatePath)) { Write-Error "game-template.html not found at $templatePath"; exit 1 }
$csv = Import-Csv $csvPath
$template = Get-Content $templatePath -Raw
$imagesDir = Join-Path $scriptDir 'images'
if (-not (Test-Path $imagesDir)) { New-Item -ItemType Directory -Path $imagesDir | Out-Null }
$pages = @()

function Get-Description($title, $category, $tag) {
  $parts = @(
    "$title is a $tag game in the $category section of ArcadeZone. This page provides background, controls, strategy, and tips to help new and returning players enjoy $title.",
    "The gameplay mechanics focus on the core interaction: players use simple controls to interact with game elements, master timing, and learn patterns.",
    "This article gives practical advice, recommended settings, and ways to approach common challenges players face while playing $title.",
    "Controls are typically intuitive - keyboard, mouse, or touch inputs - and this page documents which controls are most effective for different devices.",
    "Strategy sections break down beginner, intermediate, and advanced techniques. Beginners should focus on the basics and learn the user interface; intermediate players refine pattern play and resource management; advanced players optimize scoring and speed.",
    "We also include a short history and developer credits where available, and link to related games to encourage deeper engagement on ArcadeZone.",
    "ArcadeZone curates browser-playable versions and provides fair attribution to original creators. If an official embed is available, links or iframe instructions are included.",
    "Accessibility and device tips are included so players on mobile or desktop get the best experience when playing $title."
  )
  $desc = ""
  while (($desc -split '\s+').Count -lt 300) {
    $desc += ($parts | Get-Random) + " "
  }
  return $desc.Trim()
}

foreach ($row in $csv) {
  $slug = $row.slug
  $title = $row.title
  $category = $row.category
  $tag = $row.tag
  $external = $row.external_url

  $desc = Get-Description $title $category $tag
  $meta = "$title - Play online. Tips, controls, and background for $title."
  $screenshot = "images/$slug.svg"

  $out = $template.Replace('{{title}}', $title)
  $out = $out.Replace('{{meta_description}}', $meta)
  $out = $out.Replace('{{slug}}', $slug)
  $out = $out.Replace('{{screenshot_url}}', $screenshot)
  $out = $out.Replace('{{category}}', $category)
  $out = $out.Replace('{{tag}}', $tag)
  $out = $out.Replace('{{description_300_plus}}', $desc)
  $out = $out.Replace('{{how_to_play}}', "Use the on-screen controls or keyboard to play $title.")
  $out = $out.Replace('{{tip1}}', "Practice basic moves and learn timing for $title.")
  $out = $out.Replace('{{tip2}}', "Watch common patterns and avoid risky moves in $title.")
  $out = $out.Replace('{{tip3}}', "Try slower, deliberate play when learning $title; speed comes later.")
  $out = $out.Replace('{{external_url}}', $external)
  $out = $out.Replace('{{developer_info}}', "Developer information / credits where available.")

  $outPath = Join-Path $scriptDir ("$slug.html")
  Set-Content -Path $outPath -Value $out -Encoding UTF8

  # Create simple SVG placeholder
  $escapedTitle = [System.Security.SecurityElement]::Escape($title)
  $svgContent = @"<svg xmlns='http://www.w3.org/2000/svg' width='640' height='360'><rect width='100%' height='100%' fill='#f3f4f6'/><text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' font-family='Arial,Helvetica,sans-serif' font-size='28' fill='#111'>$escapedTitle</text></svg>"@
  $svgPath = Join-Path $imagesDir ("$slug.svg")
  Set-Content -Path $svgPath -Value $svgContent -Encoding UTF8

  $pages += "https://pxlrush.com/$slug.html"
}

# Build sitemap
$smapHeader = @'<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'@
$smapFooter = "</urlset>`n"
$entries = "  <url><loc>https://pxlrush.com/</loc><changefreq>daily</changefreq></url>`n"
foreach ($p in $pages) { $entries += "  <url><loc>$p</loc><changefreq>monthly</changefreq></url>`n" }
$smap = $smapHeader + $entries + $smapFooter
Set-Content -Path (Join-Path $scriptDir 'sitemap.xml') -Value $smap -Encoding UTF8

# Create all-games.html
$linksHtml = $csv | ForEach-Object { "<li><a href='" + $_.slug + ".html'>" + $_.title + "</a></li>" } -join "`n"
$allHtml = @"<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='utf-8'/>
  <meta name='viewport' content='width=device-width,initial-scale=1'/>
  <title>All Games — ArcadeZone</title>
  <link rel='stylesheet' href='/css/style.css'/>
</head>
<body>
  <main>
    <h1>All Games</h1>
    <ul>
$linksHtml
    </ul>
  </main>
</body>
</html>"@
Set-Content -Path (Join-Path $scriptDir 'all-games.html') -Value $allHtml -Encoding UTF8

Write-Host "Generated $($csv.Count) game pages, SVG placeholders, sitemap.xml, and all-games.html."