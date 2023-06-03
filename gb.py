from pathlib import Path
import pandas as pd

INTERVALS = {"2": [1, 2], "3": [3, 4], "4": [5], "4+": [6], "5": [7], "6": [8, 9], "7": [10, 11], "8": [0]}


# test_choral_path = Path("choral.csv")


def create_intervals(chorals, mode=None):
    for choral in chorals:
        for chord in choral:
            continuum = []
            c = sorted(chord)
            for pitch in range(1, 4):
                interval = (c[pitch] - c[0]) % 12
                if mode == "gb":
                    n = [key for key, value in INTERVALS.items() if interval in value]
                    continuum.append(n[0])
                else:
                    continuum.append(interval + 36)
            del chord[1:3]
            continuum = sorted(continuum)
            for index, pitch in enumerate(continuum):
                chord.insert(index + 1, continuum[index])


def create_seed_intervals(choral, mode=None):
    for chord in choral:
        continuum = []
        c = sorted(chord)
        for pitch in range(1, 4):
            interval = (c[pitch] - c[0]) % 12
            if mode == "gb":
                n = [key for key, value in INTERVALS.items() if interval in value]
                continuum.append(n[0])
            else:
                continuum.append(interval + 36)
        del chord[1:3]
        continuum = sorted(continuum)
        for index, pitch in enumerate(continuum):
            chord.insert(index + 1, continuum[index])


def create_gb(choral):
    for chord in choral:
        for pitch in range(1, 4):
            interval = chord[pitch] - 36
            effective_interval = [key for key, value in INTERVALS.items() if interval in value]
            chord[pitch] = effective_interval[0]
