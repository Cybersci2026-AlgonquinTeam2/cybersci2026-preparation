# Hidden messages in audio and images

Use the [expanded command tree](chapters/media-analysis.md#run-the-decision-tree-at-the-terminal) during triage. It routes parser errors, stereo measurements, pulses, tone pairs, speech and image clues through specific commands and follow-up checks. This page is the short refresher and two-tone drill.

Work on a copy. Keep original sample rate and channels until you have compared them. Lossy recompression, downmixing and aggressive noise removal can erase a clue.

```sh
sha256sum clue.wav
file clue.wav
ffprobe -v error -show_format -show_streams clue.wav
ffmpeg -i clue.wav -lavfi showspectrumpic=s=1400x700 clue-spectrum.png
```

- **Speech-like but unintelligible:** listen once at safe volume; compare reverse playback in Audacity and modest speed changes. Preserve a timestamp and compare with the original. Do not guess words based on rhythm alone.
- **Repetitive beeps:** zoom in on the waveform. Measure beep and gap lengths from several samples. A short/long duration pattern suggests Morse. Two stable frequencies at once suggest DTMF. A changing pitch may be modulation. Verify with multiple symbols.
- **Odd tones or no obvious speech:** use Audacity's Spectrogram view. Try a wide frequency range, then zoom. A longer analysis window improves frequency resolution while blurring short pulses. Compare both views.
- **Stereo:** use Audacity's Split Stereo Track and solo each channel. If both sound alike, compare them before making a mono copy. A clue in opposite phase can disappear in mono.
- **Image:** check dimensions and metadata with `exiftool clue.png`. Inspect transparency, crop boundaries and color channels. Compare original and adjusted copies. Metadata can be forged.

## Worked audio drill

Create a harmless dual-tone file with known frequencies and inspect it without relying on the filename.

```sh
sox -n -r 16000 -c 1 a.wav synth 1 sine 697 vol 0.25
sox -n -r 16000 -c 1 b.wav synth 1 sine 1209 vol 0.25
sox -m a.wav b.wav exercise.wav
sox exercise.wav -n spectrogram -o exercise.png
```

Two horizontal bands should appear near 697 and 1209 Hz. This pair corresponds to DTMF digit 1. Compare `a.wav` as a control: it should have one band. If bursts are short, shrink the analysis window to distinguish their timing. Never assume an unknown clip is DTMF until you see two simultaneous tones matching a known pair.
