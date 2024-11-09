def I_TYPE( line ):
  # line is 32 bits
  # STORE 32 bits in 1 register

  global PC
  global register
  global memory

  imm = line[0:12]
  rs1 = line[12:17]
  funct3 = line[17:20]
  rd = line[20:25]
  opcode = line[25:32]

  #lw
  if opcode == '0000011':
  #rd = mem(rs1 + sext(imm[11:0]))
    register[rd] = memory(add_bin(register[rs1], imm))
    PC += 4

  #addi
  if opcode == '0010011':
    if funct3 == '000':
      register[rd] = bin_add(register[rs],imm)

  #sltiu
    elif funct3 == '011':
      #rd = 1. If unsigned(rs) < unsigned(imm)
      if bin_to_dec(register[rs],'u') < bin_to_dec(bin_to_dec(imm),'u') :
        register[rd] = sext(1 ,32)   
    PC +=4

  #jalr
  
  if opcode == '1100111':
      register[rd] = sext((PC+4),32)
      tempPC = add_bin(register[rs], imm)
      tempPC = tempPC[:-1] + '0'
      PC = bin_to_dec(tempPC,'u')


    
    
