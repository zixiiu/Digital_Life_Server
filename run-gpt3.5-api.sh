#!/bin/bash
SCRIPT_NAME="SocketServer.py"
CHATVER=3
server_ip="localhost"
PROXY="http://127.0.0.1:7890"
STREAM="True"
CHARACTER="paimon"
MODEL="gpt-3.5"

# demo by lancher
# python %SCRIPT_NAME% --chatVer N/A --APIKey N/A --ip 192.168.31.207 --accessToken N/A --proxy N/A --paid False --brainwash False --model N/A --stream False --character N/A

# Chatgpt
#python $SCRIPT_NAME --chatVer $CHATVER --APIKey $OPENAI_API_KEY --proxy $PROXY --stream $STREAM --model $MODEL --character $CHARACTER
# ERNIE-Bot-4
#python $SCRIPT_NAME --stream $STREAM --SecretKey $EB4_SK --APIKey $EB4_APIKey --model $MODEL --character $CHARACTER
python $SCRIPT_NAME --stream $STREAM --accessToken $accessToken --model $MODEL --character $CHARACTER