@echo off
set SCRIPT_NAME=SocketServer.py
@REM 指定对话的版本 1 Token Email&Password 3 OPENAI_API_TOKEN
set CHATVER=3
@REM 自定义GPTAPIKEY
@REM set APIKEY=%OPENAI_API_KEY%
@REM 文心SecretKey
@REM set SecretKey=
@REM server_ip
set server_ip=localhost
@REM 指定代理服务器的地址
set PROXY=http://127.0.0.1:7890
@REM 指定是否以流式方式进行对话
set STREAM=True
@REM 指定角色的名称 paimon yunfei catmaid
set CHARACTER=paimon
@REM 指定使用的GPT模型 gpt-3.5 gpt-3.5-turbo gpt-4 ERNIEBot
set MODEL=gpt-3.5

@REM demo by lancher
@REM python %SCRIPT_NAME% --chatVer N/A --APIKey N/A --ip 192.168.31.207 --accessToken N/A --proxy N/A --paid False --brainwash False --model N/A --stream False --character N/A

@REM Chatgpt
python %SCRIPT_NAME% --chatVer %CHATVER%  --APIKey %OPENAI_API_KEY%  --proxy %PROXY% --stream %STREAM% --model %MODEL% --character %CHARACTER%
@REM ERNIE-Bot-4
@REM python %SCRIPT_NAME% --stream %STREAM%  --SecretKey %EB4_SK% --APIKey %EB4_APIKey% --ip %server_ip% --model %MODEL% --character %CHARACTER%

