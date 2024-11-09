import re
import sys

#register mapping
reg_ENCODE  = {'zero': '00000',   'ra': '00001',     'sp': '00010',     'gp': '00011', 
               'tp': '00100',     't0': '00101',     't1': '00110',     't2': '00111', 
               's0': '01000',     'fp': '01000',     's1': '01001',     'a0': '01010',     'a1': '01011', 
               'a2': '01100',     'a3': '01101',     'a4': '01110',     'a5': '01111', 
               'a6': '10000',     'a7': '10001',     's2': '10010',     's3': '10011', 
               's4': '10100',     's5': '10101',     's6': '10110',     's7': '10111', 
               's8': '11000',     's9': '11001',     's10': '11010',    's11': '11011', 
               't3': '11100',     't4': '11101',     't5': '11110',     't6': '11111'}


#error mapping. can modify later
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

operation = { 'mul' : '0000100',
          'rst' : '0000101',
          'rvrs': '0000111',
          'halt' : '0000110'}
          


######################################################################################################


def multiply(instruction_elements):
    '''
    instruction_elements is a list of the form ['mul', 'rd', 'rs1', 'rs2']
    Output format: Filler bits(10 zeroes) + rd + rs1 + rs2 + opcode
    '''
    opcode = "0000100"
    rd = reg_ENCODE.get(instruction_elements[1])
    rs1 = reg_ENCODE.get(instruction_elements[2])
    rs2 = reg_ENCODE.get(instruction_elements[3])

    if (rd == None) or (rs1 == None) or (rs2 == None):
        return "e3"

    output = '0000000000' + rd + rs1 + rs2 + opcode
    return output

def reset():
    '''
    Output format: Filler bits(25 zeroes) + opcode
    '''
    opcode = "0000101"

    output = '0000000000000000000000000' + opcode
    return output


def rvrs ( instruction ) :
    '''argument : list type, instruction
    returns : string of encoded binary
    '''
    opcode = '0000111'
    rd = reg_ENCODE.get(I_instruction[1])
    rs = reg_ENCODE.get(I_instruction[2])  

    if (rd == None) or (rs == None):
        return "e3"
  
    encoded = '000000000000' + rs + '000' + rd + opcode
    return encoded

def halt():
  
  encoded = '0'*25 + '0000110'
  return encoded
  
#############################################################################################


with open (sys.argv[1], "r") as pointer:
    assembly = pointer.readlines()

output_list = []
PC = 0
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

    opcode = instruction_elements[0]
  
    if operation[opcode] == "0000100":
        output = multiply(instruction_elements)

    elif operation[opcode] == "0000101":
        output = reset()

    elif operation[opcode] == "0000111":
        output = rvrs(instruction_elements)

    elif operation[opcode] == "0000110":
        output = halt()


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


########################################################################################

with open (sys.argv[2], "w") as pointer:
  if (len(output_list) != 0):
      for idx in range(len(output_list) - 1):
         pointer.write(output_list[idx] + "\n")
      pointer.write(output_list[-1])
