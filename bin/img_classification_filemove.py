#!/usr/bin/env python3

import os
import argparse
import shutil
import uuid

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("input_list", help="(partial) output of bin/img_classifier.py(one record lile <file, True> or <file,False>")
    parser.add_argument("output_dir", help="output_dir")

    args = parser.parse_args()

    with open(args.input_list) as f:
        records = list(map(lambda x: x.strip(), f.readlines()))

    print("INFO: checking whether files in list exist")
    img_files = []
    flags = []
    for r in records:
        img_file, flag = r.split(",")
        img_file = img_file.strip()
        flag = flag.strip()
        img_files.append(img_file)
        flags.append(flag)
        if os.path.exists(img_file) is False:
            print("ERROR: %s is not found " % (img_file))
            raise ValueError("a file in specified list not found")

    print("INFO: check done. start move")

    for i in range(len(img_files)):
        if flags[i] == "True":
            temp = str(uuid.uuid4())
            shutil.move(img_files[i], args.output_dir+"/"+temp+".jpg")
            print("INFO: %s => %s" % (img_files[i], args.output_dir+"/"+temp+".jpg"))
