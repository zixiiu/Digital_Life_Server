# Digital Life Server
## Installation
### Requirements
- Nvidia GPU with CUDA support
### Clone the repo
```bash
git clone --recurse-submodules https://github.com/zixiiu/Digital_Life_Server.git 
```
### Getting everything ready
1. install pytorch
    ```bash
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    ```
2. install other requirements
    ```bash
    pip install -r requirements.txt
    ```
3. Build `monotonic_align`
   ```bash
   cd TTS/vits/monotonic_align
   midir monotonic_align
   python setup.py build_ext --inplace
   cp monotonic_align/*.pyd .
   ```
4. Download models from zoo:  
   ASR Model:   
   to `/ASR/resources/models`  
   Sentiment Model:  
   to `/SentimentEngine/models`  
   TTS Model:  
   to `/TTS/models`
5. Start the server
    ```bash
    run-gpt3.5-api.bat
    ```