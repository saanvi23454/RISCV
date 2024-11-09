### FOR SIMULATOR PURPOSE ONLY #############

# HALT
# opcode 0000110
#let all other bits be filler 0
halt = '00000000000000000000000000000110'

# simply have to write in while loop, if line == halt, break. No need for function

#####################

# rvrs_opcode = '0000111'

def rvrs( line ):

  global PC
  global memory
  global register
  
  # syntax : '000000000000' + rs1 + '000' + rd + '0000111'

  rs1 = line[12:17]
  rd = [20:25]

  register[rd] = register[rs1][::-1]

  PC += 4

  ####################################################

####### FOR ASSEMBLER PURPOSE ONLY ###############



  
  
