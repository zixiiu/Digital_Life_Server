@echo off
set SCRIPT_NAME=SocketServer.py
@REM set CHATVER=3
set server_ip=localhost
set PROXY=http://127.0.0.1:7890
set STREAM=True
set CHARACTER=paimon
set MODEL=ERNIE-Bot-4

@REM demo by lancher
@REM python %SCRIPT_NAME% --chatVer N/A --APIKey N/A --ip 192.168.31.207 --accessToken N/A --proxy N/A --paid False --brainwash False --model N/A --stream False --character N/A

@REM Chatgpt
@REM python %SCRIPT_NAME% --chatVer %CHATVER%  --APIKey %OPENAI_API_KEY%  --proxy %PROXY% --stream %STREAM% --model %MODEL% --character %CHARACTER%
@REM ERNIE-Bot-4
@REM python %SCRIPT_NAME% --stream %STREAM%  --SecretKey %EB4_SK% --APIKey %EB_APIKey% --model %MODEL% --character %CHARACTER%
python %SCRIPT_NAME% --stream %STREAM%  --accessToken  --model %MODEL% --character %CHARACTER%
