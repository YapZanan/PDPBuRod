# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['mainwindow.py'],
             pathex=['C:\\Users\\Naufal\\PycharmProjects\\pythonProject2\\venv\\lib\\site-packages\\cv2\\cv2.cp39-win_amd64.pyd', 'C:\\Users\\Naufal\\PycharmProjects\\pythonProject4\\Face_Detection_PyQt_Final'],
             binaries=[],
             datas=[],
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
          name='mainwindow',
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
               name='mainwindow')
