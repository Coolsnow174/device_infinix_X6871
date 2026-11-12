#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate configs/properties/*.prop from the XOS16 dump build.prop files."""

import os
import re
import sys

DUMP = sys.argv[1] if len(sys.argv) > 1 else '/root/X6871/XOS16'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'configs', 'properties')

PARTS = {
    'system': 'system/system',
    'system_ext': 'system_ext/etc',
    'vendor': 'vendor',
    'odm': 'odm/etc',
    'product': 'product/etc',
    'vendor_dlkm': 'vendor_dlkm/etc',
    'odm_dlkm': 'odm_dlkm/etc',
    'system_dlkm': 'system_dlkm/etc',
}

# Props set by the build system / product config -> skip
SKIP_PATTERNS = (
    re.compile(r'^import\s'),
    re.compile(r'^ro\.build\.'),
    re.compile(r'^ro\.product\.'),
    re.compile(r'^ro\.system\.'),
    re.compile(r'^ro\.\w+\.build\.'),
    re.compile(r'^ro\.bootimage\.build\.'),
    re.compile(r'^ro\.odm\.build\.'),
    re.compile(r'^ro\.bootimage\.'),
    re.compile(r'^ro\.boot\.'),
    re.compile(r'^ro\.boot2\.'),
    re.compile(r'^ro\.actionable\.'),
    re.compile(r'^ro\.cpu\.'),
    re.compile(r'^ro\.dalvik\.'),
    re.compile(r'^ro\.first_api_level$'),
    re.compile(r'^ro\.board\.api'),
    re.compile(r'^ro\.kernel\.'),
    re.compile(r'^ro\.vndk\.'),
    re.compile(r'^ro\.zygote\.'),
    re.compile(r'^ro\.art\.'),
    re.compile(r'^ro\.crypto\.'),
    re.compile(r'^ro\.seprimary'),
    re.compile(r'^ro\.hwui\.'),
    re.compile(r'^ro\.config\.'),
    re.compile(r'^ro\.config\.'),
    re.compile(r'^ro\.vendor\.rom\.'),
    re.compile(r'^oem\.'),
    re.compile(r'^pm\.'),
    re.compile(r'^dpm\.'),
    re.compile(r'^ims\.'),
    re.compile(r'^mtk\.'),
)

KEEP = (
    'ro.build.characteristics',
)


def load(path):
    if not os.path.isfile(path):
        return []
    out = []
    with open(path, errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            k, v = line.split('=', 1)
            k, v = k.strip(), v.strip()
            if not v:
                continue
            out.append((k, v))
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for part, path in PARTS.items():
        props = []
        seen = set()
        for prop_file in ('build.prop', 'rw.prop', 'ro.prop'):
            for k, v in load(os.path.join(DUMP, path, prop_file)):
                if k in seen:
                    continue
                seen.add(k)
                if k in KEEP:
                    pass
                elif any(p.match(k) for p in SKIP_PATTERNS):
                    continue
                props.append((k, v))
        props.sort()
        with open(os.path.join(OUT, part + '.prop'), 'w') as f:
            f.write('# SPDX-FileCopyrightText: The LineageOS Project\n')
            f.write('# SPDX-License-Identifier: Apache-2.0\n')
            f.write('#\n')
            f.write('# Generated from the XOS 16.3.0.155SP20 (BP2A.250605.031.A3) dump.\n')
            f.write('#\n\n')
            for k, v in props:
                f.write(f'{k}={v}\n')
        total += len(props)
        print(f'{part}: {len(props)} props')
    print(f'Total: {total}')


if __name__ == '__main__':
    main()
