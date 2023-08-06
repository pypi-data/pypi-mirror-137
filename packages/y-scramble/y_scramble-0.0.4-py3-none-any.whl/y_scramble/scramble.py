from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import SCORERS
import pandas as pd
import numpy as np
import scipy
import copy

class Scrambler:

    def __init__(self, model, iterations=100):
        self.base_model = model
        self.scrambled_models = []
        self.iterations = iterations
    
    def validate(self, X, y, method="train_test_split", scoring="accuracy", cross_val_score_aggregator="mean", pvalue_threshold=0.05, cv_kfolds=7, as_df=False):
        model_scorer = SCORERS.get(scoring)
        if model_scorer is None:
            raise Exception(f"scoring function '{model_scorer}' is not a sklearn scorer")

        if method == "train_test_split":
            base_model_score, scrambled_model_scores = self.__validate_train_test_split(X, y, model_scorer)

        elif method == "cross_validation":
            base_model_score, scrambled_model_scores = self.__validate_cross_validation(X, y, model_scorer, aggregation=cross_val_score_aggregator, cv_kfolds=cv_kfolds)

        all_scores = [base_model_score, *scrambled_model_scores]

        all_scores_zscores = scipy.stats.zscore(all_scores)
        all_scores_pvalues = scipy.stats.norm.sf(abs(all_scores_zscores))*2

        all_scores_significances = all_scores_pvalues <= pvalue_threshold

        if as_df:

            df = pd.DataFrame({"score": all_scores, "zscore": all_scores_zscores, "pvalue": all_scores_pvalues, "significancy": all_scores_significances})
            df['model'] = 'base_model'
            df['model'][1::] = 'randomized'

            return df

        else:

            return all_scores, all_scores_zscores, all_scores_pvalues, all_scores_pvalues <= pvalue_threshold

    def __validate_train_test_split(self, X, y, scorer):
        
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        self.base_model.fit(X_train, y_train)
        self.scrambled_models = [copy.copy(self.base_model) for _ in range(self.iterations)]
        base_model_score = scorer(self.base_model, X_test, y_test)
        scrambled_model_scores = []

        for scrambled_model in self.scrambled_models:

            y_train_scrambled = copy.copy(y_train)
            np.random.shuffle(y_train_scrambled)
            scrambled_model.fit(X_train, y_train_scrambled)
            scrambled_model_score = scorer(scrambled_model, X_test, y_test)
            scrambled_model_scores.append(scrambled_model_score)

        return base_model_score, scrambled_model_scores
        
    def __validate_cross_validation(self, X, y, scorer, aggregation="mean", cv_kfolds=7):
        
        if aggregation == "mean":
            aggregator = np.mean
        elif aggregation == "median":
            aggregator = np.median
        else:
            raise Exception(f"aggregation function '{aggregation}' is not available (choose mean or median)")

        base_model_score = aggregator(cross_val_score(self.base_model, X, y, scoring=scorer, cv=cv_kfolds))
        self.scrambled_models = [copy.copy(self.base_model) for _ in range(self.iterations)]

        scrambled_model_scores = []

        for scrambled_model in self.scrambled_models:
            y_scrambled = copy.copy(y)
            np.random.shuffle(y_scrambled)
            scores = cross_val_score(scrambled_model, X, y_scrambled, scoring=scorer)
            scrambled_model_score = aggregator(scores)
            scrambled_model_scores.append(scrambled_model_score)
            
        return base_model_score, scrambled_model_scores