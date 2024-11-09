ABINAME_to_REG = {"zero" : "x0",    "ra" : "x1",
                  "sp" : "x2",    "gp" : "x3",    "tp" : "x4",
                  "t0" : "x5",    "t1" : "x6",    "t2" : "x7",
                  "s0" : "x8",    "fp" : "x8",    "s1" : "x9",
                  "a0" : "x10",   "a1" : "x11",   "a2" : "x12",    "a3" : "x13", 
                  "a4" : "x14",   "a5" : "x15",   "a6" : "x16",    "a7" : "x17",
                  "s2" : "x18",   "s3" : "x19",   "s4" : "x20",    "s5" : "x21",
                  "s6" : "x22", "s7":"x23", "s8":"x24", "s9":"x25", "s10":"x26","s11":"x27",
                  "t3" : "x28", "t4": "x29", "t5":"x30", "t6":"x31"}

def string_EXT( length , filler , value ):
    num = length - len(value)
    final = filler*num + value
    return final

def reg_ENCODE( reg_NAME ):
    reg_NUM = int(reg_NAME[1:])
    bin_EQ = bin(reg_NUM)[2:]
    bin_EQ = string_EXT( 5 , "0" , bin_EQ )
    return bin_EQ



def string_to_number(value):
  ''' this function takes a STRING number as argument
  returns a corresponding INTEGER value after removing leading 0 
  '''
  fin = ""
  if value[0]=="-":
    fin += "-"
    value = value[1:]
  value = value.lstrip("0")
  fin += value
  return int(fin)


def label_in_bounds(label):
    """
    label: an Integer, in decimal, signed.
    this function returns e8 if label is out of bounds, else True.
    """
    global PC, assembly

    line_to_jump = PC + label
    if line_to_jump >= 0 and line_to_jump < len(assembly):
        return True
    else:
        return "e8"


  #this code not needed anymore !!    
        #if label is present in instruction_elements, type will be 2nd element of the list(after removing "")
        #NOTE: Label has not been removed
        try: 
            integer = int(instruction_elements[0])
            instruction_elements = [element for element in instruction_elements if element != ""]
            type = instruction_elements[1]
        except: type = instruction_elements[0]

            if type == "jalr":
                label_num = int(instruction_elements[-1])               #to check if resultant line(to jump to) is out of bounds
                if label_in_bounds(label_num) == "e8":
                    output_list.clear()
                    output_list.append(errorGEN("e8", PC))
                    break


            label_num = int(instruction_elements[-1])              #to check if resultant line(to jump to) is out of bounds
            if label_in_bounds(label_num) == "e8":
                output_list.clear()
                output_list.append(errorGEN("e8", PC))
                break
          
