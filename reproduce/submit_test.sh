#!/bin/bash
#SBATCH -t 05:00:00
#SBATCH -o /scratch2/weka/quest/shehadak/.slurm_jobs/slurm-%j.out
#SBATCH -e /scratch2/weka/quest/shehadak/.slurm_jobs/slurm-%j.err
#SBATCH -N 1
#SBATCH -c 1
#SBATCH --gres=gpu:1
#SBATCH --constraint=any-gpu
#SBATCH --partition=quest
#SBATCH --mem=8G

cd /scratch2/weka/quest/shehadak/gaze-coding/icatcher_plus/
source ~/.bash_profile
conda activate gaze
echo "Run Started"

python test.py \
    /home/shehadak/weka/gaze-coding/icatcher_plus/reproduce/videos/test_vid_1000.mp4 \
    models/icatcher+_lookit.pth --fc_model models/our_fc_model.pt \
    --output_video_path test_output/ \
    --fc_model_arch vgg19_bn \
    --gpu_id 0

conda deactivate
echo "Run Complete"