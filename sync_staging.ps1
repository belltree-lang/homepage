$base = 'c:\Users\sss_1\OneDrive\ドキュメント\GitHub\homepage - コピー'
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

$ok = 0
$skip = 0

foreach ($file in $files) {
    $src = Join-Path $base $file
    $dst = Join-Path $base ('lolipop_staging\' + $file)
    $dstDir = Split-Path $dst -Parent
    if (!(Test-Path $dstDir)) {
        New-Item -ItemType Directory -Path $dstDir -Force | Out-Null
    }
    if (Test-Path $src) {
        Copy-Item $src $dst -Force
        Write-Host ("OK  " + $file)
        $ok++
    } else {
        Write-Host ("SKIP (not found): " + $file)
        $skip++
    }
}

Write-Host ""
Write-Host ("完了: " + $ok + " ファイルコピー / " + $skip + " スキップ")
