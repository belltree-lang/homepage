$path = "c:\Users\sss_1\OneDrive\ドキュメント\GitHub\homepage - コピー\terms-of-service\index.html"
try {
    $c = [IO.File]::ReadAllText($path)
    $c.Substring(0, [Math]::Min(10000, $c.Length))
} catch {
    $_.Exception.Message
}
