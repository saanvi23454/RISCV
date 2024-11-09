functions_utype = {"lui":"0110111",
                   "auipc":"0010111"}

def U_TYPE(U_instruction):
  
    ''' 
    U_instruction is a list of string in format :
    [(Name of u_type function),(destination register),(value of the immediate)]

    returns : Above provided U_instrution into 32 bit binary format in a string
    '''
  
    imm = (sext(int(U_instruction[2]),32))[:20]
    if (imm == "e1"):
      return imm
      
    reg = reg_ENCODE.get(U_instruction[1])
    if (reg == None):
      return "e3"
    op_c= functions_utype[U_instruction[0]]

    return  imm+reg+op_c
