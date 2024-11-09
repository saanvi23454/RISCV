import sys

def display_file(program_ctr, file_reg):
    global output
    number = sext(str(program_ctr), 32)
    line = '0b'
    line += number
    for reg in file_reg:
        file_reg_value=file_reg[reg]
        line = line + " 0b" + ("0"*(32-len(file_reg_value)))+file_reg_value#sext(file_reg_value,32)
    line+=" "
    output.append(line)

def display_mem(memory_reg):
    global output
    for reg in memory_reg:
        reg_name=bin_to_dec(reg, 'u')
        reg_name=hex(reg_name)
        line=reg_name[0:2]+"000"+reg_name[2:7]+":0b"+memory_reg[reg]
        output.append(line)
      
##########################################################################################################

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

##################################################################################

def bin_to_dec ( number, sign = 's' ) :
  # number is a STRING
  # length is atleast 1
  # sign : s means signed, u means unsigned
  sign = sign.lower()
  
  dec = 0
  pow = 0

  length = len(number)
  if length == 0:
    return 0
    
  for i in range( length - 1, 0, -1 ):
    dec += (int(number[i]) * (2**pow) )
    pow += 1

  
  if sign == 's':
    dec -= (int(number[0]) * (2**(length-1)) )
  elif sign == 'u':
    dec += (int(number[0]) * (2**(length-1)) )


  return dec

#####################################################################################

def mul_bin(num1, num2):
    #num 1 and num 2 are in binary string
    a = bin_to_dec(num1)
    b = bin_to_dec(num2)
    result = sext( (a*b), 32)
    return result

######################################################################################

# HALT
# opcode 0000110
#let all other bits be filler 0
halt = '00000000000000000000000000000110'

# simply have to write in while loop, if line == halt, break. No need for function

####################################################################################

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

def mul(line):
    '''
    Input format: Filler bits(10 zeroes) + rd + rs1 + rs2 + opcode(0000100)
    '''
    global PC, register

    rd = line[10:15]
    rs1 = line[15:20]
    rs2 = line[20:25]

    register[rd] = mul_bin(register[rs1], register[rs2])

    PC += 4

def rst():
    '''
    No input for reset, just check in while loop if opcode matches with 0000101
    '''
    global PC, register
    for key in register:
        if key == '00010':
            register[key] = '00000000000000000000000100000000'
            continue
        else:
            register[key] = '00000000000000000000000000000000'

    PC += 4

################################################################################################

register = {'00000': '00000000000000000000000000000000', 
 '00001': '00000000000000000000000000000000', 
 '00010': '00000000000000000000000100000000', 
 '00011': '00000000000000000000000000000000', 
 '00100': '00000000000000000000000000000000', 
 '00101': '00000000000000000000000000000000', 
 '00110': '00000000000000000000000000000000', 
 '00111': '00000000000000000000000000000000', 
 '01000': '00000000000000000000000000000000', 
 '01001': '00000000000000000000000000000000', 
 '01010': '00000000000000000000000000000000', 
 '01011': '00000000000000000000000000000000', 
 '01100': '00000000000000000000000000000000', 
 '01101': '00000000000000000000000000000000', 
 '01110': '00000000000000000000000000000000', 
 '01111': '00000000000000000000000000000000', 
 '10000': '00000000000000000000000000000000', 
 '10001': '00000000000000000000000000000000', 
 '10010': '00000000000000000000000000000000', 
 '10011': '00000000000000000000000000000000', 
 '10100': '00000000000000000000000000000000', 
 '10101': '00000000000000000000000000000000', 
 '10110': '00000000000000000000000000000000', 
 '10111': '00000000000000000000000000000000', 
 '11000': '00000000000000000000000000000000', 
 '11001': '00000000000000000000000000000000', 
 '11010': '00000000000000000000000000000000', 
 '11011': '00000000000000000000000000000000', 
 '11100': '00000000000000000000000000000000', 
 '11101': '00000000000000000000000000000000', 
 '11110': '00000000000000000000000000000000', 
 '11111': '00000000000000000000000000000000'}
  
 # to get value stored in register from its binary. value is in DECIMAL

register_name = { } # to decode the register name from its binary

memory = {'10000000000000000': '00000000000000000000000000000000', 
 '10000000000000100': '00000000000000000000000000000000', 
 '10000000000001000': '00000000000000000000000000000000', 
 '10000000000001100': '00000000000000000000000000000000', 
 '10000000000010000': '00000000000000000000000000000000', 
 '10000000000010100': '00000000000000000000000000000000', 
 '10000000000011000': '00000000000000000000000000000000', 
 '10000000000011100': '00000000000000000000000000000000', 
 '10000000000100000': '00000000000000000000000000000000', 
 '10000000000100100': '00000000000000000000000000000000', 
 '10000000000101000': '00000000000000000000000000000000', 
 '10000000000101100': '00000000000000000000000000000000', 
 '10000000000110000': '00000000000000000000000000000000', 
 '10000000000110100': '00000000000000000000000000000000', 
 '10000000000111000': '00000000000000000000000000000000', 
 '10000000000111100': '00000000000000000000000000000000', 
 '10000000001000000': '00000000000000000000000000000000', 
 '10000000001000100': '00000000000000000000000000000000', 
 '10000000001001000': '00000000000000000000000000000000', 
 '10000000001001100': '00000000000000000000000000000000', 
 '10000000001010000': '00000000000000000000000000000000', 
 '10000000001010100': '00000000000000000000000000000000', 
 '10000000001011000': '00000000000000000000000000000000', 
 '10000000001011100': '00000000000000000000000000000000', 
 '10000000001100000': '00000000000000000000000000000000', 
 '10000000001100100': '00000000000000000000000000000000', 
 '10000000001101000': '00000000000000000000000000000000', 
 '10000000001101100': '00000000000000000000000000000000', 
 '10000000001110000': '00000000000000000000000000000000', 
 '10000000001110100': '00000000000000000000000000000000', 
 '10000000001111000': '00000000000000000000000000000000', 
 '10000000001111100': '00000000000000000000000000000000'}

###################################################################################################

with open (sys.argv[1], "r") as pointer:
    binary = pointer.readlines()

for i in range(len(binary)-1):
   binary[i]=binary[i][:-1]
# print(binary)


PC = 0
output = []

while (PC <  (4*len( binary )) ):
    line = binary[PC//4]

    if line == halt:
        display_file(PC,register)                        # FLAG
        break
  
    opcode = line[25:32]

    # reverse
    if opcode == '0000111':
        rvrs(line)

    # multiply
    if opcode == '0000100':
        mul(line)

    # reset
    if opcode == '0000101':
        rst()
        
    register['00000'] = '0'*32
    
    display_file(PC, register)

display_mem(memory)



with open (sys.argv[2], "w") as pointer:
    if (len(output) != 0):
        for idx in range(len(output) - 1):
            pointer.write(output[idx] + "\n")
        pointer.write(output[-1])
