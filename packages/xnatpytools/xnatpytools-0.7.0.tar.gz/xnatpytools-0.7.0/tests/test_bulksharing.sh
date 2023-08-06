#!/usr/bin/env bash
export PYTHONPATH=${HOME}/dev/xnatpytools:${PYTHONPATH}

cd ../xnatpytools/bulksharing

#python bulksharing.py --test_run=1 --log_dir="." "https://xnat.acc.dh.unimaas.nl" $(cat $HOME/xnatuser.txt) $(cat $HOME/xnatpassword_acc.txt) "DMS" "DMS_test_funct" "1022791_DICOM_HEAD,1022815_DICOM_HEAD"

python bulksharing.py --test_run=0 --log_dir=$HOME/data "https://xnat.prod.dh.unimaas.nl" $(cat $HOME/xnatuser.txt) $(cat $HOME/xnatpassword_prod.txt) "DMS" "DMS_424_Blokla" $HOME/data/surfdrive/projects/20210526_100_ids_blokland_dti/Gabriella_Blokland_100IDs_MRIbrain_PHQ9lowhigh_20210526.txt
