# Prospective analysis of external environmental costs of energy provision

This repository contains the code to run the analysis and reproduce all figures of the article

Bantje, D., Sacchi, R., Arendt R., Bauer, C., Luderer, G.: *Prospective analysis of external environmental costs of energy provision*

## Installation

Using [conda](https://anaconda.org/anaconda/conda) and the `environment.yml` file provided, the environment needed to run the code can be set up:

```
conda env create -f environment.yml
```

If you still run into issues running the code, contact the owner of this repo.

## Instructions

The analysis code is contained in Juptyter notebooks, that can be run in suitable editors or locally via a browser.

To fully reproduce all steps of the analysis, run all scripts in `scripts` in the order indicated by the filename prefixes, starting with `01_prepare_brightway.ipynb`.

To only reproduce figures, run `09_make_plots_main.ipynb` for the main article figures, and `10a_make_plots_extended-data.ipynb` for extended data figures.

## Note on data availability

The `data` subfolder contains all data necessary *except* the ecoinvent database. To fully reproduce all (intermediate) results, you need to have an [ecoinvent license](https://ecoinvent.org/licenses/) covering version 3.9.1.

If you have your own ecoinvent license, you might have to adapt the first script `01_prepare_brightway.ipynb`.

However, intermediate results are stored in `output`, so all scripts following `05_perform_lcia.ipynb` can be run also without an ecoinvent license.