import glob
import os
import random

def make_train_valid_data(project_build_dir, train_percent):
    files = glob.glob(project_build_dir + "/*.jpg")
    data_set = list(map(lambda x: os.path.basename(x),files))

    choose = int(len(data_set) * (train_percent / 100.0))
    train_set = []
    valid_set = []

    for i in range(0, choose):
        idx = random.randrange(len(data_set))

        d = data_set[idx]
        train_set.append(d)
        del data_set[idx]

    valid_set = data_set
    return (train_set, valid_set)

def change_file_ext(file_name, new_ext):
    dir_name = os.path.dirname(file_name)
    basename = os.path.basename(file_name)
    
    file_name = os.path.splitext(basename)[0]
    ext_name  = os.path.splitext(basename)[1]

    if not dir_name:
        output_file_name = file_name + new_ext
    else:
        output_file_name = dir_name + "/" + file_name + new_ext

    return output_file_name
