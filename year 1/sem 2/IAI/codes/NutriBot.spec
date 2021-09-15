# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['C:/Users/ACER/sy/Code/python/IAI/main.py'],
             pathex=['C:\\Users\\ACER\\sy\\Code\\python\\iai'],
             binaries=[('C:/Users/ACER/Downloads/pyspellchecker-master/spellchecker/resources/en.json.gz', 'spellchecker/resources')],
             datas=[('C:/Users/ACER/sy/Code/python/IAI/form.ui', '.'), ('C:/Users/ACER/sy/Code/python/IAI/icon.png', '.'), ('C:/Users/ACER/sy/Code/python/IAI/icon.ico', '.'), ('C:/Users/ACER/sy/Code/python/IAI/model.tflearn.data-00000-of-00001', '.'), ('C:/Users/ACER/sy/Code/python/IAI/model.tflearn.index', '.'), ('C:/Users/ACER/sy/Code/python/IAI/model.tflearn.meta', '.'), ('C:/Users/ACER/sy/Code/python/IAI/nutrient-food.txt', '.'), ('C:/Users/ACER/sy/Code/python/IAI/robot.png', '.'), ('C:/Users/ACER/sy/Code/python/IAI/robot.png', '.'), ('C:/Users/ACER/sy/Code/python/IAI/sendIcon.png', '.'), ('C:/Users/ACER/sy/Code/python/IAI/symptoms-not_to_eat.txt', '.'), ('C:/Users/ACER/sy/Code/python/IAI/symptoms-to_eat.txt', '.'), ('C:/Users/ACER/sy/Code/python/IAI/templates.json', '.')],
             hiddenimports=['keras-nightly', 'absl-py', 'protobuf', 'grpcio', 'six', 'termcolor', 'typing-extensions', 'google-pasta', 'wheel', 'keras_preprocessing', 'tensorflow_estimator', 'h5py', 'astunparse', 'gast', 'tensorboard', 'wrapt', 'flatbuffers', 'opt_einsum', 'numpy'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='NutriBot',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='C:\\Users\\ACER\\sy\\Code\\python\\IAI\\icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='NutriBot')
