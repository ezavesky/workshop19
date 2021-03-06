# ===============LICENSE_START=======================================================
# Apache-2.0
# ===================================================================================
# Copyright (C) 2019 AT&T Intellectual Property  All rights reserved.
# ===================================================================================
# This software file is distributed by AT&T
# under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============LICENSE_END=========================================================

import pandas as pd
from sklearn import metrics # metric plotting
from matplotlib import pyplot as plt
from sklearn import preprocessing  # data ETL

# What's the deal with this script!?

# When you want to re-use functionality, you can make a package, a library, or just another importable script. 
# We chose the latter solution here to keep it simple yet allow quick imports into other notebooks for 
# easy display of results in those respective environments.

## Performance Evaluation
# This quick function will plot the performance of our algorithm by finding the [area under the curve (aka ROC)](https://en.wikipedia.org/wiki/Receiver_operating_characteristic) for a simple [RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html) and compare it to a [GradientBoostedClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html#sklearn.ensemble.GradientBoostingClassifier). We can use the returned value (the `micro auc`) to more easily compare the performance of different models that we build.  It should be noted that no tuning for either model was done, so it doesn't speak to the overall fitness of one type versus another.


# Compute ROC curve and ROC area for each class
#     example from sklearn code: https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
def draw_roc(X_test, y_test, y_predict=None, title="ROC Curves", classifier=None):
    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    if classifier is not None:
        y_predict = classifier.predict_proba(X_test)
        class_set = classifier.classes_
    else:
        class_set = list(set(y_test))
    
    # this looks complicated, but we're making sure we have one column per class
    if len(y_test.shape)==1 or y_test.shape[1]==1:
        enc = preprocessing.OneHotEncoder(sparse=False, categories='auto')
        y_test =  enc.fit_transform(y_test.values.reshape(-1, 1)).astype(float)
        class_set = enc.categories_[0] # just one set of classes learned
    max_class = len(class_set)
    
    # for each class, compute the line
    for i in range(max_class):
        fpr[i], tpr[i], _ = metrics.roc_curve(y_test[:, i], y_predict[:, i])
        roc_auc[i] = metrics.auc(fpr[i], tpr[i])

    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = metrics.roc_curve(y_test.ravel(), y_predict.ravel())
    roc_auc["micro"] = metrics.auc(fpr["micro"], tpr["micro"])

    fig = plt.figure(1, figsize=(6, 6))
    lw = 2
    for i in range(max_class):
        ax = plt.plot(fpr[i], tpr[i],
                 lw=lw, label='ROC curve (class {}, area = {:.3f})'.format(class_set[i], roc_auc[i]))
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title+" (AUC {:.3f})".format(roc_auc["micro"]))
    plt.legend(loc="lower right")
    plt.show()
    return roc_auc["micro"], fig


# Compute a scaler and optionally show its performance
def preproc_scaler(models, df_test, df_train=None, verbose=False):
    if df_train is not None:
        models["scaler"] = preprocessing.RobustScaler()
        models["scaler"].fit(df_train)
        df_train = pd.DataFrame(models["scaler"].transform(df_train), 
                             index=df_train.index, columns=df_train.columns)
        
        # visualize the ranges of all data
        if verbose:
            col_show = df_train.columns[:30].append(df_train.columns[-30:])
            ax = df_train[col_show].boxplot(figsize=(12,6), rot=90)
            ax.set_title("Scaled Features")
            plt.show()
    # scale the test data
    df_test = pd.DataFrame(models["scaler"].transform(df_test), index=df_test.index, columns=df_test.columns)
    return models, df_test