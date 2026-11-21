# Static binary analysis and native-code review

Start with a concrete question: what inputs and decisions explain the behavior? Static analysis reads bytes, headers and instructions. Dynamic observation runs a program and measures what happens. Use both on a toy binary you compile. Keep suspicious downloaded files to static inspection in an isolated analysis VM. The purpose here is code comprehension, reproduction of benign behavior, and verification of bounds and parsing fixes.

## Triage and decision tree

~~~mermaid
flowchart TD
    A["Record the question and preserve input"] --> Q0
    Q0{"Does file identify ELF or another known format"} -- Yes --> Y0["Record architecture and file class"]
    Q0 -- No --> Q1
    Y0 --> V["Verify against control and record evidence"]
    Q1{"Does the symbol table expose a named routine"} -- Yes --> Y1["Locate the routine and follow arguments, branches and returns"]
    Q1 -- No --> Q2
    Y1 --> V["Verify against control and record evidence"]
    Q2{"Can you map a comparison to a specific input"} -- Yes --> Y2["Build a truth table with a known toolchain and sample"]
    Q2 -- No --> Q3
    Y2 --> V["Verify against control and record evidence"]
    Q3{"Is the binary a toy you built"} -- Yes --> Y3["Verify by running two known input cases"]
    Q3 -- No --> Q4
    Y3 --> V["Verify against control and record evidence"]
    Q4{"Are length and return checks consistent with the contract"} -- Yes --> Y4["Document normal and malformed test results"]
    Q4 -- No --> N
    Y4 --> V["Verify against control and record evidence"]
    N["Check prerequisites, capture limitations and missing evidence"]
    N --> V
~~~

Offline text equivalent:

1. **Does file identify ELF or another known format** If yes, Record architecture and file class. If no, compare magic bytes and use an appropriate read-only format parser.
2. **Does the symbol table expose a named routine** If yes, Locate the routine and follow arguments, branches and returns. If no, compare string references and import names as leads.
3. **Can you map a comparison to a specific input** If yes, Build a truth table with a known toolchain and sample. If no, check ABI, signedness and optimization.
4. **Is the binary a toy you built** If yes, Verify by running two known input cases. If no, continue with static observations and record limits.
5. **Are length and return checks consistent with the contract** If yes, Document normal and malformed test results. If no, fix the source and rerun regression checks.

## Command recipes

### Inventory before disassembly

Start with the format, then use a reader appropriate to that format. Use the command examples below on Linux ELF files.

~~~bash
file demo
readelf -hW demo
readelf -SW demo
readelf -sW demo
strings -a -n 6 -t x -- demo | head -n 30
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `readelf -hW` | Print ELF header (`-h`) without narrow-line wrapping (`-W`). Inspect Machine, Class and entry point. |
| `-SW` | List ELF section headers with wide output. Sections label groups of file bytes for linking and inspection. |
| `-sW` | List symbols when available. Dynamic imports can remain after local symbols are stripped. |
| `strings -a -n 6 -t x` | Scan entire file for at least six printable characters and report hex file offsets. |
| `head -n 30` | Limit the preview; use a wider read if the relevant string appears later. |

The offset reported by strings is a file offset. A disassembler often displays virtual addresses. Compare section file offset and load address before treating them as the same coordinate. A string in the file need not be reachable.

### Build a controlled program in two modes

Use a clean scratch directory. The C code returns success only when invoked with exactly one user argument.

~~~bash
cat > demo.c <<'EOF'
int main(int argc, char **argv) {
    (void)argv;
    return argc == 2 ? 0 : 1;
}
EOF
gcc -Wall -Wextra -g -O0 demo.c -o demo
gcc -Wall -Wextra -g -O2 demo.c -o demo-fast
objdump -d --disassemble=main demo
objdump -d --disassemble=main demo-fast
./demo example; printf 'status=%s\n' "$?"
./demo; printf 'status=%s\n' "$?"
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `<<'EOF'` | Bash here-document with literal content. Write a new scratch file. |
| `-Wall -Wextra` | Enable useful compiler warnings that may reveal suspicious source constructs. |
| `-g` | Include debugging information. |
| `-O0` / `-O2` | Select minimal versus enabled optimization. Correct behavior should agree. |
| `-o` | Choose the output path. |
| `objdump -d --disassemble=main` | Disassemble code for the named routine when the tool can locate it. |
| `$?` | Status of the immediately preceding command. Read it before running an unrelated command. |

On both builds, one user argument gives exit status 0 and zero gives 1. The program name counts toward argc. On a different CPU or compiler version you will see different instructions. An optimizing compiler might express a condition as a computed result rather than a separate branch.

### Review parsing and memory contracts

Inspect source for how external values become sizes and indexes. Start with the function that accepts numeric input and follow validation to the first data access.

~~~bash
rg -n --glob '*.[ch]' 'strtol|strtoul|memcpy|snprintf|sizeof' .
gcc -Wall -Wextra -Wconversion -fsyntax-only demo.c
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `--glob '*.[ch]'` | Limit to C source and header files. Extend the scope if the project uses other extensions. |
| `-Wconversion` | Ask for warnings around implicit conversions. Treat warnings as leads and review each context. |
| `-fsyntax-only` | Run parsing/type checks without linking. This does not prove runtime correctness. |

Confirm valid range and units before conversion to an unsigned size. For `strtol`, separate no digits (end pointer equals start), trailing characters, numeric overflow, and application range. For copying, compare against actual destination capacity and consider terminators. Write benign regression cases around zero, exact capacity, and one above it. Use a checked implementation, and do not run malformed third-party binaries.

## Worked walkthrough

1. Start with the toy C source and predict the result for no user arguments, one argument, and two arguments. Remember the program name counts.
2. Inspect both ELF headers and confirm the binaries target the same architecture. Compare symbols. Locate main and mark where it receives or checks the input count.
3. Read the unoptimized program's decision and return. Label the conditions in ordinary language before comparing assembly syntax. The low-level instructions are one encoding of the truth table.
4. Inspect the optimized program. If a branch disappears, look for instructions that compute an output based on condition flags. Run both variants with the same examples and compare exit status.
5. Apply the same reasoning to review a fictitious parser that reads a count from text and uses it for bounds. Decide which malformed inputs should be rejected and which maximum should pass. Prove the rejection happens before allocation or copying by tracing the return path.
6. Produce a conclusion that mentions compiler options, architecture, artifact hash, input and observed result. When an important property is inferred, state the assumptions needed to reach it.

## Troubleshooting and verification

| Symptom | Likely explanations | Discriminating test and action |
|---|---|---|
| No main symbol | Stripped program, unsupported format or different entry structure | Confirm format. On owned code, compare a separate debug build. |
| Disassembler prints no instructions | Selection wrong, symbol missing or architecture unsupported | Check header and sections first, then verify tool version supports the target. |
| Optimized output differs visually | Code was inlined or conditional result computed without a branch | Compare observable behavior and avoid assuming one source line means one instruction. |
| Return value is different than predicted | Confused argc with number of user arguments or read wrong shell status | Make a 0/1/2 input truth table and capture status immediately. |
| Bounds look correct but units differ | Bytes, elements and characters conflated | Annotate each operand's unit and type; compare against real destination capacity. |
| Printed string seems decisive | String may be unreachable or unused | Look for references and confirm the path on an owned example. |

## Glossary

| Term | Meaning and use |
|---|---|
| ELF | Linux executable and object format containing headers, sections and sometimes symbols. |
| ABI | Conventions between compiled code and runtime, including argument passing. |
| File offset | Position measured from start of the file. |
| Virtual address | Position in a process address space at runtime or a linked address shown by tools. |
| Symbol | Name for a function or object. Names can be removed from a distribution build. |
| Control flow | How execution moves between instructions, calls and decisions. |
| Data flow | How an input changes and reaches an output or operation. |
| Signedness | Whether bit patterns represent negative values. It influences comparisons and conversions. |
| Array capacity | Storage available in elements or bytes. The correct check needs consistent units. |

## Practice, transfer and handoff

- Try the toy on another architecture and explain which truth-table facts remain stable despite different assembly.
- Choose a parsing change that prevents a bad conversion and show one normal and one rejected case.
- Provide a static handoff with routine, offsets, assumptions and a controlled verification case.

[GNU Binutils documentation](https://sourceware.org/binutils/docs/) · [GCC warning options](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html)

[Chapter index](README.md)
