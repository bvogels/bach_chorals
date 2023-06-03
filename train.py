import tensorflow as tf

from preprocess import bach_dataset


def train(chorals):
    train_chorales, valid_chorales, test_chorales = chorals

    notes = set()
    for chorales in (train_chorales, valid_chorales, test_chorales):
        for chorale in chorales:
            for chord in chorale:
                notes |= set(chord)

    n_notes = len(notes)
    min_note = min(notes - {0})
    max_note = max(notes)

    assert min_note == 36
    assert max_note == 81

    train_set = bach_dataset(train_chorales, shuffle_buffer_size=1000)
    valid_set = bach_dataset(valid_chorales)
    test_set = bach_dataset(test_chorales)

    n_embedding_dims = 5

    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(input_dim=n_notes, output_dim=n_embedding_dims,
                                  input_shape=[None]),
        tf.keras.layers.Conv1D(32, kernel_size=2, padding="causal", activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv1D(48, kernel_size=2, padding="causal", activation="relu", dilation_rate=2),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv1D(64, kernel_size=2, padding="causal", activation="relu", dilation_rate=4),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv1D(96, kernel_size=2, padding="causal", activation="relu", dilation_rate=8),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.LSTM(256, return_sequences=True),
        tf.keras.layers.Dense(n_notes, activation="softmax")
    ])

    model.summary()

    optimizer = tf.keras.optimizers.Adamax(learning_rate=1e-3)
    model.compile(loss="sparse_categorical_crossentropy", optimizer=optimizer,
                  metrics=["accuracy"])
    model.fit(train_set, epochs=20, validation_data=valid_set)

    model.save("my_bach_model_adamX", save_format="tf")
    model.evaluate(test_set)

    return model
