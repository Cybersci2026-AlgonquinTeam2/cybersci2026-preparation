"""Generate small, local PCM WAV files for the field guide's audio drills."""

import argparse
import math
import struct
import wave
from pathlib import Path

RATE = 16000
AMPLITUDE = 5000


def tone(frequency, count):
    return [
        round(AMPLITUDE * math.sin(math.tau * frequency * index / RATE))
        for index in range(count)
    ]


def write_wav(path, channels):
    values = [sample for frame in zip(*channels, strict=True) for sample in frame]
    frames = struct.pack(f"<{len(values)}h", *values)
    # Exclusive create prevents a repeated run from overwriting any file.
    with path.open("xb") as output:
        with wave.open(output, "wb") as wav:
            wav.setparams((len(channels), 2, RATE, 0, "NONE", "not compressed"))
            wav.writeframes(frames)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="new directory for the fixtures")
    output = parser.parse_args().output
    output.mkdir()

    low = tone(697, RATE)
    high = tone(1209, RATE)
    write_wav(output / "tone-control.wav", [low])
    write_wav(output / "tone-pair.wav", [[a + b for a, b in zip(low, high, strict=True)]])
    common = tone(440, RATE)
    write_wav(
        output / "stereo-phase.wav",
        [
            [a + b for a, b in zip(common, high, strict=True)],
            [a - b for a, b in zip(common, high, strict=True)],
        ],
    )

    unit = RATE // 10
    pulses = []
    # S: three short pulses. O: three long pulses. S: three short pulses.
    for letter_index, code in enumerate(("...", "---", "...")):
        if letter_index:
            pulses.extend([0] * (3 * unit))
        for symbol_index, symbol in enumerate(code):
            if symbol_index:
                pulses.extend([0] * unit)
            pulses.extend(tone(700, unit if symbol == "." else 3 * unit))
    write_wav(output / "timing-message.wav", [pulses])
    print(f"Wrote four 16 kHz PCM fixtures to {output}")


if __name__ == "__main__":
    main()
