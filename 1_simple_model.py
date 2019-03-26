# Example of simple model creation.

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

## PART 1
# https://pypi.org/project/acumos/#using-dataframes-with-scikit-learn


import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

from acumos.modeling import Model, List, Dict, create_namedtuple, create_dataframe
from acumos.session import AcumosSession

iris = load_iris()
X = iris.data
y = iris.target

clf = RandomForestClassifier(n_estimators=100, random_state=0)
clf.fit(X, y)

# here, an appropriate NamedTuple type is inferred from a pandas DataFrame
X_df = pd.DataFrame(X, columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'])
IrisDataFrame = create_dataframe('IrisDataFrame', X_df)

# ==================================================================================
# # or equivalently:
#
# IrisDataFrame = create_namedtuple('IrisDataFrame', [('sepal_length', List[float]),
#                                                     ('sepal_width', List[float]),
#                                                     ('petal_length', List[float]),
#                                                     ('petal_width', List[float])])
# ==================================================================================

def classify_iris(df: IrisDataFrame) -> List[int]:
    '''Returns an array of iris classifications'''
    X = np.column_stack(df)
    return clf.predict(X)

model = Model(classify=classify_iris)

## PART 2
# https://pypi.org/project/acumos/#testing-models


ClassifyIn = model.classify.input_type
ClassifyOut = model.classify.output_type

class_in = ClassifyIn(5.1, 3.5, 1.4, 0.2)
print("== Example of Input ==")
print(class_in)  # AddIn(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2)

class_out = ClassifyOut(0)
print("== Example of Output ==")
print(class_out)  # AddOut(value=0)

print("== Testing I/O matches ==")
print(model.classify.wrapped(class_in))
print(model.classify.wrapped(class_in) == class_out)  # True
