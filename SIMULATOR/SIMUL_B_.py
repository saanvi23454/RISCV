def B_TYPE( line ):
  # line is 32 bits
  #imm==0?

  global PC
  global register
  global memory

  imm = line[0]+line[24]+line[1:7]+line[20:24]+'0'
  rs1 = line[12:17]
  funct3 = line[17:20]
  rs2 = line[7:12]

  #beq
  if funct3 == '000':
    if (register[rs1] == register[rs2]):
      PC = PC + bin_to_dec(imm)
    else:
      PC += 4

  #bne
  elif funct3 == '001':
    if (register[rs1]!=register[rs2]):
      PC+=bin_to_dec(imm)
    else:
      PC+=4

  #bge
  elif funct3 == '101':
    if (bin_to_dec(register[rs1])>=bin_to_dec(register[rs2])):
      PC+=bin_to_dec(imm)
    else:
      PC+=4

  #bgeu
  elif funct3 == '111':
    if (bin_to_dec(register[rs1], 'U')>=bin_to_dec(register[rs2], 'U')):
      PC+=bin_to_dec(imm)
    else:
      PC+=4

  #blt
  elif funct3 == '100':
    if (bin_to_dec(register[rs1])<bin_to_dec(register[rs2])):
      PC+=bin_to_dec(imm)
    else:
      PC+=4

  #bltu
  elif funct3 == '110':
    if (bin_to_dec(register[rs1], 'U')<bin_to_dec(register[rs2], 'U')):
      PC+=bin_to_dec(imm)
    else:
      PC+=4

  else:
    #error
