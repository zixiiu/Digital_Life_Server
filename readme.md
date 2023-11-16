# Digital Life Server

这是「数字生命」服务部分代码。包括与前端通信，语音识别，chatGPT接入和语音合成。  
For other part of the project, please refer to:  
[Launcher](https://github.com/Liegu0317/DL_Launcher) 启动此服务器的图形界面。  
[UE Client](https://github.com/LIEGU0317/DigitalLife) 用于渲染人物动画，录音，和播放声音的前端部分。    
详细的配置流程可参见[readme_detail.md](readme_detail.md)

## Getting stuffs ready to roll:

### Clone this repo
> 注意clone代码带有[`--recursive`](https://git-scm.com/book/zh/v2/Git-%E5%B7%A5%E5%85%B7-%E5%AD%90%E6%A8%A1%E5%9D%97)参数

```bash
git clone https://github.com/liegu0317/Digital_Life_Server.git --recursive
```

### Install prerequisites

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
   cp monotonic_align/*.pyd .
   ```

4. Download models  
   [百度网盘](https://pan.baidu.com/s/1EnHDPADNdhDl71x_DHeElg?pwd=75gr)  
   ASR Model:   
   to `/ASR/resources/models`  
   Sentiment Model:  
   to `/SentimentEngine/models`  
   TTS Model:  
   to `/TTS/models`

5. （对于**没有**Nvidia显卡的电脑，采用cpu来跑的话）需要额外做一步：

   将 Digital_Life_Server\TTS\TTService.py 文件下 36行

   ```
   self.net_g = SynthesizerTrn(...).cuda()
   修改为
   self.net_g = SynthesizerTrn(...).cpu()
   ```

> 到这里，项目构建完毕🥰

### Start the server

   ```bash
   run-gpt3.5-api.bat # run-gpt3.5-api.sh
   ```