import numpy as np

soprano = []
alto = []
tenor = []
bass = []

upper = []
lower = []

basso_continuo = []

parts = []

s = [["c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "ais", "h"],
     ["c", "des", "d", "es", "e", "f", "ges", "g", "as", "a", "b", "h"]]


#scale = []


def convert_to_ly(choral, config):
    if config["choral_accidentals"] == "sharp":
        scale = s[0]
    else:
        scale = s[1]
    if len(choral[0]) == 4:  # if traditional four part chorales
        music = [soprano, alto, tenor, bass]
        for chord in choral:
            for index, pitch in enumerate(chord):
                pitch = (pitch - 36) % 12
                music[index].append(scale[pitch])
        make_four_part_lilypond(write_parts(music))
    else:  # if only soprano and bass are given and remainder is basso continuo
        music = [soprano, bass]
        for chord in choral:
            pitch = (chord[0] - 36) % 12
            music[0].append(scale[pitch])
            pitch = (chord[4] - 36) % 12
            music[1].append(scale[pitch])
        make_two_part_lilypond(write_parts(music), choral)


def write_parts(music):
    part = ""
    pitch_count = 1
    for voice in music:
        for index, pitch in enumerate(voice):
            if (index < len(voice) - 1 and pitch == voice[index + 1]) and (index + 1) % 4 != 0:
                pitch_count += 1
            else:
                if pitch_count == 16:
                    part += pitch + "4 " + pitch + " " + pitch + " " + pitch + " "
                elif pitch_count == 12:
                    part += pitch + "4 " + pitch + " " + pitch + " "
                elif pitch_count == 8:
                    part += pitch + "4 " + pitch + " "
                elif pitch_count == 6:
                    part += pitch + "4. "
                elif pitch_count == 4:
                    part += pitch + "4 "
                elif pitch_count == 3:
                    part += pitch + "8. "
                elif pitch_count == 2:
                    part += pitch + "8 "
                elif pitch_count == 1:
                    part += pitch + "16 "
                pitch_count = 1
        parts.append(part)
        part = ""
    return parts


def make_four_part_lilypond(four_parts):
    voices = ["soprano", "alto", "tenor", "bass"]
    for voice, part in zip(voices, four_parts):
        if voice == "soprano" or voice == "alto":
            lilypond_code = f'{voice} = \\relative c\' {{ {part} }}'
            upper.append(lilypond_code)
        else:
            lilypond_code = f'{voice} = \\relative c {{ {part} }}'
            lower.append(lilypond_code)
    print(print_score())


def make_two_part_lilypond(two_parts, choral):
    voices = ["soprano", "bass"]
    bc = ""
    for voice, part in zip(voices, two_parts):
        if voice == "soprano":
            lilypond_code = f'{voice} = \\relative c\' {{ {part} }}'
            upper.append(lilypond_code)
        else:
            lilypond_code = f'{voice} = \\relative c {{ {part} }}'
            lower.append(lilypond_code)
    for index, chord in enumerate(range(0, len(choral) - 1, 2)):
        gb = extract_gb(choral[chord])
        if index > 0 and gb == "8 5 3 ":
            bc += f's8 '
        else:
            bc += f'<{gb}>8 '
    lilypond_code = f'bassoContinuo = \\figures {{ {bc} }}'
    basso_continuo.append(lilypond_code)
    print(basso_continuo)
    print(print_score_with_bc())


def extract_gb(chord):
    continuo = ""
    gb = list(set(chord[1:4]))
    for pitch in sorted(gb, reverse=True):
        continuo += pitch + " "
    return continuo


def print_score():
    lilypond_template = f'\\include "deutsch.ly" ' \
                        f'{upper[0]} {upper[1]} {lower[0]} {lower[1]}' \
                        f'\\score {{' \
                        f'\\new PianoStaff << ' \
                        f'\\new Staff << ' \
                        f'\\new Voice = "soprano" \\relative {{ \\voiceOne \\soprano }} ' \
                        f'\\new Voice = "alto" \\relative {{ \\voiceTwo \\alto }} >> ' \
                        f'\\new Staff << ' \
                        f'\\clef bass ' \
                        f'\\new Voice = "tenor"  \\relative {{ \\voiceOne \\tenor }} ' \
                        f'\\new Voice = "bass" \\relative {{ \\voiceTwo \\bass }} >>' \
                        f'\\new FiguredBass {{ \\bassoContinuo }} ' \
                        f' >>' \
                        f'}}'
    return lilypond_template


def print_score_with_bc():
    lilypond_template = f'\\include "deutsch.ly" ' \
                        f'{upper[0]} {lower[0]} {basso_continuo[0]}' \
                        f'\\score {{' \
                        f'\\new PianoStaff << ' \
                        f'\\new Staff << ' \
                        f'\\new Voice = "soprano" \\relative {{ \\soprano }} >> ' \
                        f'\\new Staff << ' \
                        f'\\clef bass ' \
                        f'\\new Voice = "bass" \\relative {{ \\bass }} >>' \
                        f'\\new FiguredBass {{ \\bassoContinuo }} ' \
                        f' >>' \
                        f'}}'
    return lilypond_template
