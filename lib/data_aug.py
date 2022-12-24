import keras.utils.image_utils as image
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import array_to_img


class DataAugmentationGenerator:
    #if this is not in GUI environment show_image set to False
    def __init__(self, image_file_path, base_img_size=(400,400), base_img_color=255, save_dir = "./", show_image=True):
        self.reest_count()
        self.base_img_size = base_img_size
        self.base_img_color = base_img_color
        self.save_dir = save_dir 
        self.show_image = show_image

        #アップロードされた画像を読み込み
        self.image = image.load_img(image_file_path) #表示用のイメージデータ
        self.np_image = np.array(self.image)         #numpy配列化したもの
        self.target_image = self.np_image[np.newaxis, :, :, :] #data augmentation化する対象                      

    def imshow(self, data):
        if self.show_image == True:
            plt.imshow(data)


    def show_image(self):
        #表示画像のサイズを設定
        #plt.figure(figsize = (32, 32))
        #軸を表示しない
        plt.xticks(color = "None")
        plt.yticks(color = "None")
        plt.tick_params(bottom = False, left = False)
        #表示
        self.imshow(self.np_image)

    def reest_count(self):
        self.count = 0

    def rotation(self):
        #-180度〜+180度の間でランダムに回転するImageDataGeneratorを作成
        #rotation_datagen = ImageDataGenerator(rotation_range = 180)
        rotation_datagen = ImageDataGenerator(rotation_range = 5)
        #画像を表示
        self.show_and_save(rotation_datagen, self.target_image)

    def height(self):
        # 指定されたピクセル（-50〜+50）の範囲で上下にランダムに動かします。
        #height_datagen = ImageDataGenerator(height_shift_range = 10)
        #引数が10だと若干動かし過ぎ感がある
        #以下は、補完時に何も指定していない
        #height_datagen = ImageDataGenerator(height_shift_range = 5)
        height_datagen = ImageDataGenerator(height_shift_range = 5,fill_mode="constant", cval=125)
        self.show_and_save(height_datagen, self.target_image)

    def zoom(self):
        #0.5〜1.5の間でランダムに拡大又は縮小するImageDataGeneratorを作成
        zoom_datagen = ImageDataGenerator(zoom_range = [0.7, 1.3],fill_mode="constant", cval=125)
        self.show_and_save(zoom_datagen, self.target_image)

    def brightness(self):
        #画像の明るさを0.3〜0.8の間で調整（暗くする）
        brightness_datagen = ImageDataGenerator(brightness_range = [0.1, 0.5])
        self.show_and_save(brightness_datagen, self.target_image)

    def mix(self):
        datagen = ImageDataGenerator(rotation_range = 0.5,width_shift_range = 0.1,height_shift_range = 0.1,zoom_range = [0.7, 1.3],fill_mode="constant", cval=125)
        self.show_and_save(datagen, self.target_image)

    def mix6(self):
        for i in range(6):
            self.mix()

    def suite(self):
        self.height()
        self.zoom()
        self.brightness()
        self.mix6()

    def show_and_save(self, datagen_func, img, count_max=98):
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
          self.imshow(show_img)
        
          #データのセーブ処理
          #まずはベースとなる400x400画像を作る。背景は白(255,255,255)
          base = np.full(self.base_img_size + (3,), 255) #第一引数はサイズ(x,y)とともにチャネル数が必要。(x,y,c)となる。
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
