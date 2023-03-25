#!/bin/bash

# two configuration config_1 or config_2
# config_name=config_1
config_name=config_2

# $1 clean
echo "Training the model..." $1 $2 $config_name
if [ "$config_name" == "config_1" ]; then
	./fastText-0.9.2/fasttext  supervised -input $1/$2/train.txt -output models/$config_name/LID_model_$2 -dim 16 -minn 2 -maxn 4 -loss hs
else
	./fastText-0.9.2/fasttext  supervised -input $1/$2/train.txt -output models/$config_name/LID_model_$2 -dim 64 -minn 2 -maxn 6 -loss hs  -epoch 25  -lr 1.0
fi

echo "Compressing..."
./fastText-0.9.2/fasttext quantize -input $1/$2/train.txt -output models/$config_name/LID_model_$2 -qnorm -cutoff 50000 -retrain

echo "Testing the model..."
./fastText-0.9.2/fasttext test models/$config_name/LID_model_$2.bin $1/$2/test.txt
./fastText-0.9.2/fasttext test models/$config_name/LID_model_$2.bin $1/$2/test.txt 2
./fastText-0.9.2/fasttext test models/$config_name/LID_model_$2.bin $1/$2/test.txt 3
./fastText-0.9.2/fasttext test models/$config_name/LID_model_$2.bin $1/$2/test.txt 4

echo "Testing with lid.176..."
./fastText-0.9.2/fasttext test fastText-0.9.2/lid.176.bin $1/$2/test.txt
./fastText-0.9.2/fasttext test fastText-0.9.2/lid.176.bin $1/$2/test.txt 2
./fastText-0.9.2/fasttext test fastText-0.9.2/lid.176.bin $1/$2/test.txt 3
./fastText-0.9.2/fasttext test fastText-0.9.2/lid.176.bin $1/$2/test.txt 4

./fastText-0.9.2/fasttext predict models/$config_name/LID_model_$2.bin $1/$2/test.txt 4 > models/$config_name/predict_$2.txt
echo "Prediction done."