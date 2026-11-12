#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2026 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)

from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)

from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/infinix/X6871',
    'hardware/mediatek',
]

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
}

blob_fixups: blob_fixups_user_type = {
    'vendor/bin/hw/android.hardware.media.c2-mediatek-64b': blob_fixup()
        .replace_needed('libavservices_minijail_vendor.so', 'libavservices_minijail.so'),
    'vendor/lib64/libmnl.so': blob_fixup()
        .add_needed('libcutils.so'),
    # Audio prebuilt AIDL compatibility: versioned stubs differ from the ones
    # AOSP builds, so they ship renamed as *_prebuilt.so and every dependent
    # blob gets its DT_NEEDED entry rewritten to the prebuilt name.
    'vendor/lib64/android.hardware.audio.effect-V2-ndk_prebuilt.so': blob_fixup()
        .replace_needed('android.hardware.audio.common-V3-ndk.so', 'android.hardware.audio.common-V3-ndk_prebuilt.so')
        .replace_needed('android.media.audio.common.types-V3-ndk.so', 'android.media.audio.common.types-V3-ndk_prebuilt.so'),
    'vendor/lib64/android.hardware.audio.common-V3-ndk_prebuilt.so': blob_fixup()
        .replace_needed('android.media.audio.common.types-V3-ndk.so', 'android.media.audio.common.types-V3-ndk_prebuilt.so'),
    'vendor/lib64/android.hardware.bluetooth.audio-V4-ndk_prebuilt.so': blob_fixup()
        .replace_needed('android.hardware.audio.common-V3-ndk.so', 'android.hardware.audio.common-V3-ndk_prebuilt.so'),
    ('vendor/lib64/hw/audio.primary.mediatek.so', 'vendor/lib64/hw/audio.primary.mt6895.so'): blob_fixup()
        .replace_needed('android.hardware.audio.effect-V2-ndk.so', 'android.hardware.audio.effect-V2-ndk_prebuilt.so')
        .replace_needed('android.hardware.bluetooth.audio-V4-ndk.so', 'android.hardware.bluetooth.audio-V4-ndk_prebuilt.so')
        .replace_needed('vendor.mediatek.hardware.bluetooth.audio-V1-ndk.so', 'vendor.mediatek.hardware.bluetooth.audio-V1-ndk_prebuilt.so')
        .replace_needed('libbluetooth_audio_session_aidl.so', 'libbluetooth_audio_session_aidl_prebuilt.so'),
    'vendor/lib64/libpowerhal.so': blob_fixup()
        .replace_needed('android.hardware.bluetooth.audio-V4-ndk.so', 'android.hardware.bluetooth.audio-V4-ndk_prebuilt.so'),
    ('vendor/lib64/android.hardware.bluetooth.audio-impl-mediatek.so', 'vendor/lib64/hw/vendor.mediatek.hardware.bluetooth.audio@2.1-impl.so', 'vendor/lib64/hw/vendor.mediatek.hardware.bluetooth.audio@2.2-impl.so', 'vendor/lib64/libbluetooth_audio_session_aidl_mtk.so'): blob_fixup()
        .replace_needed('vendor.mediatek.hardware.bluetooth.audio-V1-ndk.so', 'vendor.mediatek.hardware.bluetooth.audio-V1-ndk_prebuilt.so'),
    ('vendor/lib64/libbluetooth_audio_session_aidl_displayone.so', 'vendor/lib64/libbluetooth_audio_session_aidl_displaytwo.so', 'vendor/lib64/libbluetooth_audio_session_aidl_mtk.so'): blob_fixup()
        .replace_needed('vendor.mediatek.hardware.bluetooth.audio-V1-ndk.so', 'vendor.mediatek.hardware.bluetooth.audio-V1-ndk_prebuilt.so')
        .replace_needed('libbluetooth_audio_session_aidl.so', 'libbluetooth_audio_session_aidl_prebuilt.so'),
    'vendor/lib64/libbluetooth_audio_session_aidl_prebuilt.so': blob_fixup()
        .replace_needed('vendor.mediatek.hardware.bluetooth.audio-V1-ndk.so', 'vendor.mediatek.hardware.bluetooth.audio-V1-ndk_prebuilt.so'),
    'vendor/lib64/libbluetooth_audio_session.so': blob_fixup()
        .replace_needed('libbluetooth_audio_session_aidl.so', 'libbluetooth_audio_session_aidl_prebuilt.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'X6871',
    'infinix',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
