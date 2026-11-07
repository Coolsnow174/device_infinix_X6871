#
# Copyright (C) 2026 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit from X6871 device
$(call inherit-product, device/infinix/X6871/device.mk)
-include vendor/enchanted/keys/keys.mk

# Inherit some common Lineage stuff.
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

BOARD_VENDOR := Infinix
PRODUCT_NAME := lineage_X6871
PRODUCT_DEVICE := X6871
PRODUCT_MANUFACTURER := INFINIX
PRODUCT_BRAND := Infinix
PRODUCT_MODEL := Infinix X6871

PRODUCT_GMS_CLIENTID_BASE := android-transsion
PRODUCT_SYSTEM_NAME := X6871-OP
PRODUCT_SYSTEM_DEVICE := Infinix-X6871

BUILD_FINGERPRINT := Infinix/X6871-OP/Infinix-X6871:16/BP2A.250605.031.A3/301550094:user/release-keys
