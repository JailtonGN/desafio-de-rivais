# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['DesafioDeRivais2.0.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('sons', 'sons'),
        ('imagens', 'imagens'),
        ('configuracoes.json', '.'),
        ('palavras.json', '.'),
        ('ranking_solo.json', '.'),
        ('dicio_cache.json', '.'),
        ('palavras_usadas.json', '.'),
        ('palavras_invalidas.json', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='DesafioDeRivais2.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
