# Digital Life Server
这是「数字生命」服务部分代码。包括与前端通信，语音识别，chatGPT接入和语音合成。  
For other part of the project, please refer to:  
[Launcher](https://github.com/CzJam/DL_Launcher) 启动此服务器的图形界面。  
[UE Client](https://github.com/QSWWLTN/DigitalLife) 用于渲染人物动画，录音，和播放声音的前端部分。    
详细的配置流程可参见[readme_detail.md](readme_detail.md)
## Getting stuffs ready to roll:
### Clone this repo
```bash
git clone https://github.com/zixiiu/Digital_Life_Server.git --recursive
```
### Install prerequisites
建议看[readme_detail.md](readme_detail.md)
1. install pytorch
    ```bash
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    ```
2. install other requirements
    ```bash
    pip install -r requirements.txt
    ```
3. Build `monotonic_align`  
   This may not work that well but you know what that suppose to mean.
   ```bash
   cd "TTS/vits/monotonic_align"
   mkdir monotonic_align
   python setup.py build_ext --inplace
   cp monotonic_align/*.so .
   ```
   
4. Download models  
   [百度网盘](https://pan.baidu.com/s/1EnHDPADNdhDl71x_DHeElg?pwd=75gr)  
   ASR Model:   
   to `/ASR/resources/models`  
   Sentiment Model:  
   to `/SentimentEngine/models`  
   TTS Model:  
   to `/TTS/models`

### Start the server
   ```bash
   run-gpt3.5-api.bat
   ```