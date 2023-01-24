#!/usr/bin/env python3

import cv2
import os
import argparse
import shutil

class ManualImageClassifier:
    def __init__(self, input_dir=["./"], output_dir="./"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.in_files = []
        self.move_target_flags = []

        if os.path.isdir(self.output_dir) is not True:
            raise ValueError("output_dir = %s is not found" % (self.output_dir))

        for i in input_dir:
            for root, dirs, files in os.walk(top=i):
                self.in_files += list(map(lambda x: os.path.join(root,x), files))

    def run_marking_move_target(self):
        cur = 0
        self.move_target_flags = [False for x in range(len(self.in_files))]

        while True:
            if cur == len(self.in_files):
                print("END")
                break

            print("SHOWING: %s, move target=%s" % (self.in_files[cur], self.move_target_flags[cur]))
            img = cv2.imread(self.in_files[cur])
            cv2.imshow("image" , img)
            print("input vim style key(h=left,j=down,k=up,l=right)")
            k = cv2.waitKey(0)
            k = chr(k)

            if k == "j":
                print("next")
                cur += 1
            elif k == "k":
                print("prev")
                cur -= 1
                if cur < 0:
                    cur = 0
            elif k == "l":
                print("!SET!: set this as move target to %s" % (self.output_dir))
                self.move_target_flags[cur] = True
                cur += 1
            elif k == "h":
                print("CANCEL MOVE TARGET THIS")
                self.move_target_flags[cur] = False
                cur += 1
            elif k == "q":
                print("QUIT")
                cv2.destroyWindow('image')
                break

            cv2.destroyWindow('image')

    def print_target(self):
        for i in range(len(self.in_files)):
            print("%s, %s" % (self.in_files[i], self.move_target_flags[i]))

    def move_target(self):
        for i in range(len(self.in_files)):
            if self.move_target_flags[i] is True:
                shutil.move(self.in_files[i], self.output_dir+"/")
                print("INFO: %s => %s" % (self.in_files[i], self.output_dir+"/"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("input_dir", help="input_dir")
    parser.add_argument("output_dir", help="output_dir")
    
    args = parser.parse_args()

    m = ManualImageClassifier([args.input_dir], args.output_dir)
    m.run_marking_move_target()
    m.print_target()

    print("CONFIRM: move this ?[y]")
    i = input()
    if i != "y":
        print("QUIT")

    m.move_target()

