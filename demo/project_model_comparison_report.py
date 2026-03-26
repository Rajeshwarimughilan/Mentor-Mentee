#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate a cross-model comparison report for HDFS anomaly detection.

Output files:
- outputs/model_comparison.csv
- outputs/model_comparison.md
"""

import argparse
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.append('../')
from loglizer import dataloader, preprocessing
from loglizer.models import DecisionTree, IsolationForest, LR, PCA, SVM


STRUCT_LOG = '../data/HDFS/HDFS_100k.log_structured.csv'
LABEL_FILE = '../data/HDFS/anomaly_label.csv'
DEFAULT_MODELS = ['PCA', 'LR', 'DecisionTree', 'SVM', 'IsolationForest']


def parse_args():
    parser = argparse.ArgumentParser(description='Run model comparison and export a report.')
    parser.add_argument(
        '--models',
        type=str,
        default=','.join(DEFAULT_MODELS),
        help='Comma-separated model list. Supported: PCA,LR,DecisionTree,SVM,IsolationForest',
    )
    parser.add_argument(
        '--train-ratio',
        type=float,
        default=0.5,
        help='Train split ratio for HDFS session windows.',
    )
    parser.add_argument(
        '--iforest-contamination',
        type=float,
        default=0.03,
        help='IsolationForest contamination ratio.',
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='../outputs',
        help='Directory to store CSV/Markdown report.',
    )
    return parser.parse_args()


def build_registry(iforest_contamination):
    return {
        'PCA': {
            'factory': lambda: PCA(),
            'fit_needs_labels': False,
            'feature_kwargs': {'term_weighting': 'tf-idf', 'normalization': 'zero-mean'},
        },
        'LR': {
            'factory': lambda: LR(),
            'fit_needs_labels': True,
            'feature_kwargs': {'term_weighting': 'tf-idf'},
        },
        'DecisionTree': {
            'factory': lambda: DecisionTree(),
            'fit_needs_labels': True,
            'feature_kwargs': {'term_weighting': 'tf-idf'},
        },
        'SVM': {
            'factory': lambda: SVM(),
            'fit_needs_labels': True,
            'feature_kwargs': {'term_weighting': 'tf-idf'},
        },
        'IsolationForest': {
            'factory': lambda: IsolationForest(contamination=iforest_contamination),
            'fit_needs_labels': False,
            'feature_kwargs': {},
        },
    }


def split_data(train_ratio):
    (x_train, y_train), (x_test, y_test) = dataloader.load_HDFS(
        STRUCT_LOG,
        label_file=LABEL_FILE,
        window='session',
        train_ratio=train_ratio,
        split_type='uniform',
    )
    return x_train, y_train, x_test, y_test


def evaluate_model(model_name, spec, x_train_raw, y_train, x_test_raw, y_test):
    extractor = preprocessing.FeatureExtractor()
    x_train = extractor.fit_transform(x_train_raw, **spec['feature_kwargs'])
    x_test = extractor.transform(x_test_raw)

    model = spec['factory']()

    start = time.perf_counter()
    if spec['fit_needs_labels']:
        model.fit(x_train, y_train)
    else:
        model.fit(x_train)
    fit_seconds = time.perf_counter() - start

    y_pred = np.asarray(model.predict(x_test)).astype(int)
    y_true = np.asarray(y_test).astype(int)

    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))

    precision, recall, f1 = model.evaluate(x_test, y_true)

    # Security-tilted score: prioritize anomaly catch rate (recall) then balance with F1.
    security_score = (0.60 * recall + 0.30 * f1 + 0.10 * precision) * 100.0

    return {
        'model': model_name,
        'precision': round(float(precision), 4),
        'recall': round(float(recall), 4),
        'f1': round(float(f1), 4),
        'security_score': round(float(security_score), 2),
        'tp': tp,
        'fp': fp,
        'tn': tn,
        'fn': fn,
        'fit_seconds': round(float(fit_seconds), 4),
    }


def main():
    args = parse_args()
    selected_models = [m.strip() for m in args.models.split(',') if m.strip()]
    registry = build_registry(args.iforest_contamination)

    unknown = [m for m in selected_models if m not in registry]
    if unknown:
        raise ValueError('Unsupported model(s): {}. Supported: {}'.format(', '.join(unknown), ', '.join(registry.keys())))

    print('====== Loading dataset ======')
    x_train_raw, y_train, x_test_raw, y_test = split_data(args.train_ratio)

    rows = []
    for model_name in selected_models:
        print('\n====== Running {} ======'.format(model_name))
        row = evaluate_model(model_name, registry[model_name], x_train_raw, y_train, x_test_raw, y_test)
        rows.append(row)

    df = pd.DataFrame(rows)
    df = df.sort_values(by=['security_score', 'f1', 'recall'], ascending=False).reset_index(drop=True)
    df.insert(0, 'rank', np.arange(1, len(df) + 1))

    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), args.output_dir))
    os.makedirs(out_dir, exist_ok=True)

    csv_path = os.path.join(out_dir, 'model_comparison.csv')
    md_path = os.path.join(out_dir, 'model_comparison.md')

    df.to_csv(csv_path, index=False)

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('# Model Comparison Report\n\n')
        f.write('Sorted by `security_score` (higher is better).\n\n')
        f.write(df.to_markdown(index=False))
        f.write('\n')

    print('\n====== Comparison summary ======')
    print(df.to_string(index=False))
    print('\nSaved CSV : {}'.format(csv_path))
    print('Saved MD  : {}'.format(md_path))


if __name__ == '__main__':
    main()
