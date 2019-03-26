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

from sklearn import metrics # metric plotting
from matplotlib import pyplot as plt
from sklearn import preprocessing  # data ETL


## Performance Evaluation
# This quick function will plot the performance of our algorithm by finding the [area under the curve (aka ROC)](https://en.wikipedia.org/wiki/Receiver_operating_characteristic) for a simple [RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html) and compare it to a [GradientBoostedClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html#sklearn.ensemble.GradientBoostingClassifier). We can use the returned value (the `micro auc`) to more easily compare the performance of different models that we build.  It should be noted that no tuning for either model was done, so it doesn't speak to the overall fitness of one type versus another.


# Compute ROC curve and ROC area for each class
# example from sklearn code: https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
def draw_roc(classifier, X_test, y_test, title_str="ROC Curves"):
    y_score = classifier.predict_proba(X_test)
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    
    # this looks complicated, but we're making sure we have one column per class
    max_class = classifier.n_classes_
    if len(y_test.shape)==1 or y_test.shape[1]==1:
        y_test = preprocessing.OneHotEncoder(sparse=False, categories='auto') \
                            .fit_transform(y_test.values.reshape(-1, 1)).astype(float)
    # for each class, compute the line
    for i in range(classifier.n_classes_):
        fpr[i], tpr[i], _ = metrics.roc_curve(y_test[:, i], y_score[:, i])
        roc_auc[i] = metrics.auc(fpr[i], tpr[i])

    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = metrics.roc_curve(y_test.ravel(), y_score.ravel())
    roc_auc["micro"] = metrics.auc(fpr["micro"], tpr["micro"])

    plt.figure()
    lw = 2
    for i in range(classifier.n_classes_):
        plt.plot(fpr[i], tpr[i],
                 lw=lw, label='ROC curve (class {}, area = {:.2f})'.format(i, roc_auc[i]))
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title_str)
    plt.legend(loc="lower right")
    plt.show()
    return roc_auc["micro"]