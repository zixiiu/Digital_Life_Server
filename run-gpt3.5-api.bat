SCRIPT_NAME=SocketServer.py
CHATVER=3
PROXY=http://127.0.0.1:7890
STREAM=False
CHARACTER=paimon
MODEL=gpt-3.5-turbo
echo $SCRIPT_NAME

python $SCRIPT_NAME --chatVer $CHATVER --stream $STREAM --character $CHARACTER --model $MODEL
