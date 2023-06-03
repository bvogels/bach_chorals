import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

STATS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def create_statistic(chorales):
    for c in chorales:
        for choral in c:
            for chord in choral:
                for pitch in chord:
                    v = (pitch - 35) % 12
                    STATS[v-1] += 1

    pitches = ['c', 'cis/des', 'd', 'dis/es', 'e', 'f', 'fis/ges', 'g', 'gis/as', 'a', 'ais/b', 'h']

    plt.bar(pitches, STATS)
    plt.title("Verteilung der Töne der Oktave (Normalisiert auf C-Dur)")
    plt.xlabel("Ton")
    plt.ylabel("Häufigkeit")
    plt.show()
    plt.savefig('pitches.pgf')
