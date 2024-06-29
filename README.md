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

## Online experiment
Upon interest from the reviewers, we provide extended context for our online experiment conducted on a large international fashion discovery platform in May 2024. 
We describe the context to the extent permitted by the organization's non-disclosure policy.

**Task**: Personalize the rank of a selection (thousands) of fashion products, i.e., a subset of product category, *optionally* filtered by the user.
- If a user explicitly *dislikes* an item, we would like to hide it, as well as items related to it.

**Layout**: Scrollable grid (tens-hundreds of rows, ~5 products in row). Naturally, first several rows receive higher exposure.

**Training data**: Weighted implicit feedback. Training user-item matrix has $O(10^6)$ users, $O(10^6)$ items, and contains $O(10^7)$ interactions over the historical period used in training. The resulting data-Gram matrix has $O(10^9)$ nonzeros (=density ~0.1%).

**Models**: Baseline = proprietary implementation of [SANSA](https://dl.acm.org/doi/10.1145/3604915.3608827), a sparse variant of [EASE](https://arxiv.org/abs/1905.03375). New variant = absolute value of the baseline model. Retrained *daily*.

**Evaluation**: 7 day A/B test in 50-50 split. Over this period, each variant received roughly 0.5M sessions. We report observed 3% lift in CTR (Mann-Whitney p=2e7). Additionally, our experiment focused on conversion-related, monetary metrics (we cannot disclose numbers, but they were in favor of the proposed modifications).

To visually demonstrate the different behavior of the two variants, we provide additional examples similar to Fig. 3 in the `visual-examples` folder.
