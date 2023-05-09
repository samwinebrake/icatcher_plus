#!/bin/bash
#SBATCH -t 07:00:00
#SBATCH -o /scratch2/weka/quest/shehadak/.slurm_jobs/slurm-%j.out
#SBATCH -e /scratch2/weka/quest/shehadak/.slurm_jobs/slurm-%j.err
#SBATCH -N 1
#SBATCH -c 1
#SBATCH --gres=gpu:1
#SBATCH --constraint=any-gpu
#SBATCH --mem=8G

cd /scratch2/weka/quest/shehadak/gaze-coding/icatcher_plus/reproduce
source ~/.bash_profile
conda activate gaze
echo "Run Started"

# ICP
# python test.py \
#     $1 \
#     models/icatcher+_lookit.pth \
#     --output_video_path output/icp \
#     --output_annotation output/icp \
#     --output_format compressed \
#     --fc_model models/face_classifier_lookit.pth \
#     --fc_model_arch vgg16 \
#     --fd_model opencv_dnn \
#     --gpu_id 0

# Age model
# python test.py \
#     $1 \
#     models/icatcher+_lookit.pth \
#     --output_video_path output/ours_agemodel \
#     --output_annotation output/ours_agemodel \
#     --output_format compressed \
#     --fc_model models/our_fc_model.pt \
#     --fc_model_arch vgg19_bn \
#     --fd_model opencv_dnn \
#     --gpu_id 0

# Retinaface
# python test.py \
#     $1 \
#     models/icatcher+_lookit.pth \
#     --output_video_path output/ours_retinaface \
#     --output_annotation output/ours_retinaface \
#     --output_format compressed \
#     --fc_model models/face_classifier_lookit.pth \
#     --fc_model_arch vgg16 \
#     --fd_model retinaface \
#     --gpu_id 0


# Gaze
# python test.py \
#     $1 \
#     models/regnet_gaze.pth \
#     --output_video_path output/ours_gaze \
#     --output_annotation output/ours_gaze \
#     --output_format compressed \
#     --fc_model models/face_classifier_lookit.pth \
#     --fc_model_arch vgg16 \
#     --fd_model opencv_dnn \
#     --gpu_id 0

# Facerec
# python test.py \
#     $1 \
#     models/icatcher+_lookit.pth \
#     --output_video_path output/ours_facerec \
#     --output_annotation output/ours_facerec \
#     --output_format compressed \
#     --fc_model models/face_classifier_lookit.pth \
#     --fc_model_arch vgg16 \
#     --fd_model opencv_dnn \
#     --use_facerec bbox \
#     --gpu_id 0


# Everything except facerec
# python test.py \
#     $1 \
#     models/regnet_gaze.pth \
#     --output_video_path output/ours_everything_except_facerec \
#     --output_annotation output/ours_everything_except_facerec \
#     --output_format compressed \
#     --fc_model models/our_fc_model.pt \
#     --fc_model_arch vgg19_bn \
#     --fd_model retinaface \
#     --gpu_id 0


conda deactivate
echo "Run Complete"