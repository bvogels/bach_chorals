import tensorflow as tf
import gb as gb
import convert as ly
from preprocess import preprocess


def generate_chorale(model, seed_chords, melody, config):
    arpeggio = preprocess(tf.constant(seed_chords, dtype=tf.int64))
    arpeggio = tf.reshape(arpeggio, [1, -1])
    remaining_chords = len(melody) - len(seed_chords)
    for chord in range(remaining_chords):
        for note in range(config["parts"]):
            if note > 0 or config["mode"] == "Vogels":
                next_note = model.predict(arpeggio, verbose=0).argmax(axis=-1)[:1, -1:]
            else:
                next_note = tf.constant([[melody[chord + len(seed_chords)][0] - 35]],
                                        dtype=tf.int64)  # Assign the desired data type explicitly
            arpeggio = tf.concat([arpeggio, next_note], axis=1)
    arpeggio = tf.where(arpeggio == 0, arpeggio, arpeggio + 36 - 1)
    return tf.reshape(arpeggio, shape=[-1, config["parts"]])


def generate_chorale_v2(model, seed_chords, melody, config, temperature=1):
    arpeggio = preprocess(tf.constant(seed_chords, dtype=tf.int64))
    arpeggio = tf.reshape(arpeggio, [1, -1])
    remaining_chords = len(melody) - len(seed_chords)
    for chord in range(remaining_chords):
        for note in range(config["parts"]):
            if note > 0 or config["mode"] == "Geron":
                next_note_probas = model.predict(arpeggio)[0, -1:]
                rescaled_logits = tf.math.log(next_note_probas) / temperature
                next_note = tf.random.categorical(rescaled_logits, num_samples=1)
                arpeggio = tf.concat([arpeggio, next_note], axis=1)
            else:
                next_note = tf.constant([[melody[chord + len(seed_chords)][0] - 35]],
                                        dtype=tf.int64)  # Assign the desired data type explicitly
            arpeggio = tf.concat([arpeggio, next_note], axis=1)
    arpeggio = tf.where(arpeggio == 0, arpeggio, arpeggio + 36 - 1)
    return tf.reshape(arpeggio, shape=[-1, 4])


def create_new_choral(chorals, config):
    melody = chorals[2][2]
    if config["output"] == "gb":
        gb.create_seed_intervals(melody, config)
    seed_chords = melody[:8]

    model = tf.keras.models.load_model(config["model"])

    new_chorale = generate_chorale(model, seed_chords, melody, config)
    c = new_chorale.numpy().tolist()
    if config["output"] == "gb":
        gb.create_gb(c)
    print(c)

    ly.convert_to_ly(c, config)
