from pathlib import Path

import pandas as pd
import tensorflow as tf

from gb import create_intervals
from generate import create_new_choral
from statistic import create_statistic
from train import train


def obtain_data():
    chorales = []
    tf.keras.utils.get_file(
        "jsb_chorales.tgz",
        "https://github.com/ageron/data/raw/main/jsb_chorales.tgz",
        cache_dir=".",
        extract=True)

    jsb_chorales_dir = Path("datasets/jsb_chorales")
    train_files = sorted(jsb_chorales_dir.glob("train/chorale_*.csv"))
    valid_files = sorted(jsb_chorales_dir.glob("valid/chorale_*.csv"))
    test_files = sorted(jsb_chorales_dir.glob("test/chorale_*.csv"))
    chorales.append(train_files)
    chorales.append(valid_files)
    chorales.append(test_files)
    return chorales


def load_chorales(filepaths):
    return [pd.read_csv(filepath).values.tolist() for filepath in filepaths]


def make_choral_sets(chorales):
    return [load_chorales(chorale) for chorale in chorales]


def make_gb(chorales, configuration):
    if configuration["train_with_gb"]:
        for c in chorales:
            create_intervals(c, config)
    return chorales


# convert_to_ly(train_chorales[0])


# play_chords(new_chorale, filepath="testchoral1.wav")

if __name__ == "__main__":
    config = {
        "mode": "Geron",  # "Vogels"
        "choral_accidentals": "sharp",  # "flat"
        "output": "gb",  # "gb"
        "melody": 4,
        "train": False,
        "test": False,
        "create": True,
        "statistic": False,
        "train_with_gb": False,
        "model": "my_bach_model_gb",
        "parts": 5
    }

    chorals = obtain_data()
    chorals = make_choral_sets(chorals)
    if config["statistic"]:
        create_statistic(chorals)
    if config["train"] or config["test"]:
        chorals = make_gb(chorals, config)
        model = train(chorals)
    if config["create"]:
        create_new_choral(chorals, config)
