#  Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""DNNRegressor with custom input_fn for Housing dataset."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools

import pandas as pd
import tensorflow as tf
import numpy as np

tf.logging.set_verbosity(tf.logging.INFO)

COLUMNS = ["weapon", "range", "damage"]
FEATURES = ["weapon", "range"]
LABEL = "damage"


def get_input_fn(data_set, num_epochs=None, shuffle=True):
  return tf.estimator.inputs.pandas_input_fn(
      x=pd.DataFrame({k: data_set[k].values for k in FEATURES}),
      y=pd.Series(data_set[LABEL].values),
      num_epochs=num_epochs,
      shuffle=shuffle)



def calculate(weapon_input, stat1_input, stat2_input, stat3_input, stat4_input, statname1_input, statname2_input, statname3_input, statname4_input):
    stat1_input = int(stat1_input)
    stat2_input = int(stat2_input)
    stat3_input = int(stat3_input)
    stat4_input = int(stat4_input)

    #weapon = tf.feature_column.categorical_column_with_vocabulary_list(
     #   'weapon', ['Pistol', 'Shotgun', 'SemiAutomatic Rifle', 'FullyAutomatic Rifle', 'Rocket Launcher']
    #)

    # Feature cols
    feature_cols = [tf.feature_column.indicator_column("weapon"),tf.feature_column.numeric_column("stat1"),tf.feature_column.numeric_column("stat2"),tf.feature_column.numeric_column("stat3"),tf.feature_column.numeric_column("stat4"),tf.feature_column.indicator_column("statname1"),tf.feature_column.indicator_column("statname1"),tf.feature_column.indicator_column("statname2"),tf.feature_column.indicator_column("statname3"),tf.feature_column.indicator_column("statname4"),tf.feature_column.indicator_column("price")]

    # Build 2 layer fully connected DNN with 10, 10 units respectively.
    regressor = tf.estimator.DNNRegressor(feature_columns=feature_cols,
                                          hidden_units=[10, 10],
                                          model_dir="/tmp/weaponstest")

    prediction_set = pd.read_csv('/dev/rivai/writefile.txt', skipinitialspace=True,
                                 skiprows=1, names=COLUMNS)

    predict_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"weapon" : np.array([weapon_input]), "stat1_input" : np.array([stat1_input]), "stat2_input" : np.array([stat2_input]), "stat3_input" : np.array([stat3_input]), "stat4_input" : np.array([stat4_input]), "statname1_input" : np.array([statname1_input]), "statname2_input" : np.array([statname2_input]), "statname3_input" : np.array([statname3_input]), "statname4_input" : np.array([statname4_input])}
        y=np.array([0]),
                  num_epochs=None,
                  shuffle=True
    )

    y = regressor.predict(
        input_fn=predict_input_fn)

    predictions = list(p["predictions"] for p in itertools.islice(y, 1))
    print("Predictions: {}".format(str(predictions)))

    return predictions[0]

def main(unused_argv):

  if len(unused_argv) > 0:
      calculate(unused_argv[0], unused_argv[1], unused_argv[2], unused_argv[3], unused_argv[4], unused_argv[5], unused_argv[6], unused_argv[7], unused_argv[8])
      return ""
  # Load datasets
  training_set = pd.read_csv('/dev/rivai/writefile.txt', skipinitialspace=True,
                             skiprows=1, names=COLUMNS)
  test_set = pd.read_csv('/dev/rivai/writefile.txt', skipinitialspace=True,
                         skiprows=1, names=COLUMNS)

  # Set of 6 examples for which to predict median house values
  prediction_set = pd.read_csv('/dev/rivai/writefile.txt', skipinitialspace=True,
                               skiprows=1, names=COLUMNS)

  #weapon = tf.feature_column.categorical_column_with_vocabulary_list(
   #   'weapon', ['Pistol', 'Shotgun', 'SemiAutomatic Rifle', 'FullyAutomatic Rifle', 'Rocket Launcher']
  #)

  # Feature cols
  feature_cols = [tf.feature_column.indicator_column("weapon"),tf.feature_column.numeric_column("stat1"),tf.feature_column.numeric_column("stat2"),tf.feature_column.numeric_column("stat3"),tf.feature_column.numeric_column("stat4"),tf.feature_column.indicator_column("statname1"),tf.feature_column.indicator_column("statname1"),tf.feature_column.indicator_column("statname2"),tf.feature_column.indicator_column("statname3"),tf.feature_column.indicator_column("statname4"),tf.feature_column.indicator_column("price")]

  # Build 2 layer fully connected DNN with 10, 10 units respectively.
  regressor = tf.estimator.DNNRegressor(feature_columns=feature_cols,
                                        hidden_units=[10, 10],
                                        model_dir="/tmp/weaponstest")

  # Train
  regressor.train(input_fn=get_input_fn(training_set), steps=5000)

  # Evaluate loss over one epoch of test_set.
  ev = regressor.evaluate(
      input_fn=get_input_fn(test_set, num_epochs=1, shuffle=False))
  loss_score = ev["loss"]
  print("Loss: {0:f}".format(loss_score))

  # Print out predictions over a slice of prediction_set.
  y = regressor.predict(
      input_fn=get_input_fn(prediction_set, num_epochs=1, shuffle=False))
  # .predict() returns an iterator of dicts; convert to a list and print
  # predictions
  predictions = list(p["predictions"] for p in itertools.islice(y, 6))
  print("Predictions: {}".format(str(predictions)))

if __name__ == "__main__":
  tf.app.run()