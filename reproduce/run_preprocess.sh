#!/bin/bash
#SBATCH -t 24:00:00
#SBATCH -o /scratch2/weka/quest/shehadak/.slurm_jobs/slurm-%j.out
#SBATCH -e /scratch2/weka/quest/shehadak/.slurm_jobs/slurm-%j.err
#SBATCH -N 1
#SBATCH -c 2
#SBATCH --gres=gpu:1
#SBATCH --constraint=any-gpu
#SBATCH --partition=quest
#SBATCH --mem=8G
​
cd /home/shehadak/weka/gaze-coding/icatcher_plus/reproduce
source ~/.bash_profile
conda activate gaze
echo "Run Started"

python3 preprocess.py \
    /home/shehadak/weka/gaze-coding/my_icatcher_plus/datasets/lookit_test_raw/ \
    /home/shehadak/weka/gaze-coding/my_icatcher_plus/datasets/lookit_test_processed_ours/ \
    --raw_dataset_type lookit \
    --fc_model models/our_fc_model.pt \
    --split_type all \
    --one_video_per_child_policy include_all \
    --gpu_id 0
​
​
conda deactivate
echo "Run Complete"

