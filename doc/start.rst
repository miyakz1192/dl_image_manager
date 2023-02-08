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

前提条件のようなもの
----------------------

利用する画像フォーマット、拡張子はjpgである。

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
      (image_extended.jpgは単にimglabelingサーバでアノテーション作業をやりやすくするように用意されたファイルである。その後の画像処理には使われない)

   7. 人間が、No6によって転送されたファイルに対してラベリングするVOCラベリングが汎用的なので、VOCラベルにする。@imglabeling

   8. 人間が、No7のラベルをmasterラベルとしてコミットする(pushする)ファイル名はmaster/image_extended.xml@imglabeling

   9. 人間が、git pullして最新の情報をDLしたうえで、project buildを実行する@dataaug(dlimgmgrがdataaugサーバでdata augumentation自動化スクリプトを実行する。画像をダウンロードしてくる。画像ファイルに対してannotationをmasterからリネームして生成する。結果はproject/build配下に格納される)


2. 既存projectに対する変更
   dataaugサーバでコードなどを変更してcommit/push。大元イメージファイルも同様

3. projectをミックスさせて全体的な構成を行う@dataaug 
   ./bin/build_all.pyを実行する(各projectをbuildするだけ)

   以下、pytorch固有のデータセットを実行するため、./bin/build_data_set.pyを実行する
   Annotations  ImageSets  JPEGImages
   それぞれを生成する。projectまたいでtrain/validの割合を一括指定可能とする。tar.gzで固める。pytorchサーバに転送する。
      (メモ：各projectから一定の割合でtrain/validを抜き出す。これは汎用的な機能。割合は指定可能
      　　　その上で、pytorch固有の上記3組を作り出す機能。これはpytorch専用の機能。この２パートに分ける)
   
4. pytorchサーバでprojectミックスさせたものを展開する(人間、@pytorch)

設定
------

利用する学習フレームワークによっては、base_image_sizeを変更する必要がある。
学習フレームワーク応じて以下を編集して、clear_project,
build_all.pyおよびbuild_data_setを実行する。::

  a@dataaug:~/dl_image_manager$ cat lib/dl_image_manager_settings.py 
  ###########################################################
  # DL Image Manager Settings
  ###########################################################
  #ResNet34
  #DL_IMAGE_MANAGER_FORCING_GLOBAL_BASE_IMAGE_SIZE = (64,64)
  #SSD
  DL_IMAGE_MANAGER_FORCING_GLOBAL_BASE_IMAGE_SIZE = (400,400)


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

特殊なproject(ja_char)
============================

今の所、上記のフレームワークから微妙に外れるprojectとしてja_charがある。
これは、大量コーパスからそのコーパスで使われている日本語文字（かな漢字）を画像生成して、
それをマスターにして、一旦はdata augumentationせずに(あまりに大量になりすぎるため）、学習に使用するというもの。
フレームワーク通常時と比較して以下の差分がある。

1. masterにjpgが無い。xmlは存在する(かなりイレギュラーな点か)
2. daug.pyの実体処理はsample/daug.pyを使わずに、コーパスから画像を生成してbuild配下に大量jpgを配置。
   実質的なdata augumentationは実行しない(noopのdata augumentationを実行したという解釈はできる)


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

ワークフロー構築のためのメモ
=================================

以下からの引用
https://github.com/miyakz1192/game_ad_automation/commit/6501be44dd9c0bce26ff72607f366df98ba16b4c

以下。::

|物体検出や画像認識の改善のために学習データの追加と学習、検証、実機でのテストプレーという一連のワークフローを効率的に回す仕組みが無いとやってられん。
|SSDとResNet34で学習データと、テスト結果、重みの組を管理する仕組みが必要。
|まずはそこだろうか。あとは、このワークフローが完成してNo2の改善がイマイチとなると、一回、深層学習の基本に戻って調査し直すしかあるまい。

ということで、このworkflowを作ってみることにする。

考慮が必要な点は

1. 学習データの追加が簡単にできること

2. 結果が管理しやすいこと(SSD/ResNetのソースと、学習データ、重みをセットで管理)

3. タスクの状況が見えること

4. 結果のGAAへのデプロイ、アンデプロイが簡単に行えること 


まずは、データの管理方法について検討が必要なのではないか


学習データ(学習タスクアウトプット)の管理単位
-----------------------------------------------

まず、学習データの大元としてはdl_image_managerで管理している各projectが最小単位として考えられる。
各学習データをbuildした結果がdata_setと言える。

つまりdata_set ∋  project群となる。data_set.tar.gzは80MB位。あと、data_set.tar.gzを生成したプログラム(つまりdl_image_manager)もバックアップしたほうが良いので、こちらもバックアップしたい。こちらのサイズは1.8GBくらい(大きい！）

あと、各data_set.tar.gzを元にSSDとResNetで学習を行う。こちらも結果のweightとソースはともにバックアップしておきたい。

この単位を学習タスクアウトプットと一応呼んでおく。

学習タスクアウトプットの生成
-----------------------------------------------

dl_image_managerサーバを基点に以下を実施する

1. 人間が、新規projectなどを作ったり、既存projectに変更を加えたりする

2. 人間がcreate_task.shを実行する

3. create_task.shでは一連の以下が実行される

3-1. ./learn_batch.sh ssdを実行して、projectを再buildして、data_set.tar.gzを生成する。また、ssdで学習を実行する

3-2. dl_image_managerのソースをバックアップする(この際、容量節約のためdata_setディレクトリ配下を削除する。また、data_set.tar.gzはこのバックアップに含まれる)

3-3. ssdサーバ(pytorch)の/home/a/pytorch_ssdをまるごとバックアップして、dl_image_managerにダウンロードする(ssd.tar.gz)

3-4. ./learn_batch.sh resnet34を実行して、projectを再buildして、data_set.tar.gzを生成する。また、resnet34で学習を実行する

3-5. dl_image_managerのソースをバックアップする(この際、容量節約のためdata_setディレクトリ配下を削除する。また、data_set.tar.gzはこのバックアップに含まれる)

3-6. resnet34サーバ(pytorch)の/home/a/ressetをまるごとバックアップして、dl_image_managerにダウンロードする(resnet34.tar.gz)

3.7. 上記アーカイブ群をtarで固めてgaa_learning_task配下のoutputディレクトリに配置しておく



※　注意
---------

lib/dl_image_manager_config.pyをssd/resnet34で入れ替える必要がある。どのような処理が良いかは考える必要がある。
DL_IMAGE_MANAGER_FORCING_GLOBAL_BASE_IMAGE_SIZEをSSD/ResNet34に応じて追記するか、ファイル自体をまるごと置き換えるか。前者のほうがdl_image_manager_config.pyの変更に強そうな気がしなくもないが？？
　→　とりあえず対応。

buildrcが設定されていないとエラーをはくようにすると親切だが、、、、

SSDとResNet34の各タスクで一緒に学習結果をゲーム画像でテストした結果も学習タスクアウトプットに含まれると良い。
　→  ResNet34の方はやった。SSDはテストプログラムが無いので、実施していない。

学習タスクアウトプットの表示と削除
-----------------------------------------------

上記tarがoutputディレクトリにあるのでそれを見れば良い。
outputディレクトリ配下に学習タスクアウトプットの名前がついたディレクトリが更にあって、
そこに簡単なメモを記したtextが入っているといい感じかも

学習タスクアウトプットのデプロイ
---------------------------------

gaa_learning_taskのoutput配下のディレクトリを1つ選択してdepoy.shを実行する
dl_image_managerのbuildrcを読み込み、ssd/resnet34のサーバ(pytorch)に以下を実行する

1. SSDの場合、ssd.tar.gzからタイムスタンプが最新のweightを抜き出して、それをpytorch_ssdサーバの/home/a/pytorch_ssdに配置する(weight/latest_weight.pth)

2. ResNet34の場合も同様に実施する(resset34.tar.gz)

※　注意
------------

GAA経由で動作する場合はlatest_weight.pthを参照して動作する必要がある。
学習タスクアウトプットにssd.tar.gzまたはresnet34.tar.gzが無い場合は、SSD/ResNet34のどちらかのdeployを無視する
(どちらもない場合はどちらのdepoyも無視＝つまりなにもdeployされない)


考えられるシナリオ
----------------------

1. projectを１つ追加する。これは典型的なシナリオでcreate_task.sh/depoy.shが動作しそう

2. SSD/ResNet34のプログラムを改変する。同上。

3. SSDとResNet34で対象とするprojectを変えたい。例えば、SSDではja_charを必要とするし、ResNet34ではやっぱり必要としない(このようなことが今後発生するか不明だけど・・・）、この場合は、create_task.shで実行したいタスクを選択出来るようにしたら良い。(SSDはこっちのprojectsでResNet34はこっちのprojects)など。なので、create_task.shで種別-どのprojectsディレクトリの関連を設定するファイルが必要。それを見て動作。また、dl_image_manager配下にはデフォルトでprojectsディレクトリがあり、こちらがすべてのタスクで使用される仕様のため、例えば、SSD_projectsというディレクトリがあり、こちらがSSD専用のprojectsにしたければ、そちらを指定した設定ファイルを作っておく必要がある。など。

番外編
========

メモ:paramiko関連でハマる
----------------------------------

paramikoをインストールした。::

  a@dataaug:~/gaa_lib/net$ pip install paramiko
  Collecting paramiko
    Downloading paramiko-3.0.0-py3-none-any.whl (210 kB)
       |████████████████████████████████| 210 kB 15.5 MB/s 
  Collecting cryptography>=3.3
    Downloading cryptography-39.0.0-cp36-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (4.2 MB)
       |████████████████████████████████| 4.2 MB 77.7 MB/s 
  Collecting bcrypt>=3.2
    Downloading bcrypt-4.0.1-cp36-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (593 kB)
       |████████████████████████████████| 593 kB 88.1 MB/s 
  Collecting pynacl>=1.5
    Downloading PyNaCl-1.5.0-cp36-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_24_x86_64.whl (856 kB)
       |████████████████████████████████| 856 kB 115.0 MB/s 
  Requirement already satisfied: cffi>=1.12 in /home/a/.local/lib/python3.8/site-packages (from cryptography>=3.3->paramiko) (1.15.1)
  Requirement already satisfied: pycparser in /home/a/.local/lib/python3.8/site-packages (from cffi>=1.12->cryptography>=3.3->paramiko) (2.21)
  Installing collected packages: cryptography, bcrypt, pynacl, paramiko
  Successfully installed bcrypt-4.0.1 cryptography-39.0.0 paramiko-3.0.0 pynacl-1.5.0
  a@dataaug:~/gaa_lib/net$ 
  
あとで、pip叩いたら、::

  module 'lib' has no attribute 'X509_V_FLAG_CB_ISSUER_CHECK'

こまった。::

　　https://askubuntu.com/questions/1428181/module-lib-has-no-attribute-x509-v-flag-cb-issuer-check/1433089#1433089

以下実施した。解決した。::

  sudo apt remove python3-pip 
  wget https://bootstrap.pypa.io/get-pip.py
  sudo python3 get-pip.py
  




