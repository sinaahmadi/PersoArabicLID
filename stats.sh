#!/bin/bash
arr_lang_ids=("__label__pa" "__label__mzn" "__label__ps" "__label__hac" "__label__sdh" "__label__skr" "__label__ug" "__label__kas" "__label__ckb" "__label__azb" "__label__ud" "__label__fa" "__label__sd\t" "__label__glk" "__label__kmr" "__label__ar" "__label__trw" "__label__brh" "__label__bal")

if [ "$1" == "clean" ]; then
	wc -l datasets/0/test.txt datasets/0/train.txt
	for i in "${arr_lang_ids[@]}"
	do
		echo "$i"
		grep "$i" datasets/0/test.txt | wc -l
		grep "$i" datasets/0/train.txt | wc -l
	done
fi

# stats noisy 20
if [ "$1" == "noisy" ]; then
	wc -l datasets/$2/test.txt datasets/$2/train.txt
	for i in "${arr_lang_ids[@]}"
	do
		echo "$i"
		grep "$i" datasets/$2/test.txt | wc -l
		grep "$i" datasets/$2/train.txt | wc -l
	done
fi

if [ "$1" == "merged" ]; then
	wc -l datasets/merged/test.txt datasets/merged/train.txt
	for i in "${arr_lang_ids[@]}"
	do
		echo "$i"
		grep "$i" datasets/merged/test.txt | wc -l
		grep "$i" datasets/merged/train.txt | wc -l
	done
fi