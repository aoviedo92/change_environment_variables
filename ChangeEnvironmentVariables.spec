# -*- mode: python -*-
a = Analysis(['change_env_var.py'],
             pathex=['D:\\adri\\work\\PycharmProjects\\change_environment_variables'],
             hiddenimports=['atexit'],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='ChangeEnvironmentVariables.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='icon.ico')
