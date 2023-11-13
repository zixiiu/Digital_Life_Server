# 搭建”数字生命“服务

## 注意事项

⚠ **重要：** 如果你是初学者，请在**需要存放该项目的位置**打开终端（Win11）或Powershell（Win10）或Terminal（Linux），并**按照以下步骤操作**
。在开始前，请确保电脑中已安装Git和Conda。

## 安装步骤

### 克隆仓库

```bash
git clone https://github.com/liegu0317/Digital_Life_Server.git --recursive
cd Digital_Life_Server
```

### 保姆式配置环境

#### 1. 使用conda建立python虚拟环境

```bash
conda create --name py39 python=3.9
```

#### 2. 安装pytorch于`py39`环境

- 激活`py39`环境
  ```bash
  conda activate py39
  ```
- 查看cuda版本
  ```bash
  nvcc --version
  ```

**对于cuda11.8：**

- 默认地址（下载可能较慢）
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
  ```
- 国内加速地址（下载可能较快）
  ```bash
  pip install torch==2.0.0+cu118 torchvision torchaudio -f https://mirror.sjtu.edu.cn/pytorch-wheels/torch_stable.html
  ```

**对于没有Nvidia显卡的电脑：**

- 默认地址（下载可能较慢）
  ```bash
  pip install torch torchvision torchaudio
  ```
- 国内加速地址（下载可能较快）
  ```bash
  pip install torch==2.0.0+cpu torchvision torchaudio -f https://mirror.sjtu.edu.cn/pytorch-wheels/torch_stable.html
  ```

- [其他版本组合指南](https://pytorch.org/get-started/locally)

#### 3. 安装项目所需其它依赖项

- Linux：
  先安装portaudio
  ```bash
  apt install portaudio19-dev # yum install portaudio-devel 
  ```
  然后安装其他依赖
  ```bash
  pip install -r requirements_out_of_pytorch.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```
- Windows：
  ```bash
  pip install -r requirements_out_of_pytorch.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```

#### 4. 构建 `monotonic_align`

```bash
cd "TTS/vits/monotonic_align"
mkdir monotonic_align
python setup.py build_ext --inplace
cp monotonic_align/*.pyd . # linux修改为cp monotonic_align/*.so
```

#### 5. 对于不使用Nvidia显卡的电脑

- 修改 `Digital_Life_Server\TTS\TTService.py` 文件下的第57-61行，将 `SynthesizerTrn(...).cuda()` 改为 `SynthesizerTrn(...).cpu()`

> 到此，项目构建完毕。

#### 6. 下载项目所需模型

- [百度网盘](https://pan.baidu.com/s/1BkUnSte6Zso16FYlUMGfww?pwd=lg17)
- [阿里云盘](https://www.aliyundrive.com/s/jFvgsJVtV6g)
    - ASR Model: 放置于 `/ASR/resources/models`
    - Sentiment Model: 放置于 `/SentimentEngine/models`
    - TTS Model: 放置于 `/TTS/models`

## 启动“数字生命”服务器

⚠ **注意：** 启动前，请根据实际情况修改bat文件中的具体配置以及配置相关环境变量。

```bash
run-gpt3.5-api.bat
```

或

```bash
run-gpt3.5-api.sh
```

#### 全部参数

| 名称          | 描述                  | 备注                                                                                                        | 必填                          |
|-------------|---------------------|-----------------------------------------------------------------------------------------------------------|-----------------------------|
| chatVer     | 指定Chatbot的版本        | 1：session-token or 邮件&密码登录(未实现)<br />3：OPENAI_API_KEY登录 or 使用自定义接口                                        | ChatGPT                     |
| APIKey      | 应用秘钥                | 可选值：OPENAI_API_KEY、ERINEBot API Key                                                                       | ERINEBot、ChatGPT（chatVer=1） |
| SecretKey   | ERINEBot Secret Key | ERINEBot Secret Key                                                                                       | ERINEBot                    |
| accessToken | 会话标志码               | 可选值：[ERNIEBot accessToken](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Ilkkrb0i5)、OPEN_CHATGPT setCookie | ChatGPT（chatVer=1）          |
| paid        | 是否为ChatGPT plus     | True / Flase                                                                                              |                             |
| proxy       | 代理服务地址              | 代理服务的地址，例如http://127.0.0.1:7890                                                                           |                             |
| brainwash   | 洗脑模式                | 推荐在chatVer=3时开启                                                                                           |                             |
| model       | 调用的模型               | 指定使用的GPT模型，可选值：gpt-3.5、gpt-3.5-turbo、gpt-4、ERNIEBot                                                       | ALL                         |
| stream      | 流式回复                | 可有效减少响应时间，可选值：True、False                                                                                  | ALL                         |
| character   | 使用的角色               | 指定所使用的角色，可选值：paimon、yunfei                                                                                | ALL                         |

### 调用示例

- 调用ChatGPT命令行示例：
  ```
  python %SCRIPT_NAME% --chatVer %CHATVER%  --APIKey %OPENAI_API_KEY%  --proxy %PROXY% --stream %STREAM% --model %MODEL% --character %CHARACTER%
  ```
- 调用ERNIEBot命令行示例：
  ```
  python %SCRIPT_NAME% --stream %STREAM%  --SecretKey %EB4_SK% --APIKey %EB4_APIKey% --ip %server_ip% --model %MODEL% --character %CHARACTER%
  ```

