# -*- mode: python -*-

block_cipher = None


a = Analysis(['AutoScrapy.py'],
             pathex=['C:\\Users\\Administrator\\Desktop\\python\\AutoTtScrapy'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='AutoScrapy',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='C:\\Users\\Administrator\\Desktop\\cat.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='AutoScrapy')
