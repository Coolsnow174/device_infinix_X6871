#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the initial proprietary-files.txt for X6871 (XOS16) from the dump."""

import os
import sys

DUMP = sys.argv[1] if len(sys.argv) > 1 else '/root/X6871/XOS16'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'proprietary-files.txt')

PARTITIONS = {
    'vendor': 'vendor',
    'odm': 'odm',
}

# Files handled by the device tree itself (do not list as blobs)
EXCLUDE = {
    # Properties (generated into configs/properties)
    'build.prop', 'ro.prop', 'rw.prop',
    'etc/build.prop', 'etc/ro.prop', 'etc/rw.prop',
    # Init files shipped from init/
    'etc/init/hw/init.cgroup.rc',
    'etc/init/hw/init.connectivity.common.rc',
    'etc/init/hw/init.connectivity.rc',
    'etc/init/hw/init.modem.rc',
    'etc/init/hw/init.mt6895.rc',
    'etc/init/hw/init.mt6895.usb.rc',
    'etc/init/hw/init.mtkgki.rc',
    'etc/init/hw/init.project.rc',
    'etc/init/hw/init.sensor_2_0.rc',
    'ueventd.rc',
    'etc/ueventd.rc',
    # Audio effects config shipped from configs/
    'etc/vconfig/audio/audio_effects_config.xml',
    # VINTF shipped from configs/
    'etc/vintf/manifest.xml',
    'etc/vintf/compatibility_matrix.xml',
    # Keylayout shipped from configs/
    'usr/keylayout/mtk-tpd.kl',
    'usr/keylayout/mtk-pmic-keys.kl',
    # NOTICE files
    'etc/NOTICE.xml.gz',
    'NOTICE.xml.gz',
    # AOSP-built wifi stack binaries (built from device.mk)
    'bin/hw/hostapd',
    'bin/hw/wpa_supplicant',
    'bin/wlan_assistant',
    # fstab shipped from init/
    'etc/fstab.mt6895',
    # AOSP-built insmod helper
    'bin/init.insmod.sh',
    # HAL services rebuilt from AOSP source (clearkey DRM only)
    'bin/hw/android.hardware.drm-service.clearkey',
    'bin/hw/android.hardware.thermal-service.mediatek',
    'bin/hw/android.hardware.usb-aidl-service.mediatek',
    'bin/hw/android.hardware.usb.gadget-aidl-service.mediatek',
    'bin/hw/android.hardware.health-service.example',
    'bin/hw/android.hardware.wifi-service-lazy',
    'etc/init/android.hardware.drm-service.clearkey.rc',
    'etc/init/android.hardware.thermal-service-mediatek.rc',
    'etc/init/android.hardware.usb-aidl-service.mediatek.rc',
    'etc/init/android.hardware.usb.gadget-aidl-service.mediatek.rc',
    'etc/init/android.hardware.health-service.example.rc',
    'etc/init/android.hardware.wifi-service-lazy.rc',
    'etc/vintf/manifest/android.hardware.drm-service.clearkey.xml',
    'etc/vintf/manifest/android.hardware.thermal-mediatek.xml',
    'etc/vintf/manifest/android.hardware.usb-aidl-service.mediatek.xml',
    'etc/vintf/manifest/android.hardware.usb.gadget-aidl-service.mediatek.xml',
    'etc/vintf/manifest/android.hardware.health-service.example.xml',
    # Permission XMLs provided by AOSP soong modules (device.mk PRODUCT_PACKAGES)
    'etc/permissions/android.hardware.hardware_keystore_V3.xml',
    'etc/permissions/android.hardware.sensor.accelerometer.prebuilt.xml',
    'etc/permissions/android.hardware.sensor.compass.prebuilt.xml',
    'etc/permissions/android.hardware.sensor.gyroscope.prebuilt.xml',
    'etc/permissions/android.hardware.sensor.light.prebuilt.xml',
    'etc/permissions/android.hardware.sensor.proximity.prebuilt.xml',
    'etc/permissions/android.hardware.sensor.stepcounter.prebuilt.xml',
    'etc/permissions/android.hardware.sensor.stepdetector.prebuilt.xml',
}

# AOSP builds these interface stubs and libraries; copying them as blobs
# would create duplicate module rules. Versioned AIDL/HIDL interface stubs
# (foo-V<n>-ndk.so) are excluded by regex - but MTK *implementations*
# (e.g. android.hardware.audio.core-impl-mediatek.so,
# android.hardware.biometrics.common.thread.so) do NOT match the versioned
# stub pattern and are kept as blobs.
import re

STUB_EXCLUDE_RE = re.compile(r'^(?:lib64|lib)/(?:android\.[\w.]+)-V[0-9]+-ndk(?:_platform)?\.so$')

STUB_EXCLUDE_EXACT = {
    'lib64/libpowermanager',
    'lib64/libhidlbase.so',
    'lib64/libhidlmemory.so',
    'lib64/libhidltransport.so',
    'lib64/libhwbinder.so',
    'lib64/libhwbinder_p81.so',
    'lib64/libc++.so',
    'lib64/libFMQ.so',
    'lib64/libhardware.so',
    'lib64/libvndksupport.so',
    'lib64/libnetutils.so',
    'lib64/libtinyxml2.so',
    'lib64/libtinyxml.so',
    'lib64/libpagemap.so',
    'lib64/libcodec2_hidl.so',
    'lib64/libstagefright_foundation.so',
    'lib64/libsqlite3.so',
    'lib64/libexpat.so',
    'lib64/libcurl.so',
    'lib64/libpng.so',
    'lib64/libcrypto.so',
    'lib64/libssl.so',
    'lib64/libz.so',
    'lib64/liblzma.so',
    'lib64/libxml2.so',
    'lib64/libjpeg.so',
    'lib64/libspeexresampler.so',
    'lib64/libruy.so',
    'lib64/libblas.so',
    'lib64/libcap.so',
    'lib64/libcompiler_rt.so',
    'lib64/libjsoncpp.so',
    'lib64/libnl.so',
    'lib64/libpcap.so',
    'lib64/libmnl.so',
    'lib64/libflatbuffers-cpp.so',
    'lib64/libimage_io.so',
    'lib64/libjpegdecoder.so',
    'lib64/libjpegencoder.so',
    'lib64/libtextclassifier_hash.so',
    'lib64/libtinyalsav2.so',
    'lib64/libultrahdr.so',
    'lib64/libminijail.so',
    'lib/libhidlbase.so',
    'lib/libc++.so',
    'lib/libFMQ.so',
    'lib/libhardware.so',
    'lib/libz.so',
    'lib/libexpat.so',
    'lib/libcrypto.so',
    'lib/libssl.so',
    'lib/libtinyxml2.so',
}

def stub_prefix(rel):
    if STUB_EXCLUDE_RE.match(rel) is not None or rel in STUB_EXCLUDE_EXACT:
        return True
    # AIDL compat files are handled in the prebuilt rename section
    if any(rel == p for p in AIDL_COMPAT):
        return True
    return False

# CM6-style "prebuilt AIDL compatibility": stubs whose version differs from the
# AOSP one; copy with a `_prebuilt` suffix and DISABLE_DEPS;FIX_SONAME.
AIDL_COMPAT = [
    'lib64/android.hardware.audio.effect-V2-ndk.so',
    'lib64/android.hardware.bluetooth.audio-V4-ndk.so',
    'lib64/android.hardware.audio.common-V3-ndk.so',
    'lib64/android.media.audio.common.types-V3-ndk.so',
    'lib64/av-audio-types-aidl-ndk.so',
    'lib64/libaudio_aidl_conversion_common_ndk.so',
    'lib64/vendor.mediatek.hardware.bluetooth.audio-V1-ndk.so',
    'lib64/libbluetooth_audio_session_aidl.so',
]

CATEGORY_ORDER = [
    'bin', 'hw', 'camera', 'sound', 'audio', 'bluetooth', 'graphics', 'display',
    'DRM', 'gnss', 'nfc', 'sensors', 'thermal', 'usb', 'wifi', 'net', 'modem',
    'power', 'vibrator', 'lights', 'init', 'etc', 'lib64', 'lib', 'firmware',
    'usr', 'kmsetkey', 'mcd', 'crossbuild', 'vconfig', 'bprm',
]


def category(path):
    parts = path.split('/')
    for p in parts:
        for c in CATEGORY_ORDER:
            if c.lower() in p.lower():
                return c
    return parts[0]


def excluded(part, rel):
    entry = f'{part}/{rel}'
    if rel in EXCLUDE or entry in EXCLUDE:
        return True
    return False



def get_device_packages():
    """Parse PRODUCT_PACKAGES blocks from device.mk."""
    pkg_path = os.path.join(HERE, '..', 'device.mk')
    pkgs = set()
    inblock = False
    for l in open(pkg_path):
        st = l.strip()
        if st.startswith('PRODUCT_PACKAGES'):
            inblock = True
            continue
        if not inblock:
            continue
        if not l.startswith((' ', '\t')) and not st.endswith('\\'):
            inblock = False
            continue
        if st.startswith('#') or not st:
            continue
        tok = st.rstrip('\\').strip()
        if tok:
            pkgs.add(tok)
        if not st.endswith('\\'):
            inblock = False
    return pkgs


def main():
    device_pkgs = get_device_packages()
    lines = {}          # (part, cat) -> set of lines
    real_entries = set()  # (part, rel)
    symlink_groups = {}   # (part, src_rel) -> list of symlink targets (as entry paths)
    symlink_files = set()  # (part, rel) - links themselves (not real files)

    for part, d in PARTITIONS.items():
        root = os.path.join(DUMP, d)
        for base, dirs, files in os.walk(root, followlinks=False):
            dirs.sort()
            for f in sorted(files):
                full = os.path.join(base, f)
                rel = os.path.relpath(full, root)
                if os.path.islink(full):
                    symlink_files.add((part, rel))
                    src = os.readlink(full)
                    # Resolve absolute symlinks within the same partition
                    if src.startswith('/'):
                        # /vendor/... -> vendor/... relative to dump root
                        for pd, pn in PARTITIONS.items():
                            pfx = '/' + pd + '/'
                            if src.startswith(pfx):
                                src_abs = os.path.join(DUMP, src[1:])
                                break
                        else:
                            # external mount (e.g. /mnt/vendor/mdota) - skip
                            continue
                    else:
                        src_abs = os.path.normpath(os.path.join(base, src))
                    src_rel = os.path.relpath(src_abs, root)
                    g = symlink_groups.setdefault((part, src_rel), [])
                    g.append(f'{part}/{rel}')
                    continue
                if excluded(part, rel):
                    continue
                if stub_prefix(rel):
                    continue
                # skip AOSP-built modules shipped as blobs (module name collision)
                stem = os.path.splitext(rel)[0].split('/')[-1]
                if stem in device_pkgs:
                    continue
                real_entries.add((part, rel))
                cat = category(rel)
                lines.setdefault((part, cat), set()).add(f'{part}/{rel}')

    n_symlinks = 0
    for (part, src_rel), targets in sorted(symlink_groups.items()):
        n_symlinks += len(targets)
        if (part, src_rel) in symlink_files:
            # dangling / symlink-to-symlink: skip
            continue
        src_is_real = (part, src_rel) in real_entries
        if not src_is_real and not os.path.isfile(os.path.join(DUMP, PARTITIONS[part], src_rel)):
            # src not in dump at all (external partition target): skip
            continue
        # skip if the source lib is an AOSP-built module (renamed modules excluded)
        if os.path.splitext(src_rel)[0].split('/')[-1] in device_pkgs:
            continue
        cat = category(src_rel)
        line = f'{part}/{src_rel};SYMLINK={",".join(sorted(targets))}'
        if src_is_real:
            line += ';MAKE_COPY_RULE_ONLY'
            # Remove the plain entry for this src to avoid duplicate module
            cat_set = lines.get((part, cat))
            if cat_set:
                cat_set.discard(f'{part}/{src_rel}')
        lines.setdefault((part, cat), set()).add(line)

    out = []
    out.append('# SPDX-FileCopyrightText: The LineageOS Project\n')
    out.append('# SPDX-License-Identifier: Apache-2.0\n')
    out.append('\n')
    out.append('# Generated from the XOS 16.3.0.155SP20 (BP2A.250605.031.A3) dump.\n')
    out.append('# Vendor and ODM partitions; vendor_dlkm/system_dlkm/odm_dlkm come\n')
    out.append('# from the X6871-kernel prebuilt tree, product is not shipped.\n')
    out.append('\n')
    out.append('# Audio prebuilt AIDL compatibility (version differs from AOSP)\n')
    for p in AIDL_COMPAT:
        for part in ('vendor', 'odm'):
            if os.path.isfile(os.path.join(DUMP, PARTITIONS[part], p)):
                out.append(f'{part}/{p}:vendor/{p[:-3]}_prebuilt.so;DISABLE_DEPS;FIX_SONAME\n')
    out.append('\n')

    n = 0
    for (part, cat) in sorted(
        lines.keys(),
        key=lambda k: (k[0], CATEGORY_ORDER.index(k[1]) if k[1] in CATEGORY_ORDER else 999, k[1]),
    ):
        title = f'{cat} ({part})' if len(PARTITIONS) > 1 else cat
        out.append(f'# {title}\n')
        for entry in sorted(lines[(part, cat)]):
            out.append(entry + '\n')
            n += 1
        out.append('\n')

    with open(OUT, 'w') as f:
        f.writelines(out)

    print(f'Wrote {n} entries, {n_symlinks} symlink targets to {OUT}')


if __name__ == '__main__':
    main()
