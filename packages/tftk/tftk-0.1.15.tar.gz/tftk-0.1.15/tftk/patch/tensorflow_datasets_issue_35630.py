# This is patch for tensorflow datasets issue 35630
# https://github.com/tensorflow/tensorflow/issues/35630


# coding=utf-8
# Copyright 2021 The TensorFlow Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module to use to extract archives. No business logic."""

import contextlib
from tensorflow_datasets.core import utils

import platform
import tensorflow_datasets

# Thefrom tensorflow_datasets.core.download.extractor import _open_or_pass

@contextlib.contextmanager
def _win_open_or_pass(path_or_fobj):
  print("WIN FILE!!!-------------")
  if isinstance(path_or_fobj, utils.PathLikeCls):
    with open(path_or_fobj, 'rb') as f_obj:
      yield f_obj
  else:
    yield path_or_fobj

def ENABLE_PATCH_TFDS_35630():
    if platform.system() == 'Windows':
      print("CALLED!!---------------------")
      extractor = tensorflow_datasets.core.download.extractor.get_extractor()
      extractor._open_or_pass = _win_open_or_pass
      
      # tensorflow_datasets.core.download.extractor._Extractor._open_or_pass = _win_open_or_pass
