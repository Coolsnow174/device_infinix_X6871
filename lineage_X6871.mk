# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit from X6871 device
$(call inherit-product, device/infinix/X6871/device.mk)

# Inherit some common Lineage stuff.
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

PRODUCT_DEVICE := X6871
PRODUCT_NAME := lineage_X6871
PRODUCT_BRAND := Infinix
PRODUCT_MODEL := Infinix X6871
PRODUCT_MANUFACTURER := Infinix

PRODUCT_GMS_CLIENTID_BASE := android-transsion

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="sys_mssi_64_64only_cn_armv82-user 16 BP2A.250605.031.A3 189099 release-keys" \
    BuildFingerprint=Infinix/X6871-OP/Infinix-X6871:16/BP2A.250605.031.A3/301550049:user/release-keys
