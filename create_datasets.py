import json
import random
import re
import pyarabic.araby as araby
from klpt.preprocess import Preprocess

# iso639-3 to iso639-2
map_6393_to_6392 = {
	"arb": "ar",
	"urd": "ud",
	"fas": "fa",
	"snd": "sd",
	"ckb": "ckb",
	"sdh": "sdh",
	"mzn": "mzn",
	"kmr": "ku",
	"glk": "glk",
	"kas": "kas",
	"hac": "hac",
	"azb": "azb",
	"pnb": "pa",
	"pus": "ps",
	"trw": "trw",
	"bal": "bal",
	"skr": "skr",
	"uig": "ug",
	"brh": "brh"
}

def clean_corpus(text):
	# clean corpus by removing acronyms (x.x or x.x.x)
    clean_text = re.sub(r".\..\..\..", "", text)
    clean_text = re.sub(r".\..\..", "", clean_text)
    # remove dates
    clean_text = clean_text.replace(" / ", "/").replace(" . ", ".").replace("...", ".")
    clean_text = re.sub(r"([1-9]|0[1-9]|[12][0-9]|3[01])[- /.]([1-9]|0[1-9]|1[012])[- /.]\d\d\d\d", "", clean_text)
    # remove links
    clean_text = re.sub(r'https?:\/\/.*[\r\n]*', '', clean_text, flags=re.MULTILINE)
    return clean_text

def tsv_to_dict(text):
    # convert the script map to a dctionary
    text_dict = dict()
    for i in text:
        i_s = i.split("\t")[0] # source letter
        if i_s not in text_dict:
            text_dict[i_s] = list()
        for j in range(1, len(i.split("\t"))):
            if i.split("\t")[j] != "":
                i_t = i.split("\t")[j] # target letter
                if i_t == "NULL":
                    i_t = ""

                if i_t not in text_dict[i_s]:
                    text_dict[i_s].append(i_t)
    return text_dict

def generate(text, character_map, noise_percentage=100):
    keys = list(character_map.keys())
    random.Random(10).shuffle(keys)
    character_map = {key: character_map[key] for key in keys}

    # Determine the number of characters that should be turned noisy, i.e. mapped with noisy equivalents, to meet the synthesis level
    text_set = set(text)
    num_replacements = round(len(text_set) * noise_percentage / 100)
    added_noise = 0
    for i in text_set:
        if not added_noise <= num_replacements:
            break
            
        if i in character_map:
            # note: this can be modified in such a way that the length of the letters be taken into account: first longer replacements, then shorter ones.
            text = text.replace(i, random.choice(character_map[i]))
            added_noise += 1
        
    if added_noise == 0 or len(text) < 5:
        return None
    
    # if noise% is 100, remove all diacritics and zwnj regardless of the random choice
    if noise_percentage == 100:
        return araby.strip_diacritics(text.replace("▁", ""))
            
    return text.replace("▁", "")

def clean_text(text, has_zwnj=False, has_diacritics=False):
    if not has_zwnj:
        text = text.replace("‌", "")
    if not has_diacritics:
        for i in [ "ً", "ِ", "ٌ", "ُ", "ّ", "ٍ", "ْ", "ء"]:
            text = text.replace(i, "")
    return text.replace("‏", " ").replace("‎", " ").replace("ـ", "")

def upsample(liste, coefficient=4, maximum=10000):
	new_liste = liste * coefficient
	if len(new_liste) > maximum:
		return new_liste[:maximum]
	return new_liste

if __name__ == '__main__':

	# -------------------- Create synthetic data
	dataset_size = 20000
	preprocessor_ckb = Preprocess("Sorani", "Arabic", numeral="Latin")

	clean_train, clean_test = list(), list()
	noisy_train, noisy_test = {20: list(), 40: list(), 60: list(), 80: list(), 100: list()}, {20: list(), 40: list(), 60: list(), 80: list(), 100: list()}
	only_clean_langs = dict()
	visited_langs = list()

	with open("configs.json", "r") as f:
		configs = json.load(f)

	with open("scripts/info.json", "r") as f:
		info = json.load(f)
	
	for config in configs:
		if config["source_language"] not in visited_langs:
			visited_langs.append(config["source_language"])
		else:
			continue

		clean_dataset = list()
		noisy_dataset = {20: list(), 40: list(), 60: list(), 80: list(), 100: list()}
		print("%s-%s"%(config["source_language"], config["target_language"]))
		counter = 0

		if config["script_map"] != "":
			# convert script map to a dictionary
			with open(config["script_map"], "r") as f:
				script_map = tsv_to_dict(f.read().splitlines()[1:])

			with open(config["corpus"], "r") as f:
				corpus = f.read()
			
			corpus = list(set(clean_corpus(corpus).splitlines()))
			random.Random(10).shuffle(corpus)
			
			for i in corpus:
				if counter >= dataset_size:
					break

				row = "__label__" + map_6393_to_6392[config["source_language_code"]] + "\t" + i.strip()

				# clean data
				clean_row = clean_text(row, has_zwnj=info[config["source_language"]]["zwnj"], has_diacritics=info[config["source_language"]]["diacritics"])
				if config["source_language"] == "Sorani" or config["source_language"] == "Kurmanji":
					clean_row = preprocessor_ckb.preprocess(clean_row)

				clean_dataset.append(clean_row)
				counter += 1
				# noisy data
				for n in noisy_dataset:
					synth_row = generate(row, script_map, n)
					if synth_row != None:
						noisy_dataset[n].append(synth_row)

		else: # Arabic, Persian, Urdu and Uyghur
			with open(config["corpus"], "r") as f:
				corpus = f.read()

			corpus = list(set(clean_corpus(corpus).splitlines()))
			random.Random(10).shuffle(corpus)
			if config["source_language"] not in only_clean_langs:
				only_clean_langs[config["source_language"]] = list()
			for i in corpus:
				row = "__label__" + map_6393_to_6392[config["source_language_code"]] + "\t" + i.strip()
				only_clean_langs[config["source_language"]].append(row)

		# ---------------------------------------------------------- prepare clean train/test datasets
		if config["script_map"] != "":
			all_clean = clean_dataset
		else:
			all_clean = only_clean_langs[config["source_language"]][:dataset_size]
		
		random.Random(10).shuffle(all_clean)
		if config["source_language"] in ["Brahui", "Torwali", "Balochi"]:
			clean_test += all_clean[0:500]
			clean_train += upsample(all_clean[500:], maximum=2000)
		else:
			clean_test += all_clean[0:2000]
			if len(all_clean[2000:]) < 8000:
				print("Upsampling....")
				clean_train += upsample(all_clean[2000:], maximum=8000)
			else:
				clean_train += all_clean[2000:10000]
		# ---------------------------------------------------------- prepare noisy train/test datasets
		for n in noisy_dataset:
			random.Random(10).shuffle(list(set(noisy_dataset[n])))
			if config["source_language"] in ["Brahui", "Torwali", "Balochi"]:
				noisy_test[n] += noisy_dataset[n][0:500]
				noisy_train[n] += upsample(noisy_dataset[n][500:], maximum=2000)
			else:
				noisy_test[n] += noisy_dataset[n][0:2000]
				if len(noisy_dataset[n][2000:]) < 8000:
					noisy_train[n] += upsample(noisy_dataset[n][2000:], maximum=8000)
				else:
					noisy_train[n] += noisy_dataset[n][2000:10000]

	# ---------------------------------------------------------- Save datasets	
	random.Random(10).shuffle(clean_test)
	random.Random(10).shuffle(clean_train)

	# save clean
	with open("datasets/0/test.txt", "w") as f:
		f.write("\n".join(clean_test))
	with open("datasets/0/train.txt", "w") as f:
		f.write("\n".join(clean_train))

	# save noisy
	for n in noisy_dataset:
		# Test
		with open("datasets/%s/test.txt"%str(n), "w") as f:
			random.Random(10).shuffle(noisy_test[n])
			f.write("\n".join(noisy_test[n]))

		# Train
		with open("datasets/%s/train.txt"%str(n), "w") as f:
			random.Random(10).shuffle(noisy_train[n])
			f.write("\n".join(noisy_train[n]))

	# save all noise levels
	test_checked_langs, train_checked_langs = dict(), dict()
	merged_test, merged_train = list(), list()

	noisy_test_all = "\n".join(["\n".join(noisy_test[i]) for i in noisy_test])
	noisy_train_all = "\n".join(["\n".join(noisy_train[i]) for i in noisy_train])
	noisy_test_all = list(set(noisy_test_all.splitlines()))
	noisy_train_all = list(set(noisy_train_all.splitlines()))

	random.Random(10).shuffle(noisy_test_all)
	random.Random(10).shuffle(noisy_train_all)

	for i in noisy_test_all:
		if i.split("\t")[0] not in test_checked_langs:
			test_checked_langs[i.split("\t")[0]] = 1
		else:
			test_checked_langs[i.split("\t")[0]] += 1

		if test_checked_langs[i.split("\t")[0]] <= 2000:
			merged_test.append(i)

	for i in noisy_train_all:
		if i.split("\t")[0] not in train_checked_langs:
			train_checked_langs[i.split("\t")[0]] = 1
		else:
			train_checked_langs[i.split("\t")[0]] += 1

		if train_checked_langs[i.split("\t")[0]] <= 8000:
			merged_train.append(i)


	with open("datasets/all/test.txt", "w") as f:
		f.write("\n".join(merged_test))
	with open("datasets/all/train.txt", "w") as f:
		f.write("\n".join(merged_train))





