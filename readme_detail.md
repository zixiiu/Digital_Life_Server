## 搭建”数字生命“服务:

> ⚠ 注意：  
> 如果不知道你在干什么（纯小白），请在**需要存放该项目的位置**打开终端(Win11)或Powershell(win10)，然后**按照下述说明逐步操作
**即可  
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

 将 Digital_Life_Server\TTS\TTService.py 文件下 36行

```
self.net_g = SynthesizerTrn(...).cuda()
修改为
self.net_g = SynthesizerTrn(...).cpu()
```

> 到这里，项目构建完毕

6. 下载项目所需模型  
   [百度网盘](https://pan.baidu.com/s/1BkUnSte6Zso16FYlUMGfww?pwd=lg17)  、[阿里云盘](https://www.aliyundrive.com/s/jFvgsJVtV6g)
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

#### 全部参数

| 名称        | 描述                | 备注                                                         | 必填                           |
| ----------- | ------------------- | ------------------------------------------------------------ | ------------------------------ |
| chatVer     | 指定Chatbot的版本   | 1：setCookice登录<br />3：OPENAI_API_KEY登录                 | ChatGPT                        |
| APIKey      | 应用秘钥            | 可选值：OPENAI_API_KEY、ERINEBot API Key                     | ERINEBot、ChatGPT（chatVer=1） |
| SecretKey   | ERINEBot Secret Key | ERINEBot Secret Key                                          | ERINEBot                       |
| accessToken | 会话标志码          | 可选值：[ERNIEBot accessToken](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Ilkkrb0i5)、OPEN_CHATGPT setCookie | ChatGPT（chatVer=1）           |
| paid        | 是否为ChatGPT plus  | True / Flase                                                 |                                |
| proxy       | 代理服务地址        | 代理服务的地址，例如http://127.0.0.1:7890                    |                                |
| brainwash   | 洗脑模式            | 推荐在chatVer=3时开启                                        |                                |
| model       | 调用的模型          | 指定使用的GPT模型，可选值：gpt-3.5、gpt-3.5-turbo、gpt-4、ERNIEBot | ALL                            |
| stream      | 流式回复            | 可有效减少响应时间，可选值：True、False                      | ALL                            |
| character   | 使用的角色          | 指定所使用的角色，可选值：paimon、yunfei                     | ALL                            |

调用ChatGPT的命令行示例：

```
python %SCRIPT_NAME% --chatVer %CHATVER%  --APIKey %OPENAI_API_KEY%  --proxy %PROXY% --stream %STREAM% --model %MODEL% --character %CHARACTER%
```

调用ERNIEBot（文心一言）的命令行示例：

```
python %SCRIPT_NAME% --stream %STREAM%  --SecretKey %EB4_SK% --APIKey %EB4_APIKey% --ip %server_ip% --model %MODEL% --character %CHARACTER%
```

