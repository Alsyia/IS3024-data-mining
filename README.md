# IS3024-data-mining
Data mining third year project: trying to predict drugs' prices using governmental dataset

You can find a copy of the dataset in `Data` diectory.

Main file is `drug_form.py`. This file loads datasets using columns names stored in `schema.py`, clean them using methods of `clean_tools.py`, might display plots from `plots.py` and eventually train a model and evaluate it.

Our final report is in `rapport.pdf`. You can also see the decision tree we trained in `tree.pdf`.

Usage:

```
pip install -r requirements.txt
python3.7 drug_form.py
```
