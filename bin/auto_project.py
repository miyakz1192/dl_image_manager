#!/usr/bin/env python3

#starndard lib
import subprocess
import argparse
import glob
import os
import shutil
import sys
import re
import hashlib
from collections import defaultdict

#my lib
sys.path.append("./lib/")
from get_current_process_user_home_dir import *
from dl_image_manager_constants import *
from build_lib import *
import gaa_lib_loader
import gaa_constants
from easy_sshscp import *
from number_suffix import *


class AutoProject:

    AUTO_GEN_TARGET_PROJECT_NAME = "close"
    AUTO_GEN_PREFIX = "autogenclose_"
    AUTO_GEN_PREFIX_REGEX = r'.*/autogenclose_*'

    def __init__(self):
        self.home_dir = get_current_process_user_home_dir()

        self.prefix = self.AUTO_GEN_PREFIX
        self.prefix_r = self.AUTO_GEN_PREFIX_REGEX
        self.additional_merge_target_src_prj = []
        self.additional_merge_target_src_prj_file_path = self.home_dir + DL_IMAGE_MANAGER_CONFIG_DIR + DL_IMAGE_MANAGER_ADDITIONAL_MERGE_TARGET_SRC_PRJ_FILE_NAME
        self.hash_db = defaultdict(lambda: None) #default val is None

    def __download_images(self):
        ssh = EasySSHSCP()
        host = "scrcpy"
        cmd = "tar cvfz /tmp/images.tar.gz -C %s %s" % (gaa_constants.GAA_HOME_DIR , gaa_constants.GAA_AUTO_GEN_DIR)
        ssh.ssh(host, cmd)
        ssh.download(host, "/tmp/images.tar.gz", "./images.tar.gz")
        subprocess.run(["tar", "xvfz", "./images.tar.gz"])

    def __save_additional_merge_target_src_prj_file(self):
        #give shot name
        additional_merge_target_src_prj = []
        path = self.home_dir + DL_IMAGE_MANAGER_PROJECTS_STORE_COMMON
        for f in glob.glob(path + "/*"):
            if re.match(self.prefix_r, f) is not None:
                f = os.path.basename(f)
                additional_merge_target_src_prj.append(f)

        fname = self.additional_merge_target_src_prj_file_path
        with open(fname, mode="w") as f:
            f.write("\n".join(additional_merge_target_src_prj))

    def __check_already_created_in_projects(self):
        dirname = self.home_dir + DL_IMAGE_MANAGER_PROJECTS
        targets = glob.glob(dirname + "/*")

        for i in targets:
            if re.match(self.prefix_r, i) is not None:
                print("ERROR: already created in projects %s" % i)
                raise ValueError()

    def __get_next_index_in_projects_store_common(self):
        path = self.home_dir + DL_IMAGE_MANAGER_PROJECTS_STORE_COMMON
        nsf = NumberSuffixFile(directory_path=path)
        return nsf.next()

    def __create_hash_db(self):
        print("INFO: create hash db")
        path = self.home_dir + DL_IMAGE_MANAGER_PROJECTS_STORE_COMMON_MASTER_IMAGE_SEARCH_PATTERN
        for fn in glob.glob(path):
            h = self.__get_checksum(fn)
            print("  file=%s, sha256=%s" % (fn, h))
            self.hash_db[h] = fn
        
    def __get_checksum(self, image_file):
        with open(image_file, "rb") as f: #open as a binary mode
            data = f.read()
            return hashlib.sha256(data).hexdigest() # h as str

    def __image_file_was_already_added(self, target_image_file):
        h = self.__get_checksum(target_image_file)
        if self.hash_db[h] is not None:
            print("INFO: target_image_file=%s is already added" % target_image_file)
            return True
        print("INFO: target_image_file=%s is new" % target_image_file)
        return False

    def __make_project(self, new_prj_name, master_image_file):
        print("INFO: making new project %s master=%s" % (new_prj_name, master_image_file))
        subprocess.run(["./bin/make_project.sh", new_prj_name])
        to = self.home_dir + DL_IMAGE_MANAGER_PROJECTS_MASTER_IMAGE % new_prj_name
        shutil.copyfile(master_image_file, to)
        subprocess.run(["./bin/gen_anno_xml.py", new_prj_name])

    def __get_image_file_list_in_image_dir(self, target_prj, kind):
        return glob.glob("./images/auto_gen/" + target_prj + "/" + kind + "/*")

    def __create_project_each_targets(self):
        #get max index autogenclose_* in ./projects_store/common/
        #max index + 1 is next index
        next_idx = self.__get_next_index_in_projects_store_common()

        #get target image file list in ./image/<target_prj>/true/
        #in this case ./images/auto_gen/close/true
        target_prj = self.AUTO_GEN_TARGET_PROJECT_NAME
        targets = self.__get_image_file_list_in_image_dir(target_prj, "true")
        #for each ./images/auto_gen/close/true/*
        for t in targets:
            #check t's hash is already in hash_db
            if self.__image_file_was_already_added(t) is True:
                continue

            new_prj_name = self.prefix + str(next_idx)
            self.__make_project(new_prj_name, t)
            self.additional_merge_target_src_prj.append(new_prj_name)
            next_idx += 1

    def __move_projects_store_common(self):
        for prj_name in self.additional_merge_target_src_prj:
            src = self.home_dir + DL_IMAGE_MANAGER_PROJECT % prj_name
            dst = self.home_dir + DL_IMAGE_MANAGER_PROJECTS_STORE_COMMON
            print("INFO: move %s to %s" % (src, dst))
            shutil.move(src, dst)

    def create_project(self):

        #download image.tar.gz(autogenclose) from GAA at scrcpy server
        self.__download_images()
        #check autogenclose_* in ./projects/ if exists ERROR&quit.
        self.__check_already_created_in_projects()

        #create hash DB key=sha256 of projects_store/common/*/master/image.jpg, value=file name of that
        self.__create_hash_db()

        try:
            self.__create_project_each_targets()
        except:
            print("INFO: some error exists but contine")
            import traceback
            traceback.print_exc()

        self.__move_projects_store_common()
        self.__save_additional_merge_target_src_prj_file()

if __name__ == "__main__":
    AutoProject().create_project()
