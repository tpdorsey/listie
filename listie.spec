# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['listie.py'],
    pathex=[],
    binaries=[],
    datas=[('images','images')],
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
    [],
    exclude_binaries=True,
    name='Listie',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Listie',
)
app = BUNDLE(
    coll,
    name='Listie.app',
    icon='listie-icon.icns',
    bundle_identifier=None,
    info_plist={
        'NSHighResolutionCapable': 'True',
        'CFBundleShortVersionString': '2.0.0',
        'NSHumanReadableCopyright': '© Terrence Dorsey 2025'
    }
)
