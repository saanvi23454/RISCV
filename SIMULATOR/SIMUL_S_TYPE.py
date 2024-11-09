def S_TYPE( line ):
  # line is 32 bits

  global PC
  global register
  global memory

  imm = line[0:7] + line[20:25]
  rs2 = line[7:12]
  rs1 = line[12:17]
  funct3 = line[17:20]
  opcode = line[25:32]

  #sw
  memory[add_bin(register[rs1], imm)] = register[rs2]
  PC += 4
    
