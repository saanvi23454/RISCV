from bitstring import Bits

# Used bin_to_dec function

def R_TYPE(line):
    """
    line is a 32-bit string
    reg1, reg2 - in binary 2's complement
    rs1, rs2, rd - addresses of registers(keys in register dict)
    register dictionary contains values in BINARY 2's Complement
    """
    global PC, register

    funct7 = line[0:7]
    rs2 = line[7:12]
    rs1 = line[12:17]
    funct3 = line[17:20]
    rd = line[20:25]
    opcode = line[25:32]                        # will not be used, 0110011

    reg1 = Bits(bin = str(register[rs1]))                       # register[rs1] --> binary 2's complement
    reg2 = Bits(bin = str(register[rs2]))                       

    if funct7 == "0100000":
        #sub
        result = sub_bin(str(register[rs1]), str(register[rs2]))
        register[rd] = result

    else:
        if funct3 == "000":
            #add
            result = add_bin(str(register[rs1]), str(register[rs2]))
            register[rd] = result

        elif funct3 == "001":
            #sll
            r2 = bin_to_dec(register[rs2][27:32], 'u')
            r1 = register[rs1][r2:32]
            result = r1 + r2*'0'
            register[rd] = result

        elif funct3 == "010":
            #slt
            if reg1.int < reg2.int:
                result = '00000000000000000000000000000001'
                register[rd] = result

        elif funct3 == "011":
            #sltu
            r1 = bin_to_dec(register[rs1], 'u')
            r2 = bin_to_dec(register[rs2], 'u')

            if r1 < r2:
                result = '00000000000000000000000000000001'
                register[rd] = result

        elif funct3 == "100":
            #xor
            r1 = bin_to_dec(register[rs1], 'u')
            r2 = bin_to_dec(register[rs2], 'u')
            result = bin(r1 ^ r2)[2:]                       # bin will give string starting with 0b
            register[rd] = (32 - len(result))*'0' + result                   

        elif funct3 == "101":
            #srl
            r2 = bin_to_dec(register[rs2][27:32], 'u')
            r1 = register[rs1][0:32-r2]
            result = r2*'0' + r1
            register[rd] = result

        elif funct3 == "110":
            #or
            r1 = bin_to_dec(register[rs1], 'u')
            r2 = bin_to_dec(register[rs2], 'u')
            result = bin(r1 | r2)[2:]
            register[rd] = (32 - len(result))*'0' + result

        else:
            #and
            r1 = bin_to_dec(register[rs1], 'u')
            r2 = bin_to_dec(register[rs2], 'u')
            result = bin(r1 & r2)[2:]
            register[rd] = (32 - len(result))*'0' + result

    PC += 4
