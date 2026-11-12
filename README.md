# X6871 (Infinix GT 20 Pro 5G) - Android 16 device tree

LineageOS device tree for the Infinix GT 20 Pro 5G (`X6871`, Transsion board
`mgvi_64_64only_armv82`, MediaTek Dimensity 8200 Ultimate / MT6895), based on the
XOS 16.3.0.155SP20 (`BP2A.250605.031.A3`) vendor dump.

- Kernel: GKI `6.12.38-android16-5`, 64-bit only, no VNDK (board API `202504`)
- HALs: fully AIDL (composer3, allocator V2, audio core, camera provider,
  sensors multihal, keymint 3.0 Trustonic + secretkeeper, ...)
- Filesystems: EROFS for user builds, ext4 for userdebug/eng
- Partitions: Virtual A/B, dynamic (`odm_dlkm product system system_ext vendor
  vendor_dlkm`), plus `system_dlkm` and Transsion `tr_*` partitions

## Layout

| Directory            | Purpose                                        |
| -------------------- | ---------------------------------------------- |
| `configs/properties` | Props ported from the dump build.props          |
| `configs/vintf`      | Device VINTF manifest (stock, from the dump)    |
| `configs/audio`      | ODM audio effects config                        |
| `configs/keylayout`  | Touch panel keylayout                           |
| `init/`              | fstab + stock init rc sources (from the dump)   |
| `overlay*/`          | RRO overlays (from the XOS14 tree, to refresh)   |
| `sepolicy/`          | SELinux rules (from the XOS14 tree, to refresh)  |
| `tools/`             | Dump -> tree generators (props, proprietary)    |

## Usage

1. Drop this directory at `device/infinix/X6871`.
2. Create `device/infinix/X6871-kernel` from the XOS16 dump (see the README in
   that tree), including the radio firmware images under `firmware/`.
3. Build the vendor tree:

   ```bash
   source build/envsetup.sh
   # run extract-files with the dump mounted at vendor/infinix/X6871/dump
   python3 extract-files.py
   ```

4. Build:

   ```bash
   source build/envsetup.sh
   lunch lineage_X6871-userdebug
   m
   ```

## Status / TODO

- [x] BoardConfig, device.mk, fstab, init rc sources, props, VINTF
- [x] proprietary-files.txt generated from the dump (vendor + odm)
- [ ] Blob fixups need iteration once a full build tree is available
- [ ] Overlays and sepolicy need a pass against Android 16 stock policies
- [ ] Radio firmware images (`firmware/*.img`) must be extracted from OTA
- [ ] system_ext/product Transsion apps are intentionally not shipped yet
