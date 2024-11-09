<h2>About the Project</h2>
We created a custom assembler and a custom simulator to implement a subset of RV32I (RISC-V 32-bit integer) instruction set. RISCV, an open-source, load-store type ISA, is increasingly used for open-source hardware development. We verified its correctness through an automated testing infrastructure using multiple test cases.<br><br>

Step 1) <br> 
  -> Designed an Assembler which translate a .txt file code written in assembly language to a machine code(binary code) and saves it into a .txt file<br>
  -> Used Python language to code the assembler<br>
  -> Accounted for several possible errors that could be encountered on custom user inputs<br><br>
  
Step 2)<br>
  -> Designed a Simulator which executes the instructions of the input machine code, and prints the value stored in all register and memory locations after each execution.<br>
  -> Used Python language to code the simulator<br>
  -> Assumption : syntactical errors, accessing non-existent memory or register locations, etc., taken care of by the assembler. Hence, minimal error checking in this step.<br><br>

Additionally, we created a few added instructions which weren't part of the original ISA subset to increase the functionality and convenience of our assembler-simulator.

<h2>Adding Code</h2>
Add the assembler code in the Simple-Assembler directory. Add the commands to execute the assembler in Simple-Assembler/run.<br>
Add the simulator code in the SimpleSimulator directory. Add the commands to execute the assembler in SimpleSimulator/run.<br>
Make sure that both the assembler and the simulator read from stdin.<br>
Make sure that both the assembler and the simulator write to stdout.<br>
<h2>How to Evaluate</h2>
Go to the automatedTesting directory and execute the run file with appropiate options passed as arguments.<br>
Options available for automated testing:<br>
--verbose: Prints verbose output<br>
--no-asm: Does not evaluate the assembler<br>
--no-sim: Does not evaluate the simulator<br>

