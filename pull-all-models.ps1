# Pull all models used by the Streamlit app (run once; needs Ollama running).
$ollama = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
if (-not (Test-Path $ollama)) {
    Write-Host "Install Ollama from https://ollama.com/download first."
    exit 1
}
foreach ($model in @("phi3:mini", "gemma:2b", "moondream", "tinyllama")) {
    Write-Host "Pulling $model ..."
    & $ollama pull $model
}
Write-Host "Done. Run: py -3 -m streamlit run app.py"
