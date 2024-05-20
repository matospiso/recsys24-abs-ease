# RecSys '24: On Interpretability of Linear Autoencoders

This repository contains code used in experiments for the paper "On Interpretability of Linear Autoencoders" submitted to RecSys '24.

## Reproducing the experiments
### Environment setup
Python version: `3.10.14`. To install the required packages, run:
```bash
pip install -r requirements.txt
```

### Datasets
We used two datasets in our experiments:
1. [MovieLens 25M](https://grouplens.org/datasets/movielens/25m/)
2. [BeerAdvocate](https://www.kaggle.com/datasets/thedevastator/1-5-million-beer-reviews-from-beer-advocate)

To recreate the preprocessed datasets, place the raw dataset files (`ratings.csv` for MovieLens, `beer_reviews.csv` for BeerAdvocate) in `./data/` directory and re-run the notebooks:
- `preprocessingMovieLens.ipynb` for the MovieLens dataset.
- `preprocessingBeerAdvocate.ipynb` for the BeerAdvocate dataset.
Preprocessed datasets (`ratings_processed_DatasetName.csv`) will be saved in the `./data/` directory.

Alternatively, you can download the preprocessed datasets from our [OSF repository](https://osf.io/bjmuv/?view_only=9439f132405b48b2962abd5d0ded0567) and place them in the `./data/` directory.

### Experiments
There are two experiment notebooks:
1. `experimentMovieLens.ipynb` - experiment on the MovieLens dataset.
2. `experimentBeerAdvocate.ipynb` - experiment on the BeerAdvocate dataset.

To reproduce the results, simply re-run the notebooks. The notebook runs hyperparameter tuning and the main experiment. The results are saved in the `./results/` directory.

### Results
The results of the experiments are saved in the `./results/` directory.
- `hyperparametersDatasetName.txt` contains the results of hyperparameter tuning.
- `resultsDatasetName.txt` contains the results of experiments on the dataset.
- `summary_table.txt` contains the summary of the results as presented in the paper (Table 1).
- `results.ipynb` plots the extended results (recall of liked items, recall of disliked items, and ndcg) for different values of `k`.
