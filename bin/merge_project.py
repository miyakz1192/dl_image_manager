#!/usr/bin/env python3

import glob


class ProjectMerger:
    def __init__(self, src_prj=None, dst_prj=None, projects_dir=None):
        self.src_prj = src_prj
        self.dst_prj = dst_prj
        self.projects_dir = projects_dir

    def __count_jpg_files(self, dir_name):
        return len(glob.glob(dir_name + "/*.jpg"))

    def load_config(self, file_name=None):
        #load configuration of src_prj and dst_prj from files
        pass

    def __project_build_dir_name(self,project_name):
        return self.projects_dir + "/" + project_name + "/build"

    def __count_jpg_files_in_project(self, project_name):
        return self.__count_jpg_files(self.__project_build_dir_name(project_name))

    def __prj_file_name_prefix(self, project_name):
        return "%s_" % project_name

    def __transform_and_copy_annotation_file(self, project_name, src_count , dst_count):
        import pdb
        pdb.set_trace()
        src_anno_file_name = self.__prj_file_name_prefix(project_name) + str(src_count) + ".xml"
        dst_anno_file_name = self.__prj_file_name_prefix(self.dst_prj) + str(dst_count) + ".xml"

        data = self.__get_annotation_data_and_rewrite(src_anno_file_name)

        self.__save_xml_data_as(data, dst_anno_file_name)

        print(dst_anno_file_name)

    def __get_annotation_data_and_rewrite(self, file_name):
        pass

    def __save_xml_data_as(self, data, dst_anno_file_name):
        pass

    def __copy_jpg_file(self, project_name, suffix_count):
        pass

    def __merge_one_prj(self, target_prj, next_count):
        target_prj_jpg_file_count = self.__count_jpg_files_in_project(target_prj)


        for i in range(target_prj_jpg_file_count):
            self.__transform_and_copy_annotation_file(target_prj, i, next_count + i)
            self.__copy_jpg_file(target_prj,i)

        return next_count

    def merge(self):
        #FIXME: good path def like build_data_set.py
        self.dst_prj_jpg_file_count = self.__count_jpg_files(self.projects_dir + "/" + self.dst_prj + "/build")

        print("INFO: %s jpg files count=%d" % (self.dst_prj, self.dst_prj_jpg_file_count))

        next_count = self.dst_prj_jpg_file_count
        for target_prj in self.src_prj:
            next_count = self.__merge_one_prj(target_prj, next_count)


if __name__ == "__main__":
    print("main!")
    pm = ProjectMerger(src_prj=["closebcow"], dst_prj="close", projects_dir="./projects")
    pm.merge()
