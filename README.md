## About the Project

This project implements a custom assembler and simulator for a subset of the RV32I (RISC-V 32-bit integer) instruction set. RISC-V, an open-source, load-store type ISA, is gaining popularity for open-source hardware development. We verified the correctness of the assembler and simulator through an automated testing infrastructure, running multiple test cases to ensure reliability.

### Step 1: Assembler
- Designed an assembler that translates a `.txt` file containing assembly language code into machine code (binary) and saves it into another `.txt` file.
- Implemented in Python to handle various types of user input and account for common errors.
- Incorporated error handling for common issues, such as invalid instructions and incorrect formats.

### Step 2: Simulator
- Designed a simulator that executes machine code instructions and prints the current values stored in all registers and memory locations after each execution.
- Implemented in Python with minimal error checking, assuming syntactical errors and invalid memory/register accesses are handled by the assembler.
  
### Additional Features
- Added custom instructions beyond the original RV32I subset to improve the functionality and convenience of the assembler and simulator.

## Adding Code

1. **Assembler Code**:
   - Place the assembler code in the `Simple-Assembler` directory.
   - Add the commands to execute the assembler in `Simple-Assembler/run`.

2. **Simulator Code**:
   - Place the simulator code in the `SimpleSimulator` directory.
   - Add the commands to execute the simulator in `SimpleSimulator/run`.

Ensure that both the assembler and simulator:
- Read from `stdin`.
- Write to `stdout`.

## How to Evaluate

1. Navigate to the `automatedTesting` directory.
2. Run the `run` file with appropriate options passed as arguments.

### Available Options:
- `--verbose`: Prints detailed output for debugging.
- `--no-asm`: Skips the assembler evaluation.
- `--no-sim`: Skips the simulator evaluation.
