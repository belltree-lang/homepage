$b = 'c:\Users\sss_1\OneDrive\ドキュメント\GitHub\homepage - コピー'
$files = @(
    'index.html',
    'about\index.html',
    'contact\index.html',
    'services\index.html',
    'services\fitness\index.html',
    'services\leaf\index.html',
    'services\legal\index.html',
    'services\home-care\index.html',
    'services\acupuncture\index.html',
    'team\index.html',
    'solutions\index.html',
    'solutions\stroke\index.html',
    'solutions\frailty\index.html',
    'solutions\fall-risk\index.html',
    'solutions\parkinson\index.html',
    'solutions\home-care-start\index.html',
    'solutions\lower-back-pain\index.html',
    'solutions\knee-pain\index.html',
    'cases\index.html',
    'recruit\index.html',
    'recruit\acupuncture\index.html',
    'recruit\fitness\index.html'
)

foreach ($f in $files) {
    $src = Join-Path $b $f
    $dst = Join-Path $b ('lolipop_staging\' + $f)
    $dir = Split-Path $dst -Parent
    if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    Copy-Item $src $dst -Force
    Write-Host ('OK: ' + $f)
}
Write-Host 'Done.'
