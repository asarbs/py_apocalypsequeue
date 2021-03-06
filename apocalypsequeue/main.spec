# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
    ('maps/*.jpg', 'maps'),
    ('maps/*.map', 'maps'),
    ('icons/*.png', 'icons'),
    ('system/simulation_editor_theme.json', '.'),
    ('C:/Users/asarb/PycharmProjects/py_apocalypsequeue/venv/Lib/site-packages/pygame_gui/data/*.json', 'pygame_gui/data'),
    ('C:/Users/asarb/PycharmProjects/py_apocalypsequeue/venv/Lib/site-packages/pygame_gui/data/*.ttf', 'pygame_gui/data')
]

a = Analysis(['main.py'],
             pathex=['C:\\Users\\asarb\\PycharmProjects\\py_apocalypsequeue\\apocalypsequeue'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
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
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
