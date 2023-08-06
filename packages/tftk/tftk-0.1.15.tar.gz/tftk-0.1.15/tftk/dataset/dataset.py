import tensorflow as tf
import tensorflow_datasets as tfds
from typing import Tuple

class TFDS():
    @classmethod
    def get_dataset(cls, name:str, split:str, data_dir:str=None)->Tuple[tf.data.Dataset, int]:
        ds, info = tfds.load(name=name, split=split, data_dir=data_dir, with_info=True)
        return ds, info.splits[split].num_examples
