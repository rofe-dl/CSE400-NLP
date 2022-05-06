from process_dataset.text_features import get_train_test, get_data

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_validate
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer

import numpy as np

def get_random_forest():
    # return RandomForestClassifier(random_state=42)
    return RandomForestClassifier(**{
        'random_state': 42,
        'class_weight': None, 
        'criterion': 'gini', 
        'max_depth': 2000,
        'min_samples_leaf': 1, 
        'min_samples_split': 2,
        'n_estimators': 1500
    })

def main():
    rfc = get_random_forest()
    x_train, x_test, y_train, y_test = get_train_test()
    rfc.fit(x_train, y_train)

    results = rfc.predict(x_test)
    print(classification_report(y_test, results, digits=4))

def k_fold():
    pipeline = Pipeline(
        [('transformer', CountVectorizer(min_df=5, ngram_range=(1, 2))), ('estimator', get_random_forest())]
    )
    
    x, y = get_data()
    scoring = {'accuracy': 'accuracy',
           'f1_macro': 'f1_macro',
           'precision_macro': 'precision_macro',
           'recall_macro' : 'recall_macro',
           'f1_weighted' : 'f1_weighted',
           'precision_weighted' : 'precision_weighted',
           'recall_weighted' : 'recall_weighted'
           }
    
    scores = cross_validate(pipeline, x, y, cv=5, scoring=scoring, n_jobs=-1)

    print('Accuracy: ', np.mean(scores['test_accuracy']))
    print('F1 Macro: ', np.mean(scores['test_f1_macro']))
    print('Precision Macro: ', np.mean(scores['test_precision_macro']))
    print('Recall Macro: ', np.mean(scores['test_recall_macro']))
    print('F1 Weighted: ', np.mean(scores['test_f1_weighted']))
    print('Precision Weighted: ', np.mean(scores['test_precision_weighted']))
    print('Recall Weighted: ', np.mean(scores['test_recall_weighted']))

if __name__ == '__main__':
    print('On Train/Test Split', end='\n\n')
    main()
    print('On K-fold Cross Validation', end='\n\n')
    k_fold()