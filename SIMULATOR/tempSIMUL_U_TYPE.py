def U_TYPE( line ):
  #line is 32 bits
  global PC
  global register 
  global memory
  
  imm = line[0:20]
  rd = line[20:25]
  opcode =line[25:32]

  if (opcode == "0110111"):
    register[rd] = sext(bin_to_dec(imm),32)

  elif (opcode == "0010111"):
    register[rd] = sext(PC + bin_to_dec(imm), 32)

  PC += 4
