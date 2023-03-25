# Language Identification for Perso-Arabic scripts

<p align="center" width="100%">
    <img width="33%" src="https://raw.githubusercontent.com/sinaahmadi/PersoArabicLID/master/PersoArabicGraphemes.png"> 
</p>

The [Perso-Arabic scripts](https://en.wikipedia.org/wiki/Persian_alphabet) are a family of scripts that are widely adopted and used by various linguistic communities around the globe. Identifying various languages using such scripts is crucial to language technologies and challenging in low-resource setups. As such, this paper sheds light on the challenges of detecting languages using Perso-Arabic scripts, especially in bilingual communities where “unconventional” writing is practiced. To address this, we use a set of supervised techniques to classify sentences into their languages. Building on these, we also propose a hierarchical model that targets clusters of languages that are more often confused by the classifiers. 

This repository provides datasets and models for language identification with a focus on languages that use a Perso-Arabic script. The selected 19 languages are the followings:

* Brahui (`brh`)
* Torwali (`trw`)
* Balochi (`bal`)
* Kashmiri (`kas`)
* Gorani (Hawrami, `hac`)
* Northern Kurdish (Kurmanji, `kmr-arab`)
* Central Kurdish (Sorani, `ckb`)
* Southern Kurdish (`sdh`)
* Arabic (`arb`)
* Persian (`fas`)
* Gilaki (`glk`)
* Urdu (`urd`)
* Sindhi (`snd-arab`)
* Azeri (`azb-arab`)
* Uyghur (`uig`)
* Pashto (`pas`)
* Saraiki (`skr`)
* Mazanderani (`mzn`)
* Punjabi (`pnb`)

## Datasets
The [dataset] folder is structured as follows:

1. **Clean**: A dataset of clean data (0% of noise) is provided in [datasets/0](datasets/0). This includes all the selected languages along with Urdu, Persian, Arabic and Uyghur. The dataset contains 10,000 instances per language.
1. **Noisy**: Based on the script mappings in [scripts](scripts), a certain level of noise is injected in the clean text from the corpora of the source language. This is carried out in [create_datasets.py](create_datasets.py). The following datasets containing 10,000 instances per language are provided based on the indicated level of noise from 20% to 100% as:
	* [datasets/20](datasets/20) (20% noise)
	* [datasets/40](datasets/40) (40% noise)
	* [datasets/60](datasets/60) (60% noise)
	* [datasets/80](datasets/80) (80% noise)
	* [datasets/100](datasets/100) (100% noise)
	* [datasets/all](datasets/all): all the previous noisy datasets are merged.
1. **Merged**: Folder [datasets/merged](datasets/merged) contains instances from the clean and noisy datasets (the two previous ones). To avoid imbalance of clean languages for which there is no noise, i.e. Urdu, Persian, Arabic and Uyghur, 10,000 more instances are added from their clean corpora. Therefore, there should be 20000 instances per language.

It should be noted that we upsample data for some of the languages for which there are < 10,000 sentences in our corpora. This is summarized as follows (# refers to the number of sentences):

| Language | # clean corpus | Upsample (# clean train set) | # Clean test set |
|----------|----------------|------------------------------|------------------|
| Brahui   | 549            | Yes (200)                    | 500              |
| Torwali  | 1371           | Yes (2000)                   | 500              |
| Balochi  | 1649           | Yes (2000)                   | 500              |
| Kashmiri | 6340           | Yes (8000)                   | 2000             |
| Gorani   | 8742           | Yes (8000)                   | 2000             |
| others   | > 10,000       | No                           | 2000             |

## Models
The [models] folder provides compressed models that are trained on the train sets. These models are trained on all the selected models.

You can load the trained [models](models) using [fasttext](https://fasttext.cc) in Python or on command-line. For more information, pease consult [https://fasttext.cc/docs/en/python-module.html](https://fasttext.cc/docs/en/python-module.html).

Here is an example in Python:

```python
>>> import fasttext
>>> model = fasttext.load_model("LID_model_merged.ftz")
>>> model.predict("لەزۆربەی یارییەکان گوڵ تۆمار دەکات")
(('__label__ckb',), array([0.96654707]))

```

**We recommend [the merged model  (LID_model_merged.ftz)](LID_model_merged.ftz).**

## Utilities
* [stats.sh](stats.sh) counts number of instances per languages in the various datasets. It can be used with `clean`, `merged` or `noisy` as arguments. The latter should also take the noise level as an additional argument as in `stats.sh noisy 20` or `stats.sh noisy all`.
* [merger.sh](merger.sh) creates the merged datasets which performs equally well in noisy and clean setups.

## Cite this project
Please consider citing [this paper](https://sinaahmadi.github.io/docs/articles/ahmadi2023pali), if you use any part of the data or the models ([`bib` file](https://sinaahmadi.github.io/bibliography/ahmadi2023pali.txt)):

```
	@inproceedings{ahmadi2023pali,
	    title = "{PALI}: A Language Identification Benchmark for {Perso-Arabic} Scripts",
	    author = "Ahmadi, Sina and Agarwal, Milind and Anastasopoulos, Antonios",
	    booktitle = "Proceedings of the 10th Workshop on NLP for Similar Languages, Varieties and Dialects (VarDial)",
	    month = may,
	    year = "2023",
	    address = "Dubrovnik, Croatia",
	    publisher = "The 17th Conference of the European Chapter of the Association for Computational Linguistics"
	}
```

## License 
[MIT](LICENSE)

