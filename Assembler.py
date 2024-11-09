import re

#register mapping
reg_ENCODE  = {'zero': '00000',   'ra': '00001',     'sp': '00010',     'gp': '00011', 
               'tp': '00100',     't0': '00101',     't1': '00110',     't2': '00111', 
               's0': '01000',     'fp': '01000',     's1': '01001',     'a0': '01010',     'a1': '01011', 
               'a2': '01100',     'a3': '01101',     'a4': '01110',     'a5': '01111', 
               'a6': '10000',     'a7': '10001',     's2': '10010',     's3': '10011', 
               's4': '10100',     's5': '10101',     's6': '10110',     's7': '10111', 
               's8': '11000',     's9': '11001',     's10': '11010',    's11': '11011', 
               't3': '11100',     't4': '11101',     't5': '11110',     't6': '11111'}

#instruction mapping
instruction_mapping = {"r_type": {"add", "sub", "sll", 
                                  "slt", "sltu", "xor", 
                                  "srl", "or", "and"}, 
                       "i_type": {"lw", "addi", "sltiu", 'jalr'}, 
                       "s_type": {"sw"}, 
                       "b_type": {"beq", "bne", "blt", 
                                   "bge", "bltu", "bgeu"}, 
                       "u_type": {"lui", "auipc"}, 
                       "j_type": {"jal"}
                       }

#error mapping
errorMAPPING = {"e1": "Error: overflow detected in immediate value" ,
                "e2": "Error: invalid opcode",
                "e3": "Error: invalid register name",
                "e4": "Error: maximum(1000) loop calls reached",
                "e5": "Error: invalid label name",
                "e6": "Error: Virtual Halt missing after last instruction",
                "e7": "Error: Virtual Halt encountered before remaining instructions", 
                "e8": "Error: Address given in label is out of bounds",
                "e9": "Error: Label name not unique",
               "e10": "Error: Label given is not present",
               "e11": "Error: Virtual Halt missing" }                
              
def errorGEN ( errorNUM, lineNUM ):
  errorMSG = errorMAPPING[errorNUM] + " at Line " + f'{lineNUM + 1}'  # 0 PC implies line 1 !!!
  return errorMSG

########################################################################################

#function for sign extension
def sext(number, bits):
  # ONLY USE IT TO SIGN EXTEND AN IMMEDIATE VALUE
    """
    This function first converts the number into binary
    and then extends its bits to the required amount
    """
    number = int(number)
    if ( ( number < -(2**(bits-1)) ) or ( number > (2**(bits-1))-1 ) ):
        return "e1"
      
    if (number<0):
        sign = -1
        number = -number
      
    else:
        sign = 1
    binary = ""
  
    while (number>0):
        binary += f"{number%2}"
        number = number//2
    binary = binary[::-1]
    binary = ('0'*(bits-len(binary)))+binary
  
    if (sign == -1):
        flag=False
        twosComplement = ""
      
        for i in range(len(binary)-1, -1, -1):
            if (flag):
                if binary[i]=='1':
                    twosComplement+='0'
                else:
                    twosComplement+='1'
                continue
              
            twosComplement+=binary[i]
            if (binary[i]=='1'):
                flag = True 
              
        binary = twosComplement[::-1]
    return binary

########################################################################################
# R-TYPE INSTRUCTIONS
functions_r = {"add": ["0000000", "000"],                #operation: [funct7, funct3]
             "sub": ["0100000", "000"], 
             "sll": ["0000000", "001"], 
             "slt": ["0000000", "010"], 
             "sltu": ["0000000", "011"], 
             "xor": ["0000000", "100"], 
             "srl": ["0000000", "101"], 
             "or": ["0000000", "110"],
             "and": ["0000000", "111"]
             }

def R_TYPE(instruction_list):
    operation = instruction_list[0]
    reg1 = reg_ENCODE.get(instruction_list[1])
    reg2 = reg_ENCODE.get(instruction_list[2])
    reg3 = reg_ENCODE.get(instruction_list[3])

    if (reg1 == None) or (reg2 == None) or (reg3 == None):
      return "e3"
      
    output = functions_r[operation][0] + reg3 + reg2 + functions_r[operation][1] + reg1 + "0110011"
    return output 

########################################################################################

# I-TYPE INSTRUCTIONS
map_I_TYPE = {"addi" :   ["0010011", "000"] , 
              "sltiu" :  ["0010011", "011"] , 
              "jalr" :   ["1100111", "000"] , 
              "lw" :     ["0000011","010"] } 

def I_TYPE( I_instruction ):
    '''argument : list type, instruction
    returns : string of encoded binary
    '''
    rd = reg_ENCODE.get(I_instruction[1])
    
    if (I_instruction[0] not in {"lw", "jalr"}):
        imm = sext(int(I_instruction[3]),12)
        rs = reg_ENCODE.get(I_instruction[2])    
  
    elif I_instruction[0] == "lw":
        imm = sext(int(I_instruction[2]),12)
        rs = reg_ENCODE.get(I_instruction[3]) 
  
    elif I_instruction[0] == "jalr":
        rs = reg_ENCODE.get(I_instruction[2])         
        try:
          imm = sext(int(I_instruction[3]),12)
        except:
          label = label_dict.get(I_instruction[3])
          if (label == None):
             return "e10"
          imm = ((label- PC)*4)
                             
    if (imm == "e1"):
        return imm
      
    if (rs == None) or (rd == None):
        return "e3"
        
    funct = map_I_TYPE[I_instruction[0]][1]
    opc = map_I_TYPE[I_instruction[0]][0]
    
    encoded = imm + rs + funct + rd + opc   
    return encoded
  
########################################################################################

# S-TYPE INSTRUCTIONS
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

########################################################################################

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

# U-TYPE INSTRUCTIONS
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
  
########################################################################################

# J-TYPE INSTRUCTIONS
functions_jtype={"jal":"1101111"}

def J_TYPE(J_instruction):
  '''
  J_instruction is a string in format
  {(function name),(destination register),(label)}

  returns : 32 bit binary sequence
  '''
  try:
    J_instruction[2] = int(J_instruction[2])
  except:
    label = label_dict.get(J_instruction[2])
    if (label == None):
       return "e10"
    J_instruction[2] = ((label-(PC))*4)
    
  imm=(sext(int(J_instruction[2]),21))
  if (imm == "e1"):
      return imm
  imm = imm[0] + imm[10:20] + imm[9] + imm[1:9]
  
  reg=reg_ENCODE.get(J_instruction[1])
  if (reg == None):
      return "e3"
    
  op_code = functions_jtype[J_instruction[0]]         
  return imm + reg + op_code
  
########################################################################################

virtual_halt = "00000000000000000000000001100011"

import sys
with open (sys.argv[1], "r") as pointer:
    assembly = pointer.readlines()
  
#Stores the line number of labels in label_dict
label_dict = {}
error_flag = False
output_list = []

# NOTE : THIS CODE IS STORING THE LABEL WITH LINE NUMBER and then REMOVING THE LABEL from the line.
for i in range(len(assembly)):
    if  (':'  in assembly[i]) :
        temp_label = (re.split( ":", assembly[i] ))[0]
      
        if temp_label in label_dict:
          error_flag = True
          output = errorGEN("e9", i )
          print(output)
          output_list.append(output)
          break
        assembly[i] = assembly[i].replace(temp_label + ": ", "")
        label_dict[temp_label] = i

########################################################################################

if error_flag == False:
    PC = 0
    vh_flag = False
    vh_num = -1
    
    while ( PC < (len(assembly) ) ):
        instruction = (assembly[PC]).lower()
      
        if (instruction == "\n"):                                      #for Empty lines
            PC += 1
            continue
    
        # if (vh_flag == True):
        #     output_list.clear()
        #     output_list.append( errorGEN("e7", vh_num) )
        #     break
          
        instruction_elements = re.split(' |,|\(|\)|:|\n', instruction)
        instruction_elements = [element for element in instruction_elements if element != ""]
   
        type = instruction_elements[0]
      
        if type in instruction_mapping["r_type"]:
            output = R_TYPE(instruction_elements)
      
        elif type in instruction_mapping["i_type"]:        
            output = I_TYPE(instruction_elements)
    
        elif type in instruction_mapping["s_type"]:
            output = S_TYPE(instruction_elements)
    
        elif type in instruction_mapping["b_type"]:
            output = B_TYPE(instruction_elements)
          #label present or not will be checked within B_TYPE() --> label out of bound function in recycle bin
            if (output == virtual_halt):
              vh_flag = True
              vh_num = PC
              
        elif type in list(instruction_mapping["u_type"]):
            output = U_TYPE(instruction_elements)
    
        elif type in list(instruction_mapping["j_type"]):
            output = J_TYPE(instruction_elements)
    
       # code for LABEL
      
        else:
            # opcode not from the mentioned mnemonics
            output_list.clear()
            output = errorGEN("e2", PC)
            output_list.append( output )
            print (output)
            break
    
        if ( output in errorMAPPING ):
            output_list.clear()
            error1 = errorGEN(output, PC)
            output_list.append( error1 )
            print (error1)
            break
      
        output_list.append(output)
        PC += 1
    
    else:
      # this CODE will not be execute if while has been exited due to a BREAK statement
      if (vh_flag == False):
        output_list.clear()
        error2 = errorGEN("e11", PC-1)
        output_list.append( error2 )
        print (error2)

########################################################################################

with open (sys.argv[2], "w") as pointer:
  if (len(output_list) != 0):
      for idx in range(len(output_list) - 1):
         pointer.write(output_list[idx] + "\n")
      pointer.write(output_list[-1])
