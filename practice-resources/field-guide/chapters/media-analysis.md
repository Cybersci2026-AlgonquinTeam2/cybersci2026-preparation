# Audio, images and hidden messages

An audio file can carry a clue in speech, timing, pitch, channel differences or metadata. Each possibility predicts a different observable feature. If dots and dashes are encoded as pulses, changing the frequency display won't fix a timing problem. If text is drawn in frequency over time, zooming into a waveform may only make a dense blob bigger. Pick your display to match the hypothesis.

## Inputs, outputs and prerequisites

Use a local copy of the authorized artifact and open it in a disposable VM when its origin is uncertain. Start with headphones at a low volume, especially if a clip contains unfamiliar tones. Kali toolkit packages include FFmpeg (with ffprobe), SoX, ExifTool and optional Audacity and GIMP. Keep the source and every derivative in different files. Commands below assume a Bash terminal in a scratch directory. Replace example filenames as needed. Avoid posting competition artifacts to hosted analyzers.

Inputs: original media, the exact question, expected answer format, and any supplied reference. Outputs: metadata report, a timestamped observation, independent validation, and the smallest repeatable transformation that reveals the clue.

## Decision tree

~~~mermaid
flowchart TD
    A["Hash original and inventory streams"] --> B{"Does container and stream metadata make sense?"}
    B -- No --> C["Check signature and parser errors. Preserve original."]
    B -- Yes --> D{"Where is the evidence?"}
    D -- Speech --> E["Compare channels. Try reversible playback changes."]
    D -- Pulses --> F["Mark boundaries in waveform. Measure tones and gaps."]
    D -- Text-like pattern --> G["Inspect spectrogram. Sweep window and frequency range."]
    D -- Stereo anomaly --> H["Solo L and R. Compare sum and difference."]
    D -- Image --> I["Separate RGB and alpha. Inspect native pixels."]
    D -- Metadata or extra stream --> J["List format tags and per-stream properties. Corroborate."]
    E --> K{"Can a teammate reproduce it from the original?"}
    F --> K
    G --> K
    H --> K
    I --> K
    J --> K
    K -- Yes --> L["Record tool settings, interval, output and confidence."]
    K -- No --> M["Try a control and return to the last confirmed observation."]
~~~

**Offline route:** inventory first. Speech goes to playback and channel comparison. Pulses go to timing measurement. Tones or apparent images go to the spectrogram. Stereo anomalies go to left, right and difference comparisons. Images go to RGBA inspection. Validate each result on a preserved original.

| First observation | Try first | What would change your mind? |
|---|---|---|
| The opening and ending sound backwards | Reverse the complete stream on a copy | The resulting words have no consistent syntax or audible agreement across multiple phrases |
| Short and long beeps | Measure on/off durations | Durations overlap heavily or two simultaneous frequencies encode each symbol |
| Recurring paired tones | Compare two peaks per interval to known DTMF pairs | The alleged second peak is harmonic, drifts, or fails to coexist in the same window |
| Narrow slanted bands | Inspect a linear-frequency spectrogram | The structure follows ordinary harmonics in a spoken or musical passage |
| One ear differs strongly | Solo each channel and compare a difference track | The same apparent pattern remains in both channels at the same time |
| Image looks blank | Inspect alpha and individual color channels | Pixel values are uniform in every original channel |

## Run the decision tree at the terminal

~~~mermaid
flowchart TD
    Entry["Enter at the first applicable node"] --> Step1
    Step1["1. file -- clue.wav"] --> Result1{"Inventory and branch by format"}
    Result1 -->|Stereo| Step2
    Result1 -->|mono| Step3
    Result1 -->|mono| Step4
    Result1 -->|image| Step5
    Result1 -->|parser error| End1_3["1. Follow the matching result below"]
    Step2["2. ffmpeg -n -i clue.wav -map 0:a:0 -af 'pan=mono&#124;c0=c0' left.wav"] --> Result2{"Compare original channels and difference"}
    Result2 -->|Feature stronger in a channel or difference| End2_0["2. Follow the matching result below"]
    Result2 -->|similar outputs| End2_1["2. Follow the matching result below"]
    Result2 -->|missing channel| Step1
    Result2 -->|existing output| End2_3["2. Follow the matching result below"]
    Step3["3. sox clue.wav -n spectrogram -x 1200 -y 257 -z 80 -o clue-spectrum.png"] --> Result3{"Distinguish duration, simultaneous tones and visible shapes"}
    Result3 -->|Constant pitch plus short/long pulses| End3_0["3. Follow the matching result below"]
    Result3 -->|two simultaneous bands| End3_1["3. Follow the matching result below"]
    Result3 -->|visual shapes| End3_2["3. Follow the matching result below"]
    Result3 -->|no stable structure| Step4
    Step4["4. ffmpeg -n -i clue.wav -ss 4.25 -t 2.5 excerpt.wav"] --> Result4{"Test a short speech-like excerpt"}
    Result4 -->|Independent listeners agree| End4_0["4. Follow the matching result below"]
    Result4 -->|excerpt empty| Step1
    Result4 -->|ambiguous result| Step3
    Step5["5. exiftool -a -G1 -s clue.png"] --> Result5{"Inspect image evidence and metadata separately"}
    Result5 -->|Clue in pixels| End5_0["5. Follow the matching result below"]
    Result5 -->|clue only in metadata| End5_1["5. Follow the matching result below"]
    Result5 -->|format mismatch| End5_2["5. Follow the matching result below"]
~~~


Start at **1**. Each node gives the exact check, the options that affect the result, and where to go for each outcome. Filenames are placeholders for your local working copies. **Record** means save the observation and its evidence locator. **Hand off** means keep the last confirmed result and state what is missing.

### 1 · Inventory and branch by format

~~~bash
file -- clue.wav
ffprobe -v error -show_streams -show_format -of json clue.wav
~~~

**Options and interpretation.** `--` ends file options. `-v error` limits diagnostics, `-show_streams` gives stream/channels, `-show_format` gives container fields, and `-of json` selects JSON.

- **Stereo.** **2**
- **mono.** **3** or **4** if speech-like
- **image.** **5**
- **parser error.** compare the first 32 bytes with `xxd -g 1 -l 32 clue.wav` before trying another parser.

### 2 · Compare original channels and difference

~~~bash
ffmpeg -n -i clue.wav -map 0:a:0 -af 'pan=mono|c0=c0' left.wav
ffmpeg -n -i clue.wav -map 0:a:0 -af 'pan=mono|c0=c1' right.wav
ffmpeg -n -i clue.wav -map 0:a:0 -af 'pan=mono|c0=0.5*c0+0.5*c1' sum.wav
ffmpeg -n -i clue.wav -map 0:a:0 -af 'pan=mono|c0=0.5*c0-0.5*c1' diff.wav
~~~

**Options and interpretation.** `-n` prevents overwrite; `-i` names input; `-map 0:a:0` selects the first audio stream of input zero; `-af pan` maps sample channels. Coefficients select one channel or compute half-sum and half-difference.

- **Feature stronger in a channel or difference.** use it in **3–4** and record the transform
- **similar outputs.** use a clean channel
- **missing channel.** back to **1**
- **existing output.** pick fresh names.

### 3 · Distinguish duration, simultaneous tones and visible shapes

~~~bash
sox clue.wav -n spectrogram -x 1200 -y 257 -z 80 -o clue-spectrum.png
~~~

**Options and interpretation.** `-n` discards audio output. `-x` sets width, `-y` vertical bins per channel, `-z` visible dB range and `-o` the image path.

- **Constant pitch plus short/long pulses.** map timings in waveform view
- **two simultaneous bands.** compare to the DTMF grid and single-tone control
- **visual shapes.** vary window size and keep time and frequency ranges
- **no stable structure.** test a known fixture or go to **4**.

### 4 · Test a short speech-like excerpt

~~~bash
ffmpeg -n -i clue.wav -ss 4.25 -t 2.5 excerpt.wav
ffmpeg -n -i excerpt.wav -af areverse excerpt-reversed.wav
~~~

**Options and interpretation.** `-ss` after the input selects the output start in seconds, `-t` gives duration, and `areverse` reverses the buffered excerpt. Use the observed interval instead of the example numbers.

- **Independent listeners agree.** record text plus original offset and duration
- **excerpt empty.** check timeline at **1**
- **ambiguous result.** return to **3** or hand off with an uncertainty note.

### 5 · Inspect image evidence and metadata separately

~~~bash
exiftool -a -G1 -s clue.png
xxd -g 1 -l 32 clue.png
~~~

**Options and interpretation.** `-a` includes duplicate tags, `-G1` shows field group, `-s` shows short names, `-g 1` groups bytewise, and `-l 32` limits the hex read.

- **Clue in pixels.** inspect RGB, alpha and native scale in GIMP
- **clue only in metadata.** corroborate before accepting
- **format mismatch.** use the file evidence tree.

## Command reference and reasoning

~~~bash
sha256sum -- clue.wav
file -- clue.wav
ffprobe -v error -show_format -show_streams -of json clue.wav > clue-probe.json
exiftool -a -G1 -s clue.wav
soxi clue.wav
~~~

| Part | Meaning | What to look for |
|---|---|---|
| `sha256sum --` | Digest exact bytes. The double dash ends option parsing in this GNU command. | A stable identifier across copies. A hash by itself says nothing about the recording's author. |
| `file --` | Identify likely format from content. | Filename and detected format can disagree. A weak or unknown signature calls for a second parser. |
| `ffprobe -v error` | Suppress routine logs while showing errors. | If parsing fails, retain stderr. A quiet invocation can still exit with an error. |
| `-show_format` | List container-level fields such as format, duration and tags. | Container duration may be missing or rounded. |
| `-show_streams` | Describe each media stream and its codec, rate and channel information where available. | Multiple audio streams differ from one stereo stream. Identify the one the question refers to. |
| `-of json` | Choose JSON writer. Bash `>` creates or truncates the output file. | Convenient to read repeatedly offline. Use a fresh filename and inspect output only after a successful exit. |
| `exiftool -a -G1 -s` | Show duplicate tags, include group names, and show concise tag identifiers. | Conflicting repeated tags suggest different metadata namespaces. Corroborate any clue in a tag. |
| `soxi` | Summarize audio properties detected by SoX. | Compare its sample rate, channels and duration with ffprobe. |

A **container** organizes streams, while a **codec** defines how their content is represented. A WAV frequently contains PCM samples, but WAV is a container and may use other encodings. When a tool reports two streams, selecting stream zero doesn't necessarily select left channel. Left and right are channel positions *within* one stream.

### Compare left, right, sum and difference

~~~bash
ffmpeg -hide_banner -n -i clue.wav -map 0:a:0 -af 'pan=mono|c0=c0' -c:a pcm_s16le clue-left.wav
ffmpeg -hide_banner -n -i clue.wav -map 0:a:0 -af 'pan=mono|c0=c1' -c:a pcm_s16le clue-right.wav
ffmpeg -hide_banner -n -i clue.wav -map 0:a:0 -af 'pan=mono|c0=0.5*c0+0.5*c1' -c:a pcm_s16le clue-sum.wav
ffmpeg -hide_banner -n -i clue.wav -map 0:a:0 -af 'pan=mono|c0=0.5*c0-0.5*c1' -c:a pcm_s16le clue-difference.wav
~~~

Run these against a stream with exactly two channels. `-hide_banner` reduces unrelated program info and `-n` refuses to overwrite existing outputs. `-i` introduces the source. `-map 0:a:0` selects the first audio stream in the first input. `-af` supplies the audio filter chain. In `pan`, the output channel on the left of the equals sign receives the source channel expression on the right. `-c:a pcm_s16le` writes 16-bit PCM derivatives. If the original has higher precision, retain it and do not use these derivatives for bit-level claims.

If left is A+B and right is A–B, averaging the two produces A. Half the difference produces B. This gives a concrete prediction: the common part of the stereo image will be weak on the difference track while opposite-polarity content survives. Different microphones, timing shifts and ordinary stereo mixes can also produce a strong difference, so treat it as an observation until you can identify a repeatable signal.

### Reverse speech, isolate a time span and inspect spectrum

~~~bash
ffmpeg -hide_banner -n -i clue-left.wav -af areverse clue-left-reversed.wav
ffmpeg -hide_banner -n -i clue-left.wav -ss 4.25 -t 2.5 clip.wav
sox clip.wav -n spectrogram -x 1200 -y 257 -z 80 -o clip-spectrum.png
~~~

`areverse` reverses the sample sequence and buffers the clip. For long recordings, make a short derivative first and reverse that. `-ss 4.25` after the input selects the extraction start in seconds and `-t 2.5` limits output duration. Record absolute times as **original offset plus derivative time**. Check the resulting duration before mapping back to the original, especially with lossy sources. For SoX, `-n` designates a null audio output. The `spectrogram` effect still writes an image. `-x` controls the image width, `-y` controls vertical bins per channel, `-z` selects displayed dynamic range in dB, and `-o` sets the PNG destination.

In Audacity, switch the track display to Spectrogram, open its spectrogram settings, and compare a linear scale with a log scale. Sweep window sizes in pairs while holding the frequency bounds fixed. At 16 kHz, 1024 samples cover 64 ms and the FFT bins are approximately 15.6 Hz apart. At 2048 samples the window covers 128 ms and bins are about 7.8 Hz apart. This is **bin spacing**, not a guarantee that two frequencies one bin apart will be separable. Windowing, relative signal strength, leakage and in-window modulation affect that result. Increasing window size can sharpen tones while blending short events across a boundary. Use the waveform for pulse timing.

## Full worked drill: two simultaneous tones

~~~bash
sox -n -r 16000 -c 1 -b 16 low.wav synth 1 sine 697 vol 0.25
sox -n -r 16000 -c 1 -b 16 high.wav synth 1 sine 1209 vol 0.25
sox -m low.wav high.wav dual.wav
sox dual.wav -n spectrogram -x 720 -y 257 -o dual.png
sox low.wav -n spectrogram -x 720 -y 257 -o low-control.png
~~~

1. The first two commands synthesize one second each. `-r` selects sample rate, `-c` the channel count and `-b` bits per sample on these outputs. `synth 1 sine 697` selects duration, waveform and frequency. `vol 0.25` reduces amplitude before mixing.
2. `-m` mixes inputs simultaneously. Concatenating the two files would produce two successive frequencies, which is the wrong control for DTMF.
3. Compare the two images at the same settings. A steady line near 697 Hz should be visible in both. In the mixed file, look for a concurrent line near 1209 Hz. The approximate reading is enough for an exploratory decision, but record the measurement tolerance.
4. Match the measured pair to a DTMF table. Rows contain 697, 770, 852 and 941 Hz, and the first three columns contain 1209, 1336 and 1477 Hz. The first row and first column map to digit 1. A fourth 1633 Hz column belongs to A–D on extended keypads.
5. Design a negative control: analyze the one-tone file with the identical settings. A harmonic close to an expected value isn't sufficient. Check that both fundamentals coexist and that the observation is repeatable.
6. Transfer the reasoning to an unknown clip with bursts. Mark the start, center and end of each stable region. Measure near the center so transients or gaps don't occupy most of the analysis window. Record uncertainty for segments too short to distinguish.

### Distinguish Morse timing from DTMF

A repeated duration ratio is a stronger indicator of Morse than the mere presence of beeps. Mark onsets and offsets for several pulses. Estimate a basic unit from short pulses, then compare longer pulses and pauses to it. Standard Morse uses one unit for a dot, three for a dash, one between elements of a character, three between characters and seven between words. Real recordings may have drift or noise. Infer timing groups across the whole recording and then compare candidate text to a reference table. If most decoded letters require changing the criterion from one region to the next, lower confidence.

DTMF uses a low and high tone at the same time. A spectrogram might show pulses like Morse, but each pulse can have a different frequency pair. Look for the choice among rows and columns rather than primarily the pulse duration. If the spectrum shows one changing carrier with regular symbol times, treat modulation as a third explanation and report the actually observed signal characteristics before selecting a decoder.

| Low tone / high tone | 1209 Hz | 1336 Hz | 1477 Hz | 1633 Hz |
|---|---|---|---|---|
| 697 Hz | 1 | 2 | 3 | A |
| 770 Hz | 4 | 5 | 6 | B |
| 852 Hz | 7 | 8 | 9 | C |
| 941 Hz | * | 0 | # | D |

Read the table only after you have measurements. For example, a window centered on 0.4 seconds contains peaks near 770 and 1477 Hz. Check the neighboring windows at the same settings. If both peaks coexist over the stable interval, the table predicts 6. If the low peak falls outside the interval, pairing the two could combine different symbols. Mark that interval unresolved until you have better timing evidence. This matters more in a noisy sample than the absolute precision of a single displayed peak.

### Check more than one time scale

Use the entire recording for orientation, a short segment for classification, and a narrow band for measurement. On a 90-second clip, the full-width spectrogram can make a 100 ms event thinner than a pixel. Trimming a copy helps the display, but keep the offset so other analysts can locate it. Conversely, a tiny crop can make a continuous tone look like a standalone signal by hiding adjacent context. Replay the reported interval with a little extra time on both sides to check that your boundaries match the original.

Keep separate notes for observation and interpretation. “Two bands overlap from 4.31 to 4.46 seconds” describes what a teammate can reproduce. “The sender encoded six” adds a hypothesis about the intended coding scheme. The table and consistency across adjacent symbols support that hypothesis. A negative control guards against ordinary harmonic structure or an accidental pair. Moving from the first claim to the second requires both checks.

## Offline lab: stereo cancellation and pulse timing

The [fixture generator](../labs/make_audio_fixtures.py) needs Python 3.10 or newer and uses only the standard library. From the field-guide directory, run:

~~~bash
python3 labs/make_audio_fixtures.py --help
python3 labs/make_audio_fixtures.py audio-lab
ffprobe -v error -select_streams a:0 \
  -show_entries stream=sample_rate,channels,duration \
  -of default=noprint_wrappers=1 audio-lab/stereo-phase.wav
~~~

The positional argument is a new directory in which the generator creates four WAV files. A second invocation with the same path fails before replacing them. In the probe, `-select_streams a:0` selects the first audio stream, `-show_entries` restricts output to the listed stream fields, and `-of default=noprint_wrappers=1` removes surrounding section markers. Expect one stereo stream, two channels, a 16,000 Hz rate and roughly one second of duration.

**Pair versus harmonic.** Open `tone-pair.wav` and `tone-control.wav` with the same spectrogram settings. Before looking, predict which frequency appears only in one file. Inspect the central part, away from file boundaries. The pair has components at 697 and 1209 Hz. The control has only the 697 Hz fundamental. Dividing 1209 by 697 gives approximately 1.73, so the second component is not an integer multiple of the first. That evidence supports the two-fundamental explanation. The earlier SoX example and this independent generator give you two ways to create a comparable control.

**Stereo phase branch.** In `stereo-phase.wav`, both original channels contain 440 Hz and 1209 Hz. Use the earlier FFmpeg channel recipes with the lab path as input. The half-sum retains 440 Hz and cancels 1209 Hz. The half-difference retains 1209 Hz and cancels 440 Hz. Open the two derivative spectrograms side by side using the same frequency limits. If both look equivalent, check that you mapped the correct stream, used a minus sign in the difference expression, and opened separate output files. Do not infer opposite polarity from the existence of a stereo difference alone. Here you can prove it because the fixture specifies the input relation.

**Timing branch.** Open `timing-message.wav` in waveform view and label runs of audible signal. Measure central pulse and gap stretches against the horizontal time ruler. There are nine pulses. The shortest pulse and internal gaps are about 100 ms, the long pulses and gaps between characters are about 300 ms. Group by gaps before mapping the dots and dashes. The decoded result is **SOS**. Now check the spectrogram so you can explain why this isn't the same as the dual-tone drill: pitch is nearly constant across pulses, while duration changes systematically.

**Transfer and failure test.** Give a teammate just the WAVs with neutral filenames and ask them to classify each as timing, single tone, simultaneous tones, or phase structure. They should include two supporting observations per file. Then offer a sum-only copy of the stereo fixture. A defensible conclusion from that copy is that 440 Hz is visible. It cannot establish that the 1209 Hz component never existed before summing. This is the same evidence problem as a filtered packet capture: what the saved representation omitted may be unrecoverable.

## Image branch

~~~bash
file clue.png
exiftool -a -G1 -s clue.png
xxd -l 32 clue.png
~~~

Open the image at original resolution on a copy. In GIMP, inspect the Channels view. Color values may have different contrast in red, green and blue. An alpha channel can hide pixels in ordinary compositing, so inspect transparency separately and compare against contrasting backgrounds. Keep the original alongside any level-adjusted version. An outlined letter created only by aggressive contrast adjustment may be an artifact, especially in a lossy image. Record the region, channel and adjustment, then ask someone to reproduce it.

If there is a metadata hint, determine whether it describes a transform, a time or a possible string. Compare it to pixel evidence. If the filename says PNG but the signature doesn't match, treat the signature as a clue and use a second format parser rather than converting in place. If the clue is in an animation, inspect frame timing and multiple frames instead of a single thumbnail.

## Troubleshooting and stop conditions

| Symptom | Likely explanations | Discriminating test and next action |
|---|---|---|
| FFmpeg reports invalid data | Wrong type, truncated source, or unsupported codec | Compare file signature and size with expected artifact. Test your parser against a known-good clip. |
| Right channel command fails | Input is mono or selected a different audio stream | Confirm with ffprobe. Apply mono inspection or select the intended audio stream. |
| Spectrogram looks nearly black | Wrong band, small sample amplitude, or insufficient visual range | Compare the same settings on the control. Change one setting and document the effect. |
| Spectrogram looks uniformly bright | Dynamic range or gain hides structure | Reset gain and tighten the display range in steps. Use unchanged data for the comparison. |
| Two tone readings shift with window size | Short burst, leakage, or overlapping tones | Compare center windows, record the uncertainty, and infer symbols only when multiple bursts agree. |
| Alleged hidden speech has too many interpretations | Noise or confirmation bias | Ask a teammate to transcribe without seeing your guess, compare the same interval, and record uncertainty. |
| Result appears after conversion only | Downmixing, resampling, interpolation or rounding created an artifact | Repeat with preserved sample rate and channels and use an independent viewer. |
| Audio duration differs across tools | Container estimate, decoder padding or malformed metadata | Record both estimates and compare decoded sample count on a preserved derivative. |
| Colors differ across viewers | Color profiles, alpha compositing or viewer scaling | Identify the actual channel values on original pixels and record the viewer configuration. |

Hand off when every proposed interpretation requires another unmotivated transformation. Include family of clue, exact input hash, tested region, commands, versions, the control result and the unanswered question. A flag-looking string is a lead. The standard of evidence is whether someone else can reproduce it and explain how it appeared.

## Glossary and mastery checks

| Term | Meaning |
|---|---|
| Sample rate | Samples per second per channel. With 16 kHz sampling, the Nyquist frequency is 8 kHz. |
| Bit depth | Precision for representing PCM amplitude. It does not determine sample timing. |
| Waveform | Sample amplitude over time. Best first view for onsets, offsets and relative timing. |
| Spectrogram | Energy by frequency over time. Useful for slowly changing tones and structures across bands. |
| FFT window | Short region used for one frequency estimate. Longer windows change frequency and temporal resolution. |
| Leakage | Energy spread into nearby frequency bins when a finite window doesn't align with a tone. |
| Phase cancellation | Opposite-polarity signals cancel when combined. |
| Harmonic | A component near an integer multiple of a fundamental frequency. |
| DTMF | Symbols represented by simultaneous low and high tones. |
| Alpha channel | Opacity channel describing how a pixel composites over another layer. |
| Negative control | Sample expected to lack the feature. Used to identify false positives from the analysis itself. |

- Predict what half-sum and half-difference produce if the input channels are identical, then if one is inverted.
- Explain why shortening a window can make pulse boundaries clearer even when tone identification gets worse.
- Sketch a handoff that would distinguish a real two-tone clue from a single tone with harmonics.
- Repeat with a new clip and ask a teammate to reproduce your finding from the original file and notes alone.

[FFprobe reference](https://ffmpeg.org/ffprobe.html) · [FFmpeg audio filters](https://ffmpeg.org/ffmpeg-filters.html) · [Field guide index](../README.md)
