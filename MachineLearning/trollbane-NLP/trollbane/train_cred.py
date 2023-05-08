# -*- coding: utf-8 -*-
"""
Created on Thursday, 15th May 2022 5:44:38 pm
===============================================================================
@filename:  train_cred.py
@project:   trollbane
@purpose:   Create model based off of credibility ratings.
===============================================================================
"""

import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Perceptron
from sklearn.metrics import (ConfusionMatrixDisplay, RocCurveDisplay,
                             accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score)
from sklearn.model_selection import train_test_split

from trollbane.paths import data_path


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--nodrive', action='store_true')
    args = parser.parse_args()

    if args.nodrive:
        df = pd.read_parquet(
        'notes-clean.parquet.gzip')
    #else:
    #    df = pd.read_parquet(
    #    data_path().joinpath('clean', 'notes-clean.parquet.gzip'))

    X = df['cred'].to_numpy().reshape(-1, 1)
    y = np.where(df['classification'].str.contains('MISINFORMED'), 1, 0)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42)

    clf = LogisticRegression(
        penalty='l2',
        random_state=42,
        max_iter=1000,
        multi_class='ovr')

    clf.fit(X_train, y_train)

    test_preds = clf.predict(X_test)
    train_preds = clf.predict(X_train)

    print(f'Accuracy on training data: {accuracy_score(y_train, train_preds)}')
    print(f'Accuracy on test data: {accuracy_score(y_test, test_preds)}')
    print(
        f'Precision on training data: {precision_score(y_train, train_preds)}')
    print(f'Precision on test data: {precision_score(y_test, test_preds)}')
    print(f'Recall on training data: {recall_score(y_train, train_preds)}')
    print(f'Recall on test data: {recall_score(y_test, test_preds)}')
    print(f'F1 score on training data: {f1_score(y_train, train_preds)}')
    print(f'F1 score on test data: {f1_score(y_test, test_preds)}')

    # RocCurveDisplay.from_estimator(clf, X_test, y_test)
    # plt.show()

    cm = confusion_matrix(y_test, test_preds, labels=clf.classes_)
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=clf.classes_)
    disp.plot()
    plt.show()
