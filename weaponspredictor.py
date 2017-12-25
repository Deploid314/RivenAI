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
from sklearn.utils import shuffle

import itertools

import pandas as pd
import tensorflow as tf
import numpy as np
import normalize

tf.logging.set_verbosity(tf.logging.INFO)

COLUMNS = []
FEATURES = []
LABEL = ""

NN_layers = []

def load_columns(file_name):
    input_file = open(file_name)
    input_line = input_file.readline()
    input_line = input_line.replace('\n','')
    input_array = input_line.split(',')
    global COLUMNS
    COLUMNS = input_array[2:len(input_array)]
    global FEATURES
    FEATURES = input_array[2:len(input_array)-1]
    global LABEL
    LABEL = input_array[len(input_array)-1]
    global NN_layers
    NN_layers = [len(FEATURES) + 5, 50, 50]

def get_input_fn(data_set, num_epochs=None, shuffle=True):
  return tf.estimator.inputs.pandas_input_fn(
      x=pd.DataFrame({k: data_set[k].values for k in FEATURES}),
      y=pd.Series(data_set[LABEL].values),
      num_epochs=num_epochs,
      shuffle=shuffle)

def calculate(weapon_input, stat1_input, stat2_input, stat3_input, stat4_input, statname1_input, statname2_input, statname3_input, statname4_input, price_input):
    stat1_input = normalize.stat_converter(float(stat1_input))
    stat2_input = normalize.stat_converter(float(stat2_input))
    stat3_input = normalize.stat_converter(float(stat3_input))
    stat4_input = normalize.stat_converter(float(stat4_input))
    statname1_input = statname1_input.replace(' ','_')
    statname2_input = statname2_input.replace(' ', '_')
    statname3_input = statname3_input.replace(' ', '_')
    statname4_input = statname4_input.replace(' ', '_')

    calc_combined = [weapon_input, stat1_input, stat2_input, stat3_input, stat4_input, statname1_input, statname2_input, statname3_input, statname4_input]

    #weapon = tf.feature_column.categorical_column_with_vocabulary_list(
     #   'weapon', ['Pistol', 'Shotgun', 'SemiAutomatic Rifle', 'FullyAutomatic Rifle', 'Rocket Launcher']
    #)

    # Feature cols
    feature_cols = get_feature_cols()

    # Build 2 layer fully connected DNN with 10, 10 units respectively.
    regressor = tf.estimator.DNNRegressor(feature_columns=feature_cols,
                                          hidden_units = NN_layers,
                                          model_dir="/tmp/weaponstest")

    prediction_set = pd.read_csv('writefile.txt', skipinitialspace=True,
                                 skiprows=1, names=COLUMNS)
    x_dict = {}
    x_dict["weapon"] = np.array([weapon_input])

    for stats in FEATURES[1:]:
        x_dict[stats] = np.array([float(normalize.stat_converter(0))])
        for index in range(1,4):
            if stats == calc_combined[index+4]:
                x_dict[stats] = np.array([float(calc_combined[index])])

    print(x_dict)

    predict_input_fn = tf.estimator.inputs.numpy_input_fn(
        x=x_dict,

        y=np.array([0]),
                  num_epochs=None,
                  shuffle=True
    )
    y = regressor.predict(
        input_fn=predict_input_fn)

    predictions = list(p["predictions"] for p in itertools.islice(y, 1))

    print("Exp:" + str(price_input) + " Predicted: " + str(predictions[0]) + " Error: " + str(predictions[0]/price_input))

    return predictions[0]


def get_feature_cols():
    weapon = tf.feature_column.categorical_column_with_hash_bucket(
        key="weapon",
        hash_bucket_size=1000)
    feature_cols = [tf.feature_column.indicator_column(weapon)]

    for feature in FEATURES[1:]:
        feature_cols.append(tf.feature_column.numeric_column(feature))
    return feature_cols


def main(unused_argv):
  load_columns("normalized.txt")
  if len(unused_argv) > 1:
      calculate("Soma",72.1,1.3,75,-20,"Damage  Melee Damage","Punch Through","Critical Chance","Ammo Maximum", 800)
      calculate("Boar", 10.4, 10.6, 10.8, 0.0, "Status Duration", "Flight Speed", "Heat Damage", "none", 60)
      calculate("Scoliac", 100.5, 140.6, 110.2, -44.3, "Electric Damage", "Range", "Critical_Chance_on_Slide_Attack", "Damage vs Corpus", 1000)
      return ""
  # Load datasets
  full_set = pd.read_csv("normalized.txt", skipinitialspace=True,
                             skiprows=1, names=COLUMNS)

  # Feature cols
  feature_cols = get_feature_cols()

  # Build 2 layer fully connected DNN with 10, 10 units respectively.
  regressor = tf.estimator.DNNRegressor(feature_columns=feature_cols,
                                        hidden_units = NN_layers,
                                        model_dir="/tmp/weaponstest")

  # Train
  full_set = shuffle(full_set)
  training_size = int(len(full_set) * 0.9)
  training_set = full_set.iloc[:training_size]
  test_set = full_set.iloc[training_size:]
  for i in range(10000):
      regressor.train(input_fn=get_input_fn(training_set), steps=5000)

      # Evaluate loss over one epoch of test_set.
      ev = regressor.evaluate(
          input_fn=get_input_fn(test_set, num_epochs=1, shuffle=False))
      loss_score = ev["loss"]
      print("Loss: {0:f}".format(loss_score))

if __name__ == "__main__":
  tf.app.run()