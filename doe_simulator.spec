# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for DOE Simulator executable.
Bundles the Streamlit app with all dependencies into a standalone folder
"""

block_cipher = None

a = Analysis(
    ['run_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app.py', '.'),
        ('doe_model.py', '.'),
    ],
    hiddenimports=[
        'streamlit',
        'plotly',
        'pandas',
        'numpy',
        'statsmodels',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DOE_Simulator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='DOE_Simulator'
)
