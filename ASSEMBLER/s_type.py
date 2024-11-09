# s{b|h|w|d}

map_S_TYPE = {"sw" :     ["0100011","010"] }   

def S_TYPE( S_instruction ):
  '''argument : list type, instruction
  returns : string of encoded binary
  '''
  imm = sext(int(S_instruction[2]),12)
  rt = reg_ENCODE.get(S_instruction[3])
  rd = reg_ENCODE.get(S_instruction[1])

  if (imm == "e1"):
    return imm
    
  if (rt == None) or (rd == None):
    return "e3"
    
  funct = map_S_TYPE[S_instruction[0]][1]
  opc = map_S_TYPE[S_instruction[0]][0]
  
  encoded = imm[0:7] + rd + rt + funct + imm[7:] + opc
  return encoded
