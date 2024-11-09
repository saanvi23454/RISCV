# B-TYPE INSTRUCTIONS
map_B_TYPE = { "beq" : ["1100011", "000"] , 
              "bne" : ["1100011", "001"] , 
              "blt" : ["1100011", "100"] , 
              "bge" : ["1100011", "101"] , 
              "bltu" : ["1100011", "110"] , 
              "bgeu" : ["1100011", "111"] }

def B_TYPE( B_instruction ):
  """
  B_instruction is a list of the form [[opcode, funct3], rs1, rs2, immediate value not converted in bits]
  """
  try:
    B_instruction[3] = int(B_instruction[3])
  except:
    label = label_dict.get(B_instruction[3])
    if (label == None):
       return "e10"
    B_instruction[3] = ((label-(PC))*4)
  imm = sext(int(B_instruction[3]),12)
  if (imm == "e1"):
      return imm
    
  rs1 = reg_ENCODE.get(B_instruction[1])
  rs2 = reg_ENCODE.get(B_instruction[2])

  if (rs1 == None) or (rs2 == None):
    return "e3"
  
  funct3 = map_B_TYPE[B_instruction[0]][1]
  opc = map_B_TYPE[B_instruction[0]][0]
  
  decoded = imm[0:7] + rs2 + rs1 + funct3 + imm[7:11] + imm[0] + opc
  return decoded
  
########################################################################################
