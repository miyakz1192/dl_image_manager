#! /bin/bash
set -x
pwd
source buildrc
#. buildrc

echo "NOW DIR"
pwd

echo "CH DIR to /home/a/dl_image_manager"
cd /home/a/dl_image_manager
pwd
. buildrc

sshpass -p ${GAA_RESNET34_SERVER_PASS}  ssh -o StrictHostKeyChecking=no ${GAA_RESNET34_SERVER_USER}@${GAA_RESNET34_SERVER} hostname
sshpass -p ${GAA_RESNET34_SERVER_PASS}  scp -o StrictHostKeyChecking=no data_set.tar.gz ${GAA_RESNET34_SERVER_USER}@${GAA_RESNET34_SERVER}:/tmp/
sshpass -p ${GAA_RESNET34_SERVER_PASS}  ssh -o StrictHostKeyChecking=no ${GAA_RESNET34_SERVER_USER}@${GAA_RESNET34_SERVER} "cd /home/a/resset/dataset/GAA_DATA ;  rm -rf data_set  ;  tar xvfz /tmp/data_set.tar.gz ; cd /home/a/resset ;  ./go.sh "
