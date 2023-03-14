#!/usr/bin/env python3

#starndard lib
import subprocess
import argparse
import glob
import os
import shutil
import sys

#my lib
sys.path.append("./lib/")
from get_current_process_user_home_dir import *
from dl_image_manager_constants import *
from build_lib import *
import gaa_lib_loader
import gaa_constants

class AutoProject:
    def __init__(self):
        self.prefix = "autogenclose_"

    def __download_images(self):
        pass

    def __create_additional_merge_target_src_project(self):
        pass

    def __check_already_created_in_projects(self):
        pass

    def __get_next_index(self):
        pass

    def __create_hash_db(self):
        pass

    def __check_hash_db(self):
        pass

    def __get_checksum(self, image_file):
        pass

    def __is_already_added(self, target_image_file):
        s = self.__get_checksum(target_image_file)
        return self.__check_hash_db(s)

    def __make_project(self, index):
        newname = self.prefix + str(index)
        #TODO:do make_project.sh newname

    def __get_image_file_list(self, target_prj, kind):
        pass

    def create_project(self):
        target_prj = "close"

        self.__download_images()
        self.__create_additional_merge_target_src_project()
        self.__check_already_created_in_projects()
        next_idx = self.__get_next_index()

        targets = self.__get_image_file_list(target_prj, "true")

        for t in targets:
            if self.__is_already_added(t) is True:
                continue

            self.__make_project(t, next_idx)

            next_idx += 1

if __name__ == "__main__":
    ap = AutoProject()
    ap.create_project()


