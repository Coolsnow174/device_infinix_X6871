#
# Enforce generic ramdisk allow list
$(call inherit-product, $(SRC_TARGET_DIR)/product/generic_ramdisk.mk)

# Project ID Quota
$(call inherit-product, $(SRC_TARGET_DIR)/product/emulated_storage.mk)

# Dalvik VM Configuration
$(call inherit-product, frameworks/native/build/phone-xhdpi-6144-dalvik-heap.mk)

# A/B
$(call inherit-product, $(SRC_TARGET_DIR)/product/virtual_ab_ota/launch_with_vendor_ramdisk.mk)

PRODUCT_PACKAGES += \
    update_engine \
    update_engine_sideload \
    update_verifier

AB_OTA_POSTINSTALL_CONFIG += \
    RUN_POSTINSTALL_system=true \
    POSTINSTALL_PATH_system=system/bin/otapreopt_script \
    FILESYSTEM_TYPE_system=$(BOARD_SYSTEMIMAGE_FILE_SYSTEM_TYPE) \
    POSTINSTALL_OPTIONAL_system=true

AB_OTA_POSTINSTALL_CONFIG += \
    RUN_POSTINSTALL_vendor=true \
    POSTINSTALL_PATH_vendor=bin/checkpoint_gc \
    FILESYSTEM_TYPE_vendor=$(BOARD_VENDORIMAGE_FILE_SYSTEM_TYPE) \
    POSTINSTALL_OPTIONAL_vendor=true

PRODUCT_PACKAGES += \
    checkpoint_gc \
    otapreopt_script

PRODUCT_PACKAGES += \
    create_pl_dev \
    create_pl_dev.recovery

# Characteristics
PRODUCT_CHARACTERISTICS := nosdcard

# Dynamic Partitions
PRODUCT_USE_DYNAMIC_PARTITIONS := true
PRODUCT_BUILD_SUPER_PARTITION := false

# FastbootD
$(call soong_config_set_bool,fastbootd,bypass_lock_state,true)

PRODUCT_PACKAGES += \
    fastbootd

# Overlays
PRODUCT_PACKAGES += \
    FrameworksResOverlayX6871 \
    SettingsOverlayX6871 \
    SettingsProviderOverlayX6871 \
    SystemUIOverlayX6871 \
    WifiResOverlayX6871

PRODUCT_PACKAGES += \
    LineageApertureOverlayX6871 \
    LineageDialerOverlayX6871 \
    LineageSDKOverlayX6871 \
    LineageSettingsOverlayX6871

# Shipping API level
PRODUCT_SHIPPING_API_LEVEL := 31

# Soong namespaces
PRODUCT_SOONG_NAMESPACES += \
    $(LOCAL_PATH) \
    hardware/google/interfaces \
    hardware/google/pixel \
    hardware/lineage/interfaces/power-libperfmgr \
    hardware/mediatek \
    hardware/mediatek/libmtkperf_client \
    hardware/mediatek/wlan/wifi_hal \
    hardware/transsion

# Inherit the proprietary files
$(call inherit-product, vendor/infinix/X6871/X6871-vendor.mk)

PRODUCT_PACKAGES += \
    fstab.mt6895.vendor_ramdisk \
    x6871_vendor_modules_link \
    x6871_odm_modules_link \
    x6871_sensor_firmware_link \
    x6871_mdota_link
