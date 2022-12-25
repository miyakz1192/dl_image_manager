===================================================
DL用の学習用画像を管理するためのフレームワーク
===================================================

このフレームワークは以下のような構成を持つ環境のための学習用画像管理フレームワーク

1. 学習用のサーバ(以降、便宜上pytorchサーバ)

2. ラベリング用のサーバ(以降、便宜上imglabelingサーバ)

3. data augumentation用のサーバ(以降、dataaugサーバ)


作業のメインはdataaugサーバにて行う。


動機
====

game ad augumentationのAI学習をすすめる上での学習用データ管理の問題点の解決

https://github.com/miyakz1192/game_ad_automation.git 
image_management.rst


問題解決の方策案/分析など
===========================

まず、何を学習するのか。というプロジェクトの概念を導入すると、
例えば、close画像を認識するプロジェクト、漢字を認識するプロジェクトと言ったように、用途別に整理できて良いし、プロジェクトに共通のプログラムなどをまとめやすくなる

プロジェクト
--------------

ROOT-PROJECT NAME
と言った階層にする。

次にソース管理すべきものとそうでないものに分ける。

ソース管理すべきもの
-------------------------

1. マスターのannotationファイル

2. 大元のネタ画像(オリジナルサイズ 32 x 32)と、大元のネタ画像を含む「大元のネタ画像含有ネタ画像ファイル」(400 x 400など)

3. jupyter notebookのプログラム

4. data augumentationとして自動生成に使うプログラム


ソース管理すべきでないもの
------------------------------

上記No4によって自動生成されたすべての画像ファイル

作業手順のまとめ
-------------------

人間がやる作業と本FWによって自動化される部分を明確化しておく。


1. 新規project

   1. 人間がマスターの大元画像を用意する(例：ゲーム画像からgimpを使って部分を抜き出しjpgとして保存)@dataaug

   2. 人間がdata augumentation用のjupyer notebookを作成する。このプロセスはいろいろと試行錯誤しながら実施することになる(その際全体画像サイズや、着目画像のサイズは意識)。sapmple/data_aug_sample.pyを多くの場合は利用できる。これを使って作業すると、実際に生成された画像を確認できる。@dataaug

   3. 人間がdata augumentation自動化用のスクリプトを作成する(No2を元に作成する)。ただし、sapmple/data_aug_sample.pyを利用できる。もし、No2の作業にて、sampleの動作から変更する必要がなければ、そのまま、sample/daug.pyを<project_name>/data_augmentation/に保存する。@dataaug

   ※ daug.pyは第一引数にインプット画像となる＜プロジェクト名＞(プロジェクト名/master/image.jpg)。これが規定。

   4. 人間がNo2,3のソースをコミットする。また、大元のネタ画像もコミットする@dataaug

   5. 人間が、大元のネタ画像(オリジナルサイズ 32 x 32)から、大元のネタ画像を含む「大元のネタ画像含有ネタ画像ファイル」(400 x 400など)を生成する。※bin/extend_image_size.pyを実行する(デフォルトでprojects/<project_name>/master/image_extended.jpgに保存される)。この画像をcommit pushする@dataaug

   6. 人間が、No5のファイルをimglabelingサーバに転送する(この作業はこのレポジトリをimglabelingサーバにてpullすれば良い)。@dataaug

   7. 人間が、No6によって転送されたファイルに対してラベリングするVOCラベリングが汎用的なので、VOCラベルにする。@imglabeling

   8. 人間が、No7のラベルをmasterラベルとしてコミットする(pushする)@imglabeling

   9. 人間が、git pullして最新の情報をDLしたうえで、project buildを実行する@dataaug(dlimgmgrがdataaugサーバでdata augumentation自動化スクリプトを実行する。画像をダウンロードしてくる。画像ファイルに対してannotationをmasterからリネームして生成する。結果はproject/build配下に格納される)


2. 既存projectに対する変更
   dataaugサーバでコードなどを変更してcommit/push。大元イメージファイルも同様

3. projectをミックスさせて全体的な構成を行う@dataaug
   ./bin/build_all.pyを実行する(各projectをbuildするだけ)


   以下、pytorch固有のデータセット
   Annotations  ImageSets  JPEGImages
   それぞれを生成する。projectまたいでtrain/validの割合を一括指定可能とする。tar.gzで固める。pytorchサーバに転送する。
      (メモ：各projectから一定の割合でtrain/validを抜き出す。これは汎用的な機能。割合は指定可能
      　　　その上で、pytorch固有の上記3組を作り出す機能。これはpytorch専用の機能。この２パートに分ける)

  

4. pytorchサーバでprojectミックスさせたものを展開する(人間、@pytorch)

ディレクトリ構成
===================

"https://github.com/miyakz1192/dl_image_manager.git"のそれ。::

  dl_image_manager(root)
    doc
    lib
    bin
    projects
      <project_name>
        README.md
        master
          image.jpg (data)
          image.xml (annotation)
        build
          <x>.jpg
          <x>.xml
        data_augmentation 
          daug.py
          <xxx.py>
        jupyer_notebook
          <~.ipynb>
  

"<>"でくくららた所が可変部分。
ここで、<project_name>には具体的なプロジェクト名が入る。README.mdは任意。
build配下のxは0以上の正の整数。


着目点
======

1-1~1-3ではjupyter notebookやdata augumentation自動化用の共通ライブラリが存在して、他のprojectでも共通化出来そう

No1-5は特にコマンドを作成したほうが楽。

No1-6はコマンドを作成したほうが楽。

各サーバ(dlimgmgr/dataaug/imglabeling)で共通の構成情報を保持するべき
この構成情報はパスワードを含む場合があるので、一番最初に作成して
各サーバに配布しておくのは、初期設定作業として必要か(ただし、一度で良い。サーバ構成に変更がない場合は１度でよい)。

構成情報
-----------

dataaug_usr
dataaug_pass
dataaug_target_home #(  https://github.com/miyakz1192/dl_image_manager.gitがcloneされているdir)

imglabeling_usr
imglabeling_pass
imglabeling_target_home #(同上)

pytorch_usr
pytorch_pass
pytorch_target_home #(projectミックスしたtar.gzを格納するdir)









