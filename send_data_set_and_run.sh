set -x
. buildrc

echo "NOW DIR"
pwd

echo "CH DIR to /home/a/dl_image_manager"
cd /home/a/dl_image_manager
pwd
. buildrc

sshpass -p ${GAA_PYTORCH_SERVER_PASS}  ssh -o StrictHostKeyChecking=no ${GAA_PYTORCH_SERVER_USER}@${GAA_PYTORCH_SERVER} hostname
sshpass -p ${GAA_PYTORCH_SERVER_PASS}  scp -o StrictHostKeyChecking=no data_set.tar.gz ${GAA_PYTORCH_SERVER_USER}@${GAA_PYTORCH_SERVER}:/tmp/
sshpass -p ${GAA_PYTORCH_SERVER_PASS}  ssh -o StrictHostKeyChecking=no ${GAA_PYTORCH_SERVER_USER}@${GAA_PYTORCH_SERVER} "cd /home/a/pytorch_ssd/VOCdevkit/BCCD ;  rm -rf Annotations/ ImageSets/ JPEGImages/ ;  tar xvfz /tmp/data_set.tar.gz ; mv data_set/* . ; rm -rf data_set ; cd /home/a/pytorch_ssd ; ./run_learn.sh "


