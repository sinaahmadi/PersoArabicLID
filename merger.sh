#!/bin/bash

# merge the clean and noisyd datasets
cat datasets/0/train.txt datasets/all/train.txt > datasets/merged/train.txt
cat datasets/0/test.txt datasets/all/test.txt > datasets/merged/test.txt

# add more data from the clean dataset for data balance
cat corpora/Persian_fas.txt | shuf | head -n8000 | ts "__label__fa	" | shuf >> datasets/merged/train.txt
cat corpora/Arabic_arb.txt | shuf | head -n8000 | ts "__label__ar	" | shuf >> datasets/merged/train.txt
cat corpora/Urdu_urd.txt | shuf | head -n8000 | ts "__label__ud	" | shuf >> datasets/merged/train.txt
cat corpora/Uyghur_ug-wiki-20230120.txt | shuf | head -n8000 | ts "__label__ug	" | shuf >> datasets/merged/train.txt

cat corpora/Persian_fas.txt | shuf | tail -n2000 | ts "__label__fa	" | shuf >> datasets/merged/test.txt
cat corpora/Arabic_arb.txt | shuf | tail -n2000 | ts "__label__ar	" | shuf >> datasets/merged/test.txt
cat corpora/Urdu_urd.txt | shuf | tail -n2000 | ts "__label__ud	" | shuf >> datasets/merged/test.txt
cat corpora/Uyghur_ug-wiki-20230120.txt | shuf | tail -n2000 | ts "__label__ug	" | shuf >> datasets/merged/test.txt 