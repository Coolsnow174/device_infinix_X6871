#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Extract with official LineageOS lineage-23.0 extract-utils.

Set EXTRACT_UTILS_PATH outside an Android checkout. --output selects the
physical vendor directory without changing Android build-time paths.
"""
import os
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
candidate = Path(os.environ.get('EXTRACT_UTILS_PATH', here.parents[2] / 'tools/extract-utils'))
sys.path.insert(0, str(candidate))
from extract_utils.main import ExtractUtils, ExtractUtilsModule

output = None
if '--output' in sys.argv:
    i = sys.argv.index('--output')
    output = Path(sys.argv[i + 1]).resolve()
    del sys.argv[i:i + 2]
# Resolve DT_NEEDED names to the selected stock module names. Prefer the
# partition root over hw/SoC implementations with duplicate basenames.
from functools import partial

def mapped_lib(module_name, lib, partition):
    return module_name

providers = {}
for line in (here / 'proprietary-files.txt').read_text().splitlines():
    if ';MODULE=' not in line:
        continue
    path = line.lstrip('-').split(';')[0]
    if not path.endswith('.so'):
        continue
    name = Path(path).stem
    module_name = line.split(';MODULE=')[1].split(';')[0]
    score = (path.count('/'), not path.startswith('vendor/'), path)
    if name not in providers or score < providers[name][0]:
        providers[name] = (score, module_name)
fixups = {name: partial(mapped_lib, value[1]) for name, value in providers.items()}
module = ExtractUtilsModule('X6871', 'infinix', lib_fixups=fixups, namespace_imports=[
    'device/infinix/X6871', 'hardware/mediatek', 'hardware/transsion',
])
module.device_path = str(here)
# The constructor resolves the default file list before device_path is changed.
module.proprietary_files.clear()
module.add_proprietary_file('proprietary-files.txt')
if output:
    module.vendor_path = str(output)
    module.vendor_rro_path = str(output / 'rro_overlays')
if __name__ == '__main__':
    ExtractUtils.device(module).run()
