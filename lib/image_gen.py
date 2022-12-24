import keras.utils.image_utils as image
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import array_to_img


class DataAugmentationGenerator:
    def __init__(self, base_img_size=(400,400), base_img_color=255, save_dir = "./"):
        reest_count()
        self.base_img_size = base_img_size
        self.base_img_color = base_img_color
        self.save_dir = save_dir 
        pass

    def reest_count(self):
        self.count = 0

    def show_and_save(self, datagen_func, img, count_max):
        print("===show_and_save count=%d" % (self.count))
        #表示サイズを設定
        plt.figure(figsize = (10, 5))
        
        #画像をbatch_sizeの数ずつdataに入れる
        #本稿は画像が一枚のため同じ画像がdataに入り続けることになる
        for i, data in enumerate(datagen_func.flow(img, batch_size = 1, seed = 0)):
          #表示のためnumpy配列からimgに変換する
          show_img = array_to_img(data[0], scale = False)
          #2×3の画像表示の枠を設定＋枠の指定
          #plt.subplot(2, 3, i+1)
          plt.subplot(33, 3, i+1)
          #軸を表示しない
          plt.xticks(color = "None")
          plt.yticks(color = "None")
          plt.tick_params(bottom = False, left = False)
          #画像を表示
          plt.imshow(show_img)
        
          #データのセーブ処理
          #まずはベースとなる400x400画像を作る。背景は白(255,255,255)
          base = np.full(self.base_img_size + (3), 255) #第一引数はサイズ(x,y)とともにチャネル数が必要。(x,y,c)となる。
          #targetのサイズをbaseに埋め込む
          tx = data[0].shape[0]
          ty = data[0].shape[1]
          base[0:tx,0:ty] = data[0][0:tx,0:ty]
          save_img = array_to_img(base, scale = False)
          image.save_img(self.save_dir + "/" + str(self.count) + ".jpg", save_img)
          self.count += 1
        
          #6回目で繰り返しを強制的に終了
          if i >= count_max:
            return
