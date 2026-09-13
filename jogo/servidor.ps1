# servidor.ps1 - servidor de arquivos local para o treinamento.
# Usa apenas o que ja vem no Windows: nao precisa instalar nada.
# Chamado pelo abrir_jogo.bat quando a maquina nao tem Python.
param(
  [int]$Porta = 8765,
  [string]$Raiz = "."
)

$ErrorActionPreference = "Stop"
$Raiz = (Resolve-Path -LiteralPath $Raiz).Path
if (-not $Raiz.EndsWith("\")) { $Raiz = $Raiz + "\" }

$tipos = @{
  ".html" = "text/html; charset=utf-8"
  ".htm"  = "text/html; charset=utf-8"
  ".js"   = "application/javascript; charset=utf-8"
  ".mjs"  = "application/javascript; charset=utf-8"
  ".css"  = "text/css; charset=utf-8"
  ".json" = "application/json; charset=utf-8"
  ".glb"  = "model/gltf-binary"
  ".gltf" = "model/gltf+json"
  ".wasm" = "application/wasm"
  ".jpg"  = "image/jpeg"
  ".jpeg" = "image/jpeg"
  ".png"  = "image/png"
  ".gif"  = "image/gif"
  ".svg"  = "image/svg+xml"
  ".webp" = "image/webp"
  ".ico"  = "image/x-icon"
  ".mp4"  = "video/mp4"
  ".webm" = "video/webm"
  ".mp3"  = "audio/mpeg"
  ".ogg"  = "audio/ogg"
  ".wav"  = "audio/wav"
  ".txt"  = "text/plain; charset=utf-8"
  ".md"   = "text/markdown; charset=utf-8"
  ".woff" = "font/woff"
  ".woff2"= "font/woff2"
}

try {
  $ip = [System.Net.IPAddress]::Loopback
  $ouvinte = New-Object System.Net.Sockets.TcpListener($ip, $Porta)
  $ouvinte.Start()
} catch {
  Write-Host ""
  Write-Host "  Nao consegui abrir a porta $Porta." -ForegroundColor Red
  Write-Host "  Provavelmente outro programa ja esta usando essa porta."
  Write-Host ""
  Read-Host "  Pressione ENTER para fechar"
  exit 1
}

Write-Host ""
Write-Host "  SERVIDOR DO TREINAMENTO" -ForegroundColor Yellow
Write-Host "  -----------------------"
Write-Host "  Pasta:  $Raiz"
Write-Host "  Jogo:   http://localhost:$Porta/jogo/"
Write-Host ""
Write-Host "  Feche esta janela para encerrar o treinamento."
Write-Host ""

while ($true) {
  $cliente = $null
  try {
    $cliente = $ouvinte.AcceptTcpClient()
    $cliente.NoDelay = $true
    $fluxo = $cliente.GetStream()
    $fluxo.ReadTimeout = 8000

    # linha de requisicao + cabecalhos (lidos byte a byte para nao bufferizar o corpo)
    $sb = New-Object System.Text.StringBuilder
    $anterior = 0
    $fim = $false
    while (-not $fim) {
      $b = $fluxo.ReadByte()
      if ($b -lt 0) { break }
      [void]$sb.Append([char]$b)
      if ($b -eq 10 -and $anterior -eq 10) { $fim = $true }
      if ($b -eq 10) {
        $t = $sb.ToString()
        if ($t.EndsWith("`r`n`r`n") -or $t.EndsWith("`n`n")) { $fim = $true }
      }
      $anterior = $b
      if ($sb.Length -gt 16384) { break }
    }

    $linhas = $sb.ToString() -split "`r?`n"
    if (-not $linhas -or $linhas.Length -eq 0 -or [string]::IsNullOrWhiteSpace($linhas[0])) {
      $cliente.Close(); continue
    }
    $partes = $linhas[0].Trim() -split "\s+"
    $metodo = $partes[0]
    $alvo = if ($partes.Length -gt 1) { $partes[1] } else { "/" }

    $alvo = ($alvo -split "\?")[0]
    $alvo = ($alvo -split "#")[0]
    try { $alvo = [System.Uri]::UnescapeDataString($alvo) } catch { }
    if ($alvo.EndsWith("/")) { $alvo = $alvo + "index.html" }
    $rel = $alvo.TrimStart("/").Replace("/", "\")

    $achou = $false
    $completo = $null
    try {
      $completo = [System.IO.Path]::GetFullPath((Join-Path $Raiz $rel))
      if ($completo.StartsWith($Raiz, [System.StringComparison]::OrdinalIgnoreCase) -and
          (Test-Path -LiteralPath $completo -PathType Leaf)) {
        $achou = $true
      }
    } catch { $achou = $false }

    if ($achou) {
      $dados = [System.IO.File]::ReadAllBytes($completo)
      $ext = [System.IO.Path]::GetExtension($completo).ToLowerInvariant()
      $tipo = $tipos[$ext]
      if (-not $tipo) { $tipo = "application/octet-stream" }
      $cab = "HTTP/1.1 200 OK`r`nContent-Type: $tipo`r`nContent-Length: $($dados.Length)`r`nCache-Control: no-store`r`nAccess-Control-Allow-Origin: *`r`nConnection: close`r`n`r`n"
    } else {
      $dados = [System.Text.Encoding]::UTF8.GetBytes("404 - arquivo nao encontrado: $alvo")
      $cab = "HTTP/1.1 404 Not Found`r`nContent-Type: text/plain; charset=utf-8`r`nContent-Length: $($dados.Length)`r`nConnection: close`r`n`r`n"
    }

    $bcab = [System.Text.Encoding]::ASCII.GetBytes($cab)
    $fluxo.Write($bcab, 0, $bcab.Length)
    if ($metodo -ne "HEAD" -and $dados.Length -gt 0) {
      $fluxo.Write($dados, 0, $dados.Length)
    }
    $fluxo.Flush()
  } catch {
    # conexao interrompida pelo navegador: segue para a proxima
  } finally {
    if ($cliente) { try { $cliente.Close() } catch { } }
  }
}
