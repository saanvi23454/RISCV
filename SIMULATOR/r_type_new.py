def R_TYPE_TRYING(line):
    """
    line is a 32-bit string
    reg1, reg2 - in binary 2's complement
    rs1, rs2, rd - addresses of registers(keys in register dict)
    register dictionary contains values in BINARY 2's Complement
    """
    global PC
    global register
    global memory

    funct7 = line[0:7]
    rs2 = line[7:12]
    rs1 = line[12:17]
    funct3 = line[17:20]
    rd = line[20:25]
    opcode = line[25:32]                        # will not be used, 0110011                  

    #sub
    if funct7 == "0100000":
        result = sub_bin(register[rs1], register[rs2])
        register[rd] = result

    else:
        #add
        if funct3 == "000":
            result = add_bin(register[rs1], register[rs2])
            register[rd] = result

        #sll
        elif funct3 == "001":
            r2 = bin_to_dec(register[rs2][27:32], 'u')
            r1 = register[rs1][r2:32]
            result = r1 + r2*'0'
            register[rd] = result

        #slt
        elif funct3 == "010":
            if bin_to_dec(rs1) < bin_to_dec(rs2):
                result = '0'*31 + '1'
                register[rd] = result

        #sltu
        elif funct3 == "011":
            r1 = bin_to_dec(register[rs1], 'u')
            r2 = bin_to_dec(register[rs2], 'u')

            if r1 < r2:
                result = '0'*31 + '1'
                register[rd] = result

        #xor
        elif funct3 == "100":
            r1 = bin_to_dec(register[rs1])
            r2 = bin_to_dec(register[rs2])
            result = sext((r1 ^ r2),32))                      # bin will give string starting with 0b
            register[rd] = result                

        #srl
        elif funct3 == "101":
            r2 = bin_to_dec(register[rs2][27:32], 'u')
            r1 = register[rs1][0:32-r2]
            result = r2*'0' + r1
            register[rd] = result

        #or
        elif funct3 == "110":
            r1 = bin_to_dec(register[rs1])
            r2 = bin_to_dec(register[rs2])
            result = sext((r1 | r2), 32)
            register[rd] = result

        #and
        else:
            r1 = bin_to_dec(register[rs1])
            r2 = bin_to_dec(register[rs2])
            result = sext((r1 & r2),32)
            register[rd] = result

    PC += 4
