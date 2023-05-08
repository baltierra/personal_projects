# -*- coding: utf-8 -*-
"""
Created on Thursday, 12th May 2022 10:20:50 pm
===============================================================================
@filename:  train_notes.py
@project:   trollbane
@purpose:   enter purpose
===============================================================================
"""

import argparse
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (ConfusionMatrixDisplay, RocCurveDisplay,
                             accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score)
from sklearn.model_selection import (GridSearchCV, cross_validate,
                                     train_test_split)

from trollbane.paths import data_path


def get_top_20_features(clf: LogisticRegression,
                        features: Union[CountVectorizer, TfidfVectorizer],
                        ) -> dict[str, float]:
    """
    gets the top 20 coefficients in absolute value from a logistic regression
    classifier and it

    Args:
        clf (LogisticRegression): _description_

    Returns:
        dict[str, float]: _description_
    """
    top20idxs = np.argsort(np.abs(clf.coef_)[0])[::-1][:20]
    top20words = features.get_feature_names_out()[top20idxs]
    top20coefs = clf.coef_[0][top20idxs]
    coefsort = np.argsort(top20coefs)

    return dict(zip(top20words[coefsort], top20coefs[coefsort]))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--nodrive', action='store_true')
    args = parser.parse_args()

    if args.nodrive:
        df = pd.read_parquet(
            'notes-clean.parquet.gzip',
            columns=['classification', 'summary'])
    else:
        df = pd.read_parquet(
            data_path().joinpath('clean', 'notes-clean.parquet.gzip'),
            columns=['classification', 'summary'])

    tfidf = TfidfVectorizer(lowercase=False, binary=True)
    bowdf = CountVectorizer(lowercase=False, binary=True)
    X_tfidf = tfidf.fit_transform(df['summary'])
    X_bow = bowdf.fit_transform(df['summary'])
    y = np.where(df['classification'].str.contains('MISINFORMED'), 1, 0)

    features = {'tfidf': X_tfidf, 'bow': X_bow}

    test_accuracy: list[float] = []
    train_accuracy: list[float] = []
    test_precision: list[float] = []
    train_precision: list[float] = []
    test_recall: list[float] = []
    train_recall: list[float] = []
    test_f1: list[float] = []
    train_f1: list[float] = []
    test_auc: list[float] = []
    train_auc: list[float] = []

    for feat_type, feats in features.items():
        X_train, X_test, y_train, y_test = train_test_split(
            feats, y,
            test_size=0.2,
            random_state=42)

        param_grid = {'C': np.logspace(-3, 3, 7)}
        lr = LogisticRegression(max_iter=10000)
        gscv = GridSearchCV(
            estimator=lr,
            param_grid=param_grid,
            scoring='roc_auc',
            n_jobs=4)
        gscv.fit(X_train, y_train)
        clf = gscv.best_estimator_

        tokens, coefs = zip(*get_top_20_features(clf, bowdf).items())

        fig, ax = plt.subplots(figsize=(6, 5))
        ax.barh(y=tokens, width=coefs, edgecolor='k', alpha=0.8)
        ax.axvline(x=0, ls='--', color='grey', alpha=0.8)
        if feat_type == 'tfidf':
            ax.set_title('TF-IDF Encoding')
        elif feat_type == 'bow':
            ax.set_title('Bag-of-Words Encoding')
        plt.suptitle('Top 20 Features in absolute value')
        ax.set_xlabel('Coefficent Magnitude')
        ax.set_ylabel('Tokens')
        fig.tight_layout()
        fig.savefig(f'figs/{feat_type}-token-coefs.eps')
        plt.close()

        fig, ax = plt.subplots(figsize=(6, 4))
        roc = RocCurveDisplay.from_estimator(clf, X_test, y_test, ax=ax)
        ax.plot((0, 1), ls='--', color='gray', alpha=0.8)
        fig.tight_layout()
        fig.savefig(f'figs/{feat_type}-roc-text.eps')
        plt.close()

        test_preds = clf.predict(X_test)
        train_preds = clf.predict(X_train)

        test_accuracy.append(accuracy_score(y_test, test_preds))
        train_accuracy.append(accuracy_score(y_train, train_preds))

        test_precision.append(precision_score(y_test, test_preds))
        train_precision.append(precision_score(y_train, train_preds))

        test_recall.append(recall_score(y_test, test_preds))
        train_recall.append(recall_score(y_train, train_preds))

        test_f1.append(f1_score(y_train, train_preds))
        train_f1.append(f1_score(y_test, test_preds))

        test_auc.append(roc_auc_score(y_test, clf.predict_proba(X_test)[:, 1]))
        train_auc.append(
            roc_auc_score(y_train, clf.predict_proba(X_train)[:, 1]))

    statdf = pd.DataFrame(
        data={
            'Train Accuracy': train_accuracy,
            'Test Accuracy': test_accuracy,
            'Train Precision': train_precision,
            'Test Precision': test_precision,
            'Train Recall': train_recall,
            'Test Recall': test_recall,
            'Train F1-Score': train_f1,
            'Test F1-Score': test_f1,
            'Train AUC': train_auc,
            'Test AUC': test_auc
        }
    )
    statdf = statdf.T
    statdf.columns = ('TF-IDF', 'BOW')
    statdf.to_latex(
        buf='tables/logistic-scores.tex',
        float_format='%.3f',
        bold_rows=True)
