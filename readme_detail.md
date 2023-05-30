## 搭建”数字生命“服务:
> ⚠ 注意：  
> 如果不知道你在干什么（纯小白），请在**需要存放该项目的位置**打开终端(Win11)或Powershell(win10)，然后**按照下述说明逐步操作**即可  
> 在进行以下操作前，请确保电脑中有Git和Python>=3.8
### 克隆仓库
```bash
git clone https://github.com/zixiiu/Digital_Life_Server.git --recursive
cd Digital_Life_Server
```
### 保姆式配置环境
1. 使用virtualvenv建立python虚拟环境
```bash
python -m venv venv
```
2. 安装pytorch于venv

> 你可以在终端(或Powershell)输入`nvcc --version`，找到输出中`Cuda compilation tools`一行来查看cuda版本

对于cuda11.8： 

（默认地址，下载可能较慢）
```bash
.\venv\Scripts\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
（国内加速地址，下载可能较快）
```bash
.\venv\Scripts\python.exe -m pip install torch==2.0.0+cu118 torchvision torchaudio -f https://mirror.sjtu.edu.cn/pytorch-wheels/torch_stable.html
```

对于没有Nvidia显卡的电脑：

（默认地址，下载可能较慢）
```bash
.\venv\Scripts\python.exe -m pip install torch torchvision torchaudio
```
（国内加速地址，下载可能较快）
```bash
.\venv\Scripts\python.exe -m pip install torch==2.0.0+cpu torchvision torchaudio -f https://mirror.sjtu.edu.cn/pytorch-wheels/torch_stable.html

```
其余版本组合可以从[这个页面](https://pytorch.org/get-started/locally)获取具体的下载指令  

3. 安装项目所需其它依赖项
 ```bash
.\venv\Scripts\python.exe -m pip install -r requirements_out_of_pytorch.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
 ```
4. Build `monotonic_align`
```bash
cd "TTS/vits/monotonic_align"
mkdir monotonic_align
python setup.py build_ext --inplace
cp monotonic_align/*.pyd .
```

5. （对于**没有**Nvidia显卡的电脑，采用cpu来跑的话）需要额外做一步：

​	将 Digital_Life_Server\TTS\TTService.py 文件下 36行

```
self.net_g = SynthesizerTrn(...).cuda()
修改为
self.net_g = SynthesizerTrn(...).cpu()
```

> 到这里，项目构建完毕

6. 下载项目所需模型  
   [百度网盘](https://pan.baidu.com/s/1EnHDPADNdhDl71x_DHeElg?pwd=75gr)  
   ASR Model:   
   to `/ASR/resources/models`  
   Sentiment Model:  
   to `/SentimentEngine/models`  
   TTS Model:  
   to `/TTS/models`

### 启动“数字生命“服务器
> ⚠ 注意：  
> 启动前，不要忘记根据实际情况修改bat文件中的具体配置
```bash
run-gpt3.5-api.bat
```