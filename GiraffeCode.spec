# -*- mode: python ; coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
try:
    from PIL import Image
    from src.otter_assets import _build_otter_pil, _build_fish_pil, _create_walk_frames_pil
    _assets_dir = os.path.abspath('assets')
    if not os.path.exists(os.path.join(_assets_dir, 'otter.png')):
        _o = _build_otter_pil()
        _f = _build_fish_pil()
        _w1, _w2 = _create_walk_frames_pil(_o)
        _o.save(os.path.join(_assets_dir, 'otter.png'), 'PNG')
        _w1.save(os.path.join(_assets_dir, 'otter_walk1.png'), 'PNG')
        _w2.save(os.path.join(_assets_dir, 'otter_walk2.png'), 'PNG')
        _f.save(os.path.join(_assets_dir, 'fish.png'), 'PNG')
        _o.resize((72, 72), Image.Resampling.LANCZOS).save(os.path.join(_assets_dir, 'emoji_otter.png'), 'PNG')
        _f.resize((72, 72), Image.Resampling.LANCZOS).save(os.path.join(_assets_dir, 'emoji_fish.png'), 'PNG')
except Exception as _e:
    print(f"Warning: could not pre-generate otter assets: {_e}")

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets/*', 'assets')],
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
    name='GiraffeCode',
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
    icon=['assets/icon.ico'],
)
