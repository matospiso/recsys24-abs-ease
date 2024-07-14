# RecSys '24: On Interpretability of Linear Autoencoders

This repository contains code used in experiments and supplementary material for the paper "On Interpretability of Linear Autoencoders" submitted to RecSys '24.

## Offline experiments
### Environment setup
Python version: `3.10.14`. To install the required packages, run:
```bash
pip install -r requirements.txt
```

### Datasets
In our experiments, we used sparsified variants of two well-known datasets:
1. [MovieLens 25M](https://grouplens.org/datasets/movielens/25m/)
2. [BeerAdvocate](https://www.kaggle.com/datasets/thedevastator/1-5-million-beer-reviews-from-beer-advocate)

**Splitting methodology**: we use *strong generalization* in our experiments, i.e. the entire user/session interaction history is assigned to either training, validation or testing split. In particular, we select all users/sessions with 3+ positive and 3+ negative interactions for validation and testing (split in 1:3 ratio). For more details, see individual preprocessing notebooks.

**Preprocessing notes**: We further sparsify interactions in the training split to increase sparsity of item co-occurrence. This is motivated by one of the goals of our experiments: showing that by using absolute value of weights, we are able to recover related even without observing item co-occurrence (we expect larger improvement for higher top-$k$); when co-occurrences are frequent, we expect the models to perform similarly because direct co-occurrences dominate the computed item-item scores. Moreover, for training, we use only *positive* interactions (see Section 3.2 of the paper).

To recreate the preprocessed datasets, place the raw dataset files (`ratings.csv` for MovieLens, `beer_reviews.csv` for BeerAdvocate) in `./data/movielens/` resp. `./data/beeradvocate/` directory and re-run the notebooks:
- `preprocessingMovieLens.ipynb` for the MovieLens dataset.
- `preprocessingBeerAdvocate.ipynb` for the BeerAdvocate dataset.

Preprocessed datasets (`ratings_processed_DatasetName.csv`) will be saved in the `./data/movielens/` resp. `./data/beeradvocate/` directory. Note that preprocessing also marks dataset rows according to which split they belong to.

Alternatively, you can download the preprocessed datasets from our [OSF repository](https://osf.io/bjmuv/?view_only=9439f132405b48b2962abd5d0ded0567) and place them in the `./data/movielens/` resp. `./data/beeradvocate/` directory.

### Experiments
There are two experiment notebooks:
1. `experimentMovieLens.ipynb` - experiment on the MovieLens dataset.
2. `experimentBeerAdvocate.ipynb` - experiment on the BeerAdvocate dataset.

To reproduce the results, simply re-run the notebooks. The notebooks run hyperparameter tuning and the main experiment. The experiment is organized as a 2x2 grid, where both EASE and abs(EASE) are evaluated w.r.t. positive input interactions and positive+negative input interactions. 

The results are saved in the `./results/movielens/` resp. `./results/beeradvocate/` directory.

### Evaluation metrics
For each experiment, `resultsDatasetName.txt` contains the output of three evaluation metrics: `nDCG`, `recall_liked`, and `recall_disliked` for top-$k$ thresholds $k \in \{10, 20, 50, 100, 200, 500\}$.
- `nDCG` denotes normalized discounted cumulative gain (higher values = better)
- `recall_liked` denotes the recall of liked items (higher values = better)
- `recall_disliked` denotes the recall of disliked items (lower values = better)

See `evaluation.py` for implementation details.

The results contain mean values across all users, while the values after `+/-` denote standard errors of the corresponding metric.

### Results
The results of the experiments are saved in the `./results/beeradvocate/` resp. `./results/movielens/` directory.
- `hyperparametersDatasetName.txt` contains the results of hyperparameter tuning.
- `resultsDatasetName.txt` contains the results of experiments on the dataset.

In `./results/` you will also find
- `summary_table.txt` containing the summary of the results as presented in the paper (Table 1).
- `results.ipynb` with plots of the extended results (recall of liked items, recall of disliked items, and nDCG) for different values of $k$.

## Additional offline experiments
We conducted follow-up experiments based on reviewers feedback.
### 1. Without sparsification
We ran the same experiments on MovieLens 25M and BeerAdvocate *without applying the sparsity-inducing preprocessing steps*, namely
- for MovieLens, we did not split user interactions into 24 hour sessions
- for both datasets, we removed the additional sparsification of training split

In this setting, the density of data-Gram matrix is 1.2% for BeerAdvocate and 2.3% for MovieLens. 
- An average item is, therefore, directly connected (in the sense of co-occurrence) with hundreds of other items. Since short paths are dominant contributors to the resulting item-item scores (see Section 3.2. of the paper), most of the top-$k$ recommendations for $k$ up to hundreds directly result from existing co-occurrence information. 
- For this reason, both variants are roughly equal in terms of recommendation accuracy. The variant with absolute value generally performs very slightly worse, which can be explained by the amplification of numerical errors (without absolute value, random error can cancel out).

#### Reproducing the results
To recreate the preprocessed datasets, place the raw dataset files (`ratings.csv` for MovieLens, `beer_reviews.csv` for BeerAdvocate) in `./data/movielens/` resp. `./data/beeradvocate/` directory and re-run the notebooks:
- `preprocessingMovieLens_dense.ipynb` for the MovieLens dataset.
- `preprocessingBeerAdvocate_dense.ipynb` for the BeerAdvocate dataset.

Preprocessed datasets (`ratings_processed_DatasetName_dense.csv`) will be saved in the `./data/movielens/` resp. `./data/beeradvocate/` directory.

Alternatively, you can download the preprocessed datasets from our [OSF repository](https://osf.io/bjmuv/?view_only=9439f132405b48b2962abd5d0ded0567) and place them in the `./data/movielens/` resp. `./data/beeradvocate/` directory.

##### There are two experiment notebooks:
1. `experimentMovieLens_dense.ipynb` - experiment on the MovieLens dataset.
2. `experimentBeerAdvocate_dense.ipynb` - experiment on the BeerAdvocate dataset.

To reproduce the results, simply re-run the notebooks. The notebook runs hyperparameter tuning and the main experiment. 

The results are saved in the `./results/movielens_dense/` resp. `./results/beeradvocate_dense/` directory.

### 2. Additional sparse dataset
We ran the same experiments on [Yelp2018](https://github.com/kuandeng/LightGCN/tree/master/Data/yelp2018) dataset. 
- We joined the available `train` and `test` splits (these splits use *weak generalization*), and ran the same splitting procedure as in the rest of our experiments (i.e., *strong generalization*). 
- We did not apply sparsification steps (i.e., same way as we've done it for experiments without sparsification).
- Moreover, since there are no negative interactions and individual users have tens-hundreds of interactions, we selected users with more than 30 interactions for validation and testing.

#### Dataset statistics
- 31668 users (of which 4113 are used for validation and 12338 are for testing),
- 38048 items
- 1561406 interactions (325096 for training, 305129 for validation and 931181 for testing).
- (training) data-Gram matrix has density 0.4% -- i.e., an average item co-occurs with ~100 other items, and hence we expect to see improvement at $k=100$ and above due to the ability of abs(EASE) to utilize longer chains of co-occurence edges.

See `preprocessingYelp.ipynb` for dataset statistics.

#### Evaluation
We use the same experiment pipeline as in the rest of our experiments, but since the dataset contains only *positive* interactions
- evaluation of `recall_neg` metric returns `nan` values
- evaluating only on positive inputs (`pos_inputs`) is the same as evaluating on positive and negative inputs (`pos_neg_inputs`) -- the input sets are identical

The raw outputs of experiment pipelines were, therefore, simplified to remove duplicate results (see `resultsYelp_processed.txt`)

#### Reproducing the results
To recreate the preprocessed datasets, place the raw dataset files (`train.txt` and `test.txt` obtained [here](https://github.com/kuandeng/LightGCN/tree/master/Data/yelp2018)) in `./data/yelp2018/` directory and re-run the `preprocessingYelp.ipynb` notebook.

Preprocessed dataset (`ratings_processed_Yelp.csv`) will be saved in the `./data/yelp2018/` directory.

Alternatively, you can download the preprocessed datasets from our [OSF repository](https://osf.io/bjmuv/?view_only=9439f132405b48b2962abd5d0ded0567) and place them in the `./data/yelp2018/` directory.

To reproduce the results, simply re-run the notebook `experimentYelp.ipynb`. The notebook runs hyperparameter tuning and the main experiment. 

The results are saved in the `./results/yelp2018/` directory.


## Online experiment
Upon interest from the reviewers, we provide extended context for our online experiment conducted on a large international fashion discovery platform in May 2024. 
We describe the context to the extent permitted by the organization's non-disclosure policy.

**Task**: Personalize the rank of a selection (thousands) of fashion products, i.e., a subset of product category, *optionally* filtered by the user.
- Items recommended by the model (= with positive score) are ordered first in the list.
- If a user explicitly *dislikes* an item, we would like to hide it (place it at the very end of the list), as well as items related to it.
- The remaining items (with score = 0) are displayed after recommended items.

**Layout**: Scrollable grid (tens-hundreds of rows, ~5 products in row). Naturally, first several rows receive higher exposure.

**Training data**: Weighted implicit feedback. Training user-item matrix has $O(10^6)$ users, $O(10^6)$ items, and contains $O(10^7)$ interactions over the historical period used in training. The resulting data-Gram matrix has $O(10^9)$ nonzeros (=density ~0.1%).

**Models**: Baseline = proprietary implementation of [SANSA](https://dl.acm.org/doi/10.1145/3604915.3608827), a sparse variant of [EASE](https://arxiv.org/abs/1905.03375). New variant = absolute value of the baseline model. Retrained *daily*.

**Evaluation**: 7 day A/B test in 50-50 split. Over this period, each variant received roughly 0.5M sessions. We report observed 3% lift in CTR (Mann-Whitney p=2e7). Additionally, our experiment focused on conversion-related, monetary metrics (we cannot disclose numbers, but they were in favor of the proposed modifications).

To visually demonstrate the different behavior of the two variants, we provide additional examples similar to Fig. 3 in the `visual-examples` folder.
