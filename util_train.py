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

import requests
import time
from sklearn import ensemble # classifier
from sklearn import metrics # metric plotting
from sklearn import model_selection


# What's the deal with this script!?

# When you want to re-use functionality, you can make a package, a library, or just another importable script. 
# We chose the latter solution here to keep it simple yet allow quick imports into other notebooks for 
#       easy display of results in those respective environments.

def train_model(df_train, df_labels, scoring_list, model_type, cross_validate=False, 
                n_threads=1, random_state=0):
    """
    Train a model, optionally with cross validation from a set of known model types...
    :param df_train: training dataframe
    :param df_labels: label dataframe (binary)
    :param df_labels: label dataframe (binary)
    :param scoring_list: list of strings for scoring during cross-validation
    :param cross_validate: use cross validation or not (default=False)
    :param n_threads: number of threads in cross validation (default=1)
    :returns: dictionary with best, trained model in "best"
    """
    # here, we test two simple classifiers and plot their performance
    time_start = time.time()
    models = {}

    # first, choose our model according to specification
    if model_type.lower()=="rf":
        # use random forest as our classifier
        models["best"] = ensemble.RandomForestClassifier(n_estimators=100, random_state=random_state)
        # create some estimator parameter set
        models["param"] = {"n_estimators":(50, 100, 200), "max_depth":(2,5)}
    elif model_type.lower()=="gbm":
        # use gradient boosting as our classifier
        models["best"] = ensemble.GradientBoostingClassifier(random_state=random_state)
        # create some estimator parameter set
        models["param"] = {"n_estimators":(50, 100, 200), "max_features": (2,), "learning_rate":(0.1, 0.2)}
    elif model_type.lower()=="bayes":
        from sklearn import naive_bayes
        # use naive bayes as our classifier
        models["best"] = naive_bayes.MultinomialNB(random_state=random_state)
        # create some estimator parameter set
        models["param"] = {"alpha":(1.0, 0.7)}
    # elif X:
    #     from sklearn import naive_bayes
    #     # use naive bayes as our classifier
    #     models["best"] = naive_bayes.MultinomialNB()
    #     # create some estimator parameter set
    #     models["param"] = {"alpha":(1.0, 0.7)}
    #     sklearn.neighbors.KNeighborsClassifier
    else:
        raise Exception("Sorry, {} is an unknown model type at this time, why not create it!?".format(model_type))

    # want to cross-validate for training well?
    #   warning: this can take quite a while because of the sample count...
    if cross_validate:
        models["cv"] = model_selection.GridSearchCV(models["best"], models["param"], cv=3, verbose=2, 
                              n_jobs=n_threads, scoring=scoring_list, 
                              refit=scoring_list[0], return_train_score=True)
        # execute grid search
        print("Executing grid search ({})".format(clf))
        scores = models["cv"].fit(df_train, df_labels.values.ravel())
        models["best"] = models["cv"].best_estimator_
        print(models["cv"].cv_results_)
        # print out best performance
        print(models["best"])
        for t in ["train", "test"]:
            k = "mean_{}_{}".format(t, scoring_list[0])
            print("{}: {}".format(k, models["cv"].cv_results_[k]))
    # just do normal training...
    else: 
        models["best"].fit(df_train, df_labels.values.ravel())
    models["time_train"] = (time.time() - time_start)
    return models