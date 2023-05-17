## 搭建”数字生命“服务:
> ⚠ 注意：  
> 现在是linux(ubuntu)的配置。使用python3.8
### 克隆仓库
```bash
git clone https://github.com/seanxpw/Digital_Life_Server.git -b linux_ver_python3.8 --recursive
cd Digital_Life_Server
```
### 配置环境
**需要显卡，且需要cuda11.8**
1. 使用conda建立python虚拟环境
```bash
conda env create -f environment.yaml
```
这样会自动创建一个名字叫dlife的环境
如果报错的话先下载pytorch就好。
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

requirements.txt是pip的，没有anaconda可以一试，不过yaml这个包好像是用conda装的
到时候自己注意点。

2. Build `monotonic_align`
```bash
cd "TTS/vits/monotonic_align"
mkdir monotonic_align
python setup.py build_ext --inplace
cp monotonic_align/*.so .
```

> 到这里，项目构建完毕🥰

3. 下载项目所需模型  
[百度网盘](https://pan.baidu.com/s/1EnHDPADNdhDl71x_DHeElg?pwd=75gr)
视频简介下面也有别的网盘的链接。在里面找对应的目录就行。
注意TTS的一个模型名字应该是paimon6k_390k.pth  
如果下载的是paimon6k_390000.pth请把名字修改为paimon6k_390k.pth

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

实测python3.8会报一个版本检查的错误
在lib/python3.8/site-packages/revChatGPT/__init__.py,line 23
把数字9改成8就行