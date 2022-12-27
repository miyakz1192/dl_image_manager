#!/usr/bin/env python3
import sys
sys.path.append("./lib/")

from get_current_process_user_home_dir import *
from dl_image_manager_constants import *

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("project_name", type=str)
args = parser.parse_args()

home_dir = get_current_process_user_home_dir()

project_name = args.project_name

save_file_path = home_dir + DL_IMAGE_MANAGER_PROJECTS_BUILD %(project_name) 
aux_file_path = home_dir + DL_IMAGE_MANAGER_PROJECT %(project_name) + "aux_data/"

#日本語のコーパスを持ってきて、文字を全部一度に読み込み。重複を削除した文字一覧を作成する。（漢字やカタカナなどを含む)

#コードは以下をそのまま流用させていただきました。大変ありがとうございます。
#https://qiita.com/y_itoh/items/fa04c1e2f3df2e807d61

import re
import zipfile
import urllib.request
import os.path
import glob
import numpy as np
from matplotlib import pyplot as plt
import japanize_matplotlib
import keras.utils.image_utils as image
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import array_to_img

URL = 'https://www.aozora.gr.jp/cards/000081/files/43737_ruby_19028.zip'

def load(dir):
    path = os.path.join(dir,'*.txt') #➆
    list = glob.glob(path) #➇
    return list[0] #➈


def download(URL):
    zip_file = re.split(r'/', URL)[-1] #➀
    dir = os.path.splitext(zip_file)[0]

    #すでにＤＬ済みの場合、読み込んで終了。
    if os.path.exists(aux_file_path + "/" + dir):
        print("[TRACE] already downloaded")
        return load(aux_file_path + "/" + dir)

    urllib.request.urlretrieve(URL, aux_file_path + "/" + zip_file) #➁
    dir = os.path.splitext(zip_file)[0] #➂

    with zipfile.ZipFile(aux_file_path + "/" + zip_file) as zip_object: #➃
        zip_object.extractall(aux_file_path + "/" + dir) #➄

    os.remove(aux_file_path + "/" + zip_file) #➅

    return load(aux_file_path + "/" + dir)


def convert(download_text):
    data = open(download_text, 'rb').read() #➀
    text = data.decode('shift_jis') #➁

    # 本文抽出
    text = re.split(r'\-{5,}', text)[2] #➂  
    text = re.split(r'底本：', text)[0] #➃
    text = re.split(r'［＃改ページ］', text)[0] #➄

    # ノイズ削除
    text = re.sub(r'《.+?》', '', text) #➅
    text = re.sub(r'［＃.+?］', '', text) #➆
    text = re.sub(r'｜', '', text) #➇
    text = re.sub(r'\r\n', '', text) #➈
    text = re.sub(r'\u3000', '', text) #➉   

    return text

download_file = download(URL)
print("[DEBUG] download_file = %s" % (download_file) )
#[DEBUG] download_file = 43737_ruby_19028/gingatetsudono_yoru.txt
text = convert(download_file)

#print(text)
print(len(text))


# テキストの1文字１文字をjpgファイルとして保存する
dupremoved_text = list(set(list(text)))
print(len(dupremoved_text))

n = 0
#dupremoved_text = dupremoved_text[:10] #デバッグ用
for i in dupremoved_text:
    #ベースとなる400 x 400イメージを作成する（背景は白）
    base = np.full((400, 400,3), 255)

    fig, ax = plt.subplots(figsize=(0.64, 0.64))
    ax.axis("off")
    #ax.text(0, 0.2, "こ", size=32)
    ax.text(0, 0.2, i, size=32)
    file_name = save_file_path + "/ja_char_%d.jpg" % (n)
    #テンポラリ
    plt.savefig(file_name)

    ja_c = image.load_img(file_name)
    ja_c = np.array(ja_c)
    #print(ja_c.shape)
    #(64, 64, 3)
    #矩形はりつけ
    base[0:64,0:64] = ja_c[0:64,0:64]
    save_img = array_to_img(base, scale = False)
    image.save_img(file_name, save_img)
    n += 1
