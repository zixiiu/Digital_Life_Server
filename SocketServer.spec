# -*- mode: python ; coding: utf-8 -*-

import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5)

from PyInstaller.utils.hooks import collect_all
import inspect
import torch


def collect_all_and_add_to_list(package_name, datas, binaries, hiddenimports):
    for package in package_name:
        package_datas, package_binaries, package_hiddenimports = collect_all(package)
        datas.extend(package_datas)
        binaries.extend(package_binaries)
        hiddenimports.extend(package_hiddenimports)

datas, binaries, hiddenimports = [], [], []
package_lists = ['torch', 'tqdm', 'regex', 'requests', 'packaging', 'filelock', 'numpy', 'tokenizers']
collect_all_and_add_to_list(package_lists, datas, binaries, hiddenimports)


block_cipher = None

def collect_source_files(modules):
    datas = []
    for module in modules:
        source = inspect.getsourcefile(module)
        dest = f"src.{module.__name__}"  # use "src." prefix
        datas.append((source, dest))
    return datas

source_files = collect_source_files([torch])
source_files_toc = TOC((name, path, 'DATA') for path, name in source_files)


datas.append(('venv\lib\site-packages\librosa', 'librosa'))
datas.append(('venv\lib\site-packages\cn2an', 'cn2an'))
datas.append(('TTS\models', 'TTS\models'))
datas.append(('venv\lib\site-packages\jieba','jieba'))
datas.append(('ASR', 'ASR'))
datas.append(('GPT\prompts_default', 'GPT\prompts_default'))
datas.append(('tmp', 'tmp'))
datas.append(('SentimentEngine\models\paimon_sentiment.onnx', 'SentimentEngine\models'))
hiddenimports.extend(['tiktoken_ext.openai_public','tiktoken_ext'])


a = Analysis(
    ['SocketServer.py'],
    pathex=['TTS/vits'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['torch.distributions'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, source_files_toc, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SocketServer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SocketServer',
)
