@echo off
setlocal
title Trabalho em Altura - aula e prova
cd /d "%~dp0.."
set PORTA=8765
set PASTA=%CD%

echo.
echo   TRABALHO EM ALTURA - aula e prova
echo   ---------------------------------
echo   Subindo o servidor local...
echo.

set MOTOR=

rem 1) Python pelo lancador oficial (py). Testa de verdade: a loja da Microsoft
rem    instala um 'python.exe' falso que nao executa nada.
for /f "delims=" %%i in ('py -3 -c "print(42)" 2^>nul') do set TESTE=%%i
if "%TESTE%"=="42" set MOTOR=PY
if defined MOTOR goto achou

set TESTE=
for /f "delims=" %%i in ('python -c "print(42)" 2^>nul') do set TESTE=%%i
if "%TESTE%"=="42" set MOTOR=PYTHON
if defined MOTOR goto achou

set MOTOR=POWERSHELL

:achou
if "%MOTOR%"=="PY" (
  echo   Usando Python ^(py -3^).
  start "servidor do treinamento" /min py -3 -m http.server %PORTA% --bind 127.0.0.1
)
if "%MOTOR%"=="PYTHON" (
  echo   Usando Python.
  start "servidor do treinamento" /min python -m http.server %PORTA% --bind 127.0.0.1
)
if "%MOTOR%"=="POWERSHELL" (
  echo   Sem Python nesta maquina: usando o servidor do proprio Windows.
  start "servidor do treinamento" /min powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0servidor.ps1" -Porta %PORTA% -Raiz "%PASTA%"
)

rem espera a porta responder antes de abrir o navegador
set /a TENTA=0
:laco
set /a TENTA+=1
powershell -NoProfile -Command "try{$c=New-Object Net.Sockets.TcpClient('127.0.0.1',%PORTA%);$c.Close();exit 0}catch{exit 1}" >nul 2>nul
if not errorlevel 1 goto abrir
if %TENTA% GEQ 40 goto falhou
ping -n 2 127.0.0.1 >nul
goto laco

:abrir
start "" http://localhost:%PORTA%/jogo/
echo.
echo   Pronto. O jogo abriu em  http://localhost:%PORTA%/jogo/
echo   O servidor ficou na janela minimizada "servidor do treinamento".
echo   Para encerrar o treinamento, feche aquela janela.
echo.
timeout /t 8 >nul
exit /b 0

:falhou
echo.
echo   NAO CONSEGUI SUBIR O SERVIDOR NA PORTA %PORTA%.
echo.
echo   O que costuma resolver:
echo     1. Outro programa ja esta usando a porta 8765. Edite este arquivo e troque
echo        o numero em  set PORTA=8765  por  8766  (e tente de novo).
echo     2. O antivirus ou a politica da empresa bloqueou o PowerShell.
echo        Nesse caso instale o Python em python.org (marque "Add to PATH")
echo        e rode este arquivo de novo.
echo.
pause
exit /b 1
