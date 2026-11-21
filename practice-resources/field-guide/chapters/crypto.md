# Encodings, cryptography and reliable scripting

Begin with the bytes. Humans give an input labels such as ciphertext, token, hex or corrupt text, but the label is a hypothesis until the format and transformations support it. Encoding changes representation, hashing produces a digest, compression reduces redundancy, and encryption uses a key to protect plaintext. Multiple kinds of transformation can be layered. Decode only when the source structure or a clue supports the choice. Commands below use Bash, GNU tools and Python's standard library.

## Triage and decision tree

~~~mermaid
flowchart TD
    A["Record the question and preserve input"] --> Q0
    Q0{"Is the input a human-readable alphabet with clear framing"} -- Yes --> Y0["Check hex or Base64 syntax and try a reversible transformation"]
    Q0 -- No --> Q1
    Y0 --> V["Verify against control and record evidence"]
    Q1{"Does decoded output match expected structure"} -- Yes --> Y1["Round trip while accounting for normalization"]
    Q1 -- No --> Q2
    Y1 --> V["Verify against control and record evidence"]
    Q2{"Does the format specify encryption and authenticated metadata"} -- Yes --> Y2["Identify algorithm, key availability, nonce and tag without guessing missing data"]
    Q2 -- No --> Q3
    Y2 --> V["Verify against control and record evidence"]
    Q3{"Do you need to repeat a transformation over many records"} -- Yes --> Y3["Use a strict offline parser with explicit failure behavior"]
    Q3 -- No --> Q4
    Y3 --> V["Verify against control and record evidence"]
    Q4{"Can a second parser or known test vector confirm it"} -- Yes --> Y4["Report bytes, transformation and result"]
    Q4 -- No --> N
    Y4 --> V["Verify against control and record evidence"]
    N["Check prerequisites, capture limitations and missing evidence"]
    N --> V
~~~

Offline text equivalent:

1. **Is the input a human-readable alphabet with clear framing** If yes, Check hex or Base64 syntax and try a reversible transformation. If no, capture the first bytes and ask whether there is a known binary structure.
2. **Does decoded output match expected structure** If yes, Round trip while accounting for normalization. If no, check the decoder status and try a known-good control.
3. **Does the format specify encryption and authenticated metadata** If yes, Identify algorithm, key availability, nonce and tag without guessing missing data. If no, distinguish digest, compression and encoded binary.
4. **Do you need to repeat a transformation over many records** If yes, Use a strict offline parser with explicit failure behavior. If no, record the exact one-off command and result.
5. **Can a second parser or known test vector confirm it** If yes, Report bytes, transformation and result. If no, report a candidate interpretation with its limits.

## Run the decision tree at the terminal

~~~mermaid
flowchart TD
    Entry["Enter at the first applicable node"] --> Step1
    Step1["1. file -- token.txt"] --> Result1{"Check whether the transformation fits"}
    Result1 -->|Looks like standard Base64| Step2
    Result1 -->|binary or container| Step3
    Result1 -->|unsure| End1_2["1. Follow the matching result below"]
    Step2["2. base64 -d token.txt &gt; decoded.bin"] --> Result2{"Decode and verify full success"}
    Result2 -->|Zero exit and meaningful bytes| End2_0["2. Follow the matching result below"]
    Result2 -->|nonzero exit| Step4
    Result2 -->|binary output| Step3
    Step3["3. file -- mystery.bin"] --> Result3{"Test a claimed file type instead of inferring crypto"}
    Result3 -->|Positive parser result| End3_0["3. Follow the matching result below"]
    Result3 -->|test fails| End3_1["3. Follow the matching result below"]
    Result3 -->|explicit AEAD data| End3_2["3. Follow the matching result below"]
    Step4["4. python3 decode_token.py --help"] --> Result4{"Run the strict decoder against known and malformed controls"}
    Result4 -->|Valid case prints `68656c6c6f`, invalid exits 2| End4_0["4. Follow the matching result below"]
    Result4 -->|unexpected success on malformed input| End4_1["4. Follow the matching result below"]
    Result4 -->|byte output is non-text| End4_2["4. Follow the matching result below"]
~~~


Start at **1**. Each node gives the exact check, the options that affect the result, and where to go for each outcome. Filenames are placeholders for your local working copies. **Record** means save the observation and its evidence locator. **Hand off** means keep the last confirmed result and state what is missing.

### 1 · Check whether the transformation fits

~~~bash
file -- token.txt
xxd -g 1 -l 48 token.txt
~~~

**Options and interpretation.** `--` ends file options; `-g 1` groups bytes, `-l 48` bounds preview.

- **Looks like standard Base64.** **2**
- **binary or container.** **3**
- **unsure.** record expected syntax, length and source format first.

### 2 · Decode and verify full success

~~~bash
base64 -d token.txt > decoded.bin
printf 'status=%s\n' "$?"
xxd -g 1 decoded.bin
base64 -w 0 decoded.bin; printf '\n'
~~~

**Options and interpretation.** `-d` decodes; GNU `-w 0` emits unwrapped output. `>` can leave partial bytes after an error.

- **Zero exit and meaningful bytes.** compare canonical re-encoding
- **nonzero exit.** discard partial interpretation and use **4**
- **binary output.** **3**.

### 3 · Test a claimed file type instead of inferring crypto

~~~bash
file -- mystery.bin
gzip -t known-gzip.gz
sha256sum -- mystery.bin
~~~

**Options and interpretation.** `gzip -t` checks integrity of an expected gzip file without extracting it. A hash corroborates identity, not algorithm classification.

- **Positive parser result.** record structural evidence
- **test fails.** check parser/format and control, not a conclusion of encryption
- **explicit AEAD data.** inventory algorithm, nonce, tag and associated data.

### 4 · Run the strict decoder against known and malformed controls

~~~bash
python3 decode_token.py --help
python3 decode_token.py 'aGVsbG8='
python3 decode_token.py 'aGVsbG8=!'
printf 'status=%s\n' "$?"
~~~

**Options and interpretation.** Create `decode_token.py` from the chapter recipe. `--help` lists positional arguments; the script uses strict validation and canonical re-encoding.

- **Valid case prints `68656c6c6f`, invalid exits 2.** compare with field input
- **unexpected success on malformed input.** inspect exact arguments and script version
- **byte output is non-text.** inspect format, not automatic UTF-8.

## Command recipes

### Inspect and decode deliberately

Use known sample text. Preserve the byte sequence before displaying it as characters.

~~~bash
printf '%s' 'aGVsbG8=' > token.txt
base64 -d token.txt > decoded.bin
xxd -g 1 decoded.bin
base64 -w 0 decoded.bin; printf '\n'
printf '%s' '68656c6c6f' | xxd -r -p | xxd -g 1
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `printf '%s'` | Write the input without inventing a trailing newline or interpreting it as a format. |
| `base64 -d` | Decode Base64. Check the command status because partial output can exist after malformed input. |
| `base64 -w 0` | On GNU Coreutils, disable line wrapping. Padding and wrapping conventions vary by format. |
| `xxd -g 1` | Group hexadecimal display by individual bytes. |
| `xxd -r -p` | Reverse a plain hex dump. For strict validation use a parser that rejects malformed input rather than ignoring extraneous text. |

Expected bytes are 68 65 6c 6c 6f. If they match `hello` exactly, the transformation is reproducible. Whether that plaintext answers the challenge depends on the question and its provenance.

### Teach a parser to fail visibly

In a scratch directory, create the strict example below. It accepts one standard Base64 token and rejects accidental trailing text and noncanonical encodings.

~~~bash
cat > decode_token.py <<'PY'
import argparse
import base64
import binascii

parser = argparse.ArgumentParser(description='Decode one canonical Base64 token')
parser.add_argument('token')
args = parser.parse_args()
try:
    decoded = base64.b64decode(args.token, validate=True)
except (ValueError, binascii.Error) as exc:
    parser.error(str(exc))
if base64.b64encode(decoded).decode('ascii') != args.token:
    parser.error('noncanonical Base64')
print(decoded.hex())
PY
python3 decode_token.py --help
python3 decode_token.py 'aGVsbG8='
python3 decode_token.py 'aGVsbG8=!'
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `--help` | Show parser usage without interpreting a token. |
| `validate=True` | Reject characters and padding forms that fail Python's strict syntax checks. Re-encoding adds this example's canonicality rule. |
| `parser.error` | Write a usage/error message and exit with status 2. |
| `.hex()` | Display decoded bytes without assuming text or printing arbitrary control characters. |

Canonical Base64 is a chosen requirement of this particular exercise. A format allowing alternate alphabets or omitted padding needs its own explicit specification. Avoid automatic guessing across alphabets in a script that will be used for evidentiary conclusions.

### Check for a plausible container or digest

Compression, encryption and arbitrary binary may all look random in a small window. Use a format-specific test before inferring one.

~~~bash
file mystery.bin
xxd -g 1 -l 48 mystery.bin
sha256sum -- mystery.bin
gzip -t known-gzip.gz
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `file` | Use format signatures and other heuristics. Output is a lead. |
| `xxd -l 48` | Limit inspection to the first 48 input bytes. |
| `sha256sum --` | Return a hash to compare against a trusted digest. The hash cannot be decoded into the original file. |
| `gzip -t` | Check gzip integrity without writing a decompressed output file. Only use on an appropriate local sample. |

A valid gzip test corroborates gzip structure for the supplied file. A failed one does not establish encryption. Inspect the provenance and claimed format. For an authenticated ciphertext ask which associated data, nonce and tag are expected. An authentication failure means you lack a verified plaintext for that attempt.

## Worked walkthrough

1. Read the expected result first. Decide whether the output should be a human string, a file header or a structured record. Write down the claimed transform before you inspect the sample.
2. Run the positive control for `hello` and check byte-for-byte equality and canonical round trip. Then run the appended-exclamation control and check that exit status is 2. A non-strict decoder might ignore it.
3. Make two plausible explanations for a blob that shows random-looking data: it may be compressed or encrypted. A known gzip fixture provides an example of compression. High entropy is compatible with both hypotheses and can't distinguish them alone.
4. Sketch a fictional authenticated-encryption record with fields `algorithm`, `nonce`, `ciphertext`, `tag` and `associated_data`. Explain why reusing a nonce can be unsafe under typical schemes and why a ciphertext without its tag is missing evidence for verification. Record exactly which fields were supplied before drawing a conclusion.
5. Use controlled variants for any automation: empty input, one valid token, embedded whitespace, a trailing invalid character, and output that is valid bytes but invalid UTF-8. Treat decoding bytes and interpreting them as text as separate operations.
6. Explain the final output in terms of exact input bytes, decoder settings, interpretation, and a second check. Preserve the original token for comparison rather than pasting only the readable output.

## Troubleshooting and verification

| Symptom | Likely explanations | Discriminating test and action |
|---|---|---|
| Decoded data appears empty | Wrong input file, silent partial output or legitimate empty token | Check source and destination byte counts, parser status and format requirements. |
| Round trip differs | Different padding/wrapping rules or unexpected normalization | Compare byte-level originals and canonical output; record the difference. |
| Readable partial output, nonzero status | An invalid suffix stopped decoding partway through | Do not accept partial bytes as a clean decode. Inspect diagnostic and use a strict parser. |
| Unicode decode error | The bytes may be binary, damaged or another charset | Use hex and format parser output before selecting a character encoding. |
| Authenticity check fails | Different parameters, key, altered input or missing associated data | Confirm the original specification and parameters. Preserve the failure result. |
| Digest length matches several named algorithms | Too little evidence to classify a digest | Look for source metadata rather than treating character count as identification. |

## Glossary

| Term | Meaning and use |
|---|---|
| Encoding | Reversible representation of bytes without a secret key. |
| Charset | Mapping between characters and bytes. UTF-8 is one example. |
| Ciphertext | Output of encryption, interpreted with the relevant protocol and parameters. |
| Nonce | Number or value used once as required by a particular scheme. Typically not confidential. |
| Authentication tag | Value checked to verify integrity and authenticity given the correct key and context. |
| Associated data | Context that is authenticated without necessarily being encrypted. |
| Digest | Fixed-size output of a hash function, used to compare known candidate data. |
| Canonical form | A chosen unique representation for a logical value. |
| Entropy | A statistical property of a distribution. Random-looking bytes alone do not identify a scheme. |

## Practice, transfer and handoff

- Write a fixture where permissive and strict decoders give different outcomes. Record why the source format decides which is correct.
- Compare a literal byte newline with the two printable characters backslash and n. Which layer should interpret them?
- Handoff with input location and hash, variant, exact flags, exit status and independent control.

[Python argparse](https://docs.python.org/3/library/argparse.html) · [Python Base64 reference](https://docs.python.org/3/library/base64.html)

[Chapter index](README.md)
