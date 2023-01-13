###########################################################
# DL Image Manager Settings
###########################################################
#ResNet34
#DL_IMAGE_MANAGER_FORCING_GLOBAL_BASE_IMAGE_SIZE = (64,64)
#SSD
DL_IMAGE_MANAGER_FORCING_GLOBAL_BASE_IMAGE_SIZE = (400,400)


###########################################################
# DO NOT REMOVE BELOW
###########################################################
def dl_image_manager_forcing_global_base_image_size():
    return DL_IMAGE_MANAGER_FORCING_GLOBAL_BASE_IMAGE_SIZE
