###########################################################
# DL Image Manager Settings
###########################################################
#ResNet34
DL_IMAGE_MANAGER_FORCING_GLOBAL_BASE_IMAGE_SIZE = (-1,-1)
#SSD
#DL_IMAGE_MANAGER_FORCING_GLOBAL_BASE_IMAGE_SIZE = (400,400)

#ResNet34
DL_IMAGE_MANAGER_MERGE_CONFIG_INIT_SRC= ["closebcow", "closegb", "closewcobfat", "closewcolg"]
DL_IMAGE_MANAGER_MERGE_CONFIG=(DL_IMAGE_MANAGER_MERGE_CONFIG_INIT_SRC, "close", "./projects")

#Edge Mode
DL_IMAGE_MANAGER_EDGE_MODE = False
