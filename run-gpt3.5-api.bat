@echo off
set SCRIPT_NAME=SocketServer.py
@REM 指定对话的版本
set CHATVER=3
@REM 指定代理服务器的地址
set PROXY=http://127.0.0.1:7890
@REM 指定是否以流式方式进行对话
set STREAM=False
@REM 指定角色的名称
set CHARACTER=catmaid
@REM 指定使用的GPT模型
set MODEL=gpt-3.5-turbo


python %SCRIPT_NAME% --chatVer %CHATVER% --stream %STREAM% --character %CHARACTER% --model %MODEL%