#!/usr/bin/env python3

import sys
sys.path.append("./lib/")

import glob
import shutil

from get_current_process_user_home_dir import *
from dl_image_manager_config import *
from dl_image_manager_constants import *
from xml_lib import * 

class ProjectMerger:
    def __init__(self, src_prj=None, dst_prj=None, projects_dir=None):
        self.src_prj = src_prj
        self.dst_prj = dst_prj
        self.projects_dir = projects_dir

    def __count_jpg_files(self, dir_name):
        return len(glob.glob(dir_name + "/*.jpg"))

    def __prj_build_dir_name(self,project_name):
        return self.projects_dir + "/" + project_name + "/build"

    def __count_jpg_files_in_project(self, project_name):
        return self.__count_jpg_files(self.__prj_build_dir_name(project_name))

    def __prj_file_name_prefix(self, project_name):
        return "%s_" % project_name

    def __prj_jpg_file_path(self, project_name, count):
        return self.__prj_build_dir_name(project_name) + "/" + self.__prj_file_name_prefix(project_name) + str(count) + ".jpg"

    def __prj_annotation_file_path(self, project_name, count):
        return self.__prj_build_dir_name(project_name) + "/" + self.__prj_file_name_prefix(project_name) + str(count) + ".xml"

    def __transform_and_copy_annotation_file(self, project_name, src_count , dst_count):
        src_anno_path = self.__prj_annotation_file_path(project_name, src_count)
        dst_anno_path = self.__prj_annotation_file_path(self.dst_prj, dst_count)

        xmlo = XMLOperator()
        xmlo.read(src_anno_path)
        #filename tag
        xmlo.rewrite("filename", os.path.basename(self.__prj_jpg_file_path(self.dst_prj, dst_count)))
        #object, name tag
        xmlo.rewrite("name", self.dst_prj)
        xmlo.write(dst_anno_path)

        print("INFO: copy %s to %s" % (src_anno_path, dst_anno_path))

    def __copy_jpg_file(self, project_name, src_count, dst_count):
        src_jpg_path = self.__prj_jpg_file_path(project_name, src_count)
        dst_jpg_path = self.__prj_jpg_file_path(self.dst_prj, dst_count)

        shutil.copyfile(src_jpg_path, dst_jpg_path)
        print("INFO: copy %s to %s" % (src_jpg_path, dst_jpg_path))

    def __merge_one_prj(self, target_prj, next_count):
        target_prj_jpg_file_count = self.__count_jpg_files_in_project(target_prj)
        print("INFO: source project of %s jpg files count=%d" % (target_prj, target_prj_jpg_file_count))

        for i in range(target_prj_jpg_file_count):
            self.__transform_and_copy_annotation_file(target_prj, i, next_count + i)
            self.__copy_jpg_file(target_prj,i, next_count + i)

        return next_count + target_prj_jpg_file_count

    def merge(self):
        self.dst_prj_jpg_file_count = self.__count_jpg_files(self.projects_dir + "/" + self.dst_prj + "/build")

        print("INFO: destination project of %s jpg files count=%d" % (self.dst_prj, self.dst_prj_jpg_file_count))

        next_count = self.dst_prj_jpg_file_count
        for target_prj in self.src_prj:
            next_count = self.__merge_one_prj(target_prj, next_count)

if __name__ == "__main__":
    if "DL_IMAGE_MANAGER_MERGE_CONFIG" in globals():
        print("INFO: start merge")
        src_prj = DL_IMAGE_MANAGER_MERGE_CONFIG[0]
        dst_prj = DL_IMAGE_MANAGER_MERGE_CONFIG[1]
        projects_dir = DL_IMAGE_MANAGER_MERGE_CONFIG[2]
        pm = ProjectMerger(src_prj=src_prj, dst_prj=dst_prj, projects_dir=projects_dir)
        pm.merge()
        print("INFO: end merge")
    else:
        print("INFO: no DL_IMAGE_MANAGER_MERGE_CONFIG quit this program")
