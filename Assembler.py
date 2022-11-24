#import sys
#filename = sys.argv[1]
import os
import sys

rgstrs_dict = {"x0": 0, "x1": 1, "x2": 2, "x3": 3, "x4": 4, "x5": 5, "x6": 6, "x7": 7 , "x8": 8 , "x9": 9,
"x10": 10, "x11": 11, "x12": 12, "x13":13, "x14": 14, "x15": 15, "x16": 16, "x17": 17 , "x18": 18 , "x19": 19,
"x20": 20, "x21": 21, "x22": 22, "x23": 23, "x24": 24, "x25": 25, "x26": 26, "x27": 27 , "x28": 28 , "x29": 29,
"x30": 30, "x31": 31}

labels_dict = {} #to store labels and their instCount
a = ["00000000"] * 1024
#print(a)
filename = input("Enter file name: ")

#LABEL forming stage
instCount = -1
with open(os.path.join(sys.path[0], filename), "rt") as f: #full file path
    for line_raw in f:
        line_raw = line_raw.strip() #remove extra whitespaces
        if not(line_raw == ''): #ignore empty lines
            
            instCount = instCount + 1
            line=line_raw.split('//') #separate line comments after the command
            line = line[0].split(':') #separate label and command
            #print(line)
            #print(len(line))
            if len(line) == 2: #label defined
                if not line[0].isnumeric(): #not needed here as data memory is separate so no memory data entries directly
                    new_label = {line[0]: instCount} 
                    labels_dict.update(new_label)
                    #asm_cmd = line[1].strip()
print(labels_dict)

#translation stage
instCount = -1
with open(os.path.join(sys.path[0], filename), "rt") as f: #full file path
    for line_raw in f:
        line_raw = line_raw.strip() #remove extra whitespaces
        if not(line_raw == ''): #ignore empty lines
            
            instCount = instCount + 1
            line=line_raw.split('//') #separate line comments after the command
            line = line[0].split(':') #separate label and command
            #print(line)
            #print(len(line))
            if len(line) == 2: #label defined
                if line[0].isnumeric(): # NOT NEEDED HERE
                    #print("numeric label") #will deal later
                    # sample is 0040: 0001, 0002, 0003, 0004, 0a1f etc
                    # this will store the hex values starting at label numeric address
                    # these lines MUST come at the end to avoid line miscount
                    # this will be dealt here itself TODO
                    asm_cmd = ''
                    data_ptr = int(line[0], 16)
                    data_vals = line[1].split(',') #separate all data values to be written 
                    for data_val in data_vals:
                        data_val_nospc = data_val.strip()
                        #print(data_val_nospc)
                        a[data_ptr] = data_val_nospc
                        data_ptr = data_ptr+2

                else:
                    #new_label = {line[0]: instCount}
                    #labels_dict.update(new_label)
                    asm_cmd = line[1].strip()
            else:
                asm_cmd = line[0].strip()
            #print(asm_cmd)
            if not(asm_cmd == ''):
                asm_cmd = asm_cmd.split(' ', 1) #separate opcode and instruction
                #print(asm_cmd)
                if asm_cmd[0] == "add": 
                    opcode = format(0b0110011, 'b').zfill(7)
                    func7 = format(0b0000000, 'b').zfill(7)
                    func3 = format(0b000, 'b').zfill(3)

                    rgstrs = asm_cmd[1].split(',')
                    rA = rgstrs[1].strip()
                    rB = rgstrs[2].strip()
                    rD = rgstrs[0].strip()
                    rA_val = format(rgstrs_dict[rA], 'b').zfill(5)
                    rB_val =  format(rgstrs_dict[rB], 'b').zfill(5)
                    rD_val =  format(rgstrs_dict[rD], 'b').zfill(5)
                    #cmd_code = opcode<<12
                    #cmd_code = cmd_code|funcn
                    #cmd_code = cmd_code|rD_val<<3
                    #cmd_code = cmd_code|rB_val<<6
                    #cmd_code = cmd_code|rA_val<<9
                    #print(rgstrs)
                    #print(format(cmd_code, 'b').zfill(16))
                    cmd_code = func7+rB_val+rA_val+func3+rD_val+opcode
                    cmd_code_hex = (hex(int(cmd_code,2))[2:]).zfill(8)
                    #print(cmd_code)
                    print(cmd_code_hex, end =" ")
                    a[instCount] = cmd_code_hex
                elif asm_cmd[0] == "addi": 
                    opcode = format(0b0010011, 'b').zfill(7)
                    #func7 = format(0b0000000, 'b').zfill(7)
                    func3 = format(0b000, 'b').zfill(3)

                    rgstrs = asm_cmd[1].split(',')
                    rA = rgstrs[1].strip()
                    rD = rgstrs[0].strip()
                    rA_val = format(rgstrs_dict[rA], 'b').zfill(5)
                    rD_val =  format(rgstrs_dict[rD], 'b').zfill(5)
                    
                    immdt_decimal = int( rgstrs[2].strip() )

                    #offset_val_hexB = immdt_decimal.to_bytes(2, byteorder = 'big', signed = True)
                    #offset_val_hexB = offset_val_hexB.replace(' ', '')
                    #fmt = ('{:02x} ' * len(offset_val_hexB))[:-1]
                    #offset_val_hexB_fmt = fmt.format(*offset_val_hexB) #this prevents values like 9, 10being read as special characters eg newlinw, tab
                    #also it strips last character. reference from: https://stackoverflow.com/questions/51579816/writing-binary-files-in-python-3-why-im-not-getting-the-hexadecimal-representa
                    #offset_val_hexB_str = str(offset_val_hexB_fmt)
                    #offset_val_hexB_str_trim = offset_val_hexB_str.replace(' ', '')[1:] #ignore 1 nibble (to get 12 bits instead of 16)
                    offset_val_binB = (bin(immdt_decimal& 0b111111111111).replace('0b', '')).zfill(12)
                    offset_val_bin12b = offset_val_binB
                    
                    #print(offset_val_bin12b)
                    cmd_code = offset_val_bin12b+rA_val+func3+rD_val+opcode
                    cmd_code_hex = (hex(int(cmd_code,2))[2:]).zfill(8)
                    #print(cmd_code)
                    print(cmd_code_hex, end =" ")
                    a[instCount] = cmd_code_hex
                elif asm_cmd[0] == "slli": 
                    opcode = format(0b0010011, 'b').zfill(7)
                    func7 = format(0b0000000, 'b').zfill(7)
                    func3 = format(0b001, 'b').zfill(3)

                    rgstrs = asm_cmd[1].split(',')
                    rA = rgstrs[1].strip()
                    rD = rgstrs[0].strip()
                    rA_val = format(rgstrs_dict[rA], 'b').zfill(5)
                    rD_val =  format(rgstrs_dict[rD], 'b').zfill(5)
                    
                    immdt_decimal = int( rgstrs[2].strip() ) #shamt

                    #offset_val_hexB = immdt_decimal.to_bytes(1, byteorder = 'big', signed = False)
                    #offset_val_hexB = offset_val_hexB.replace(' ', '')
                    #fmt = ('{:02x} ' * len(offset_val_hexB))[:-1]
                    #offset_val_hexB_fmt = fmt.format(*offset_val_hexB) #this prevents values like 9, 10being read as special characters eg newlinw, tab
                    #also it strips last character. reference from: https://stackoverflow.com/questions/51579816/writing-binary-files-in-python-3-why-im-not-getting-the-hexadecimal-representa
                    #offset_val_hexB_str = str(offset_val_hexB_fmt)
                    #offset_val_hexB_str_trim = offset_val_hexB_str
                    offset_val_binB = (bin(immdt_decimal& 0b111111111111).replace('0b', '')).zfill(5)
                    offset_val_bin5b = offset_val_binB
                    
                    #print(offset_val_bin12b)
                    cmd_code = func7+offset_val_bin5b+rA_val+func3+rD_val+opcode
                    cmd_code_hex = (hex(int(cmd_code,2))[2:]).zfill(8)
                    #print(cmd_code)
                    print(cmd_code_hex, end =" ")
                    a[instCount] = cmd_code_hex

                elif asm_cmd[0] == "beq":
                    opcode = format(0b1100011, 'b').zfill(7)
                    #func7 = format(0b0000000, 'b').zfill(7)
                    func3 = format(0b000, 'b').zfill(3)

                    rgstrs = asm_cmd[1].split(',')
                    rA = rgstrs[0].strip()
                    rB = rgstrs[1].strip()
                    rA_val = format(rgstrs_dict[rA], 'b').zfill(5)
                    rB_val =  format(rgstrs_dict[rB], 'b').zfill(5)
                    
                    #immdt_decimal = int( rgstrs[2].strip() ) #to calc jump offset
                    addr_offset_label =  rgstrs[2].strip()
                    offset = labels_dict.get(addr_offset_label) - instCount
                    offset_val = offset * 4
                    #print(offset_val)

                    #offset_val_hexB = offset_val.to_bytes(2, byteorder = 'big', signed = True)
                    #fmt = ('{:02x} ' * len(offset_val_hexB))[:-1]
                    #offset_val_hexB_fmt = fmt.format(*offset_val_hexB) #this prevents values like 9, 10being read as special characters eg newlinw, tab
                    #also it strips last character. reference from: https://stackoverflow.com/questions/51579816/writing-binary-files-in-python-3-why-im-not-getting-the-hexadecimal-representa
                    

                    #offset_val_hexB_str = str(offset_val_hexB_fmt)
                    #offset_val_hexB_str_trim = offset_val_hexB_str.replace(' ', '') 
                    #print(offset_val_hexB_str_trim)
                    #2 bytes = 4 nibbles = 16 bits, need only 13
                    offset_val_binB = (bin(offset_val& 0b1111111111111).replace('0b', '')).zfill(13)
                    #print(offset_val_binB)
                    offset_val_bin13b = offset_val_binB[-13:]
                    #print(offset_val_bin13b)
                    #print(offset_val_bin13b[0])#12
                    #print(offset_val_bin13b[2:8])#10:5
                    #print(offset_val_bin13b[8:12])#4:1
                    #print(offset_val_bin13b[1])#11


                    cmd_code = offset_val_bin13b[0] +  offset_val_bin13b[2:8] + rB_val + rA_val + func3 + offset_val_bin13b[8:12] + offset_val_bin13b[1]+ opcode
                    
                    cmd_code_hex = (hex(int(cmd_code,2))[2:]).zfill(8)
                    
                    print(cmd_code_hex, end =" ")
                    a[instCount] = cmd_code_hex
                
                elif asm_cmd[0] == "blt":
                    opcode = format(0b1100011, 'b').zfill(7)
                    #func7 = format(0b0000000, 'b').zfill(7)
                    func3 = format(0b100, 'b').zfill(3)

                    rgstrs = asm_cmd[1].split(',')
                    rA = rgstrs[0].strip()
                    rB = rgstrs[1].strip()
                    rA_val = format(rgstrs_dict[rA], 'b').zfill(5)
                    rB_val =  format(rgstrs_dict[rB], 'b').zfill(5)
                    
                    #immdt_decimal = int( rgstrs[2].strip() ) #to calc jump offset
                    addr_offset_label =  rgstrs[2].strip()
                    offset = labels_dict.get(addr_offset_label) - instCount
                    offset_val = offset * 4
                    #print(offset_val)

                    #offset_val_hexB = offset_val.to_bytes(2, byteorder = 'big', signed = True)
                    #fmt = ('{:02x} ' * len(offset_val_hexB))[:-1]
                    #offset_val_hexB_fmt = fmt.format(*offset_val_hexB) #this prevents values like 9, 10being read as special characters eg newlinw, tab
                    #also it strips last character. reference from: https://stackoverflow.com/questions/51579816/writing-binary-files-in-python-3-why-im-not-getting-the-hexadecimal-representa
                    

                    #offset_val_hexB_str = str(offset_val_hexB_fmt)
                    #offset_val_hexB_str_trim = offset_val_hexB_str.replace(' ', '') 
                    #print(offset_val_hexB_str_trim)
                    #2 bytes = 4 nibbles = 16 bits, need only 13
                    offset_val_binB = (bin(offset_val& 0b1111111111111).replace('0b', '')).zfill(13)
                    #print(offset_val_binB)
                    offset_val_bin13b = offset_val_binB[-13:]
                    #print(offset_val_bin13b)
                    #print(offset_val_bin13b[0])#12
                    #print(offset_val_bin13b[2:8])#10:5
                    #print(offset_val_bin13b[8:12])#4:1
                    #print(offset_val_bin13b[1])#11


                    cmd_code = offset_val_bin13b[0] +  offset_val_bin13b[2:8] + rB_val + rA_val + func3 + offset_val_bin13b[8:12] + offset_val_bin13b[1]+ opcode
                    
                    cmd_code_hex = (hex(int(cmd_code,2))[2:]).zfill(8)
                    
                    print(cmd_code_hex, end =" ")
                    a[instCount] = cmd_code_hex
                
                elif asm_cmd[0] == "lw":
                    opcode = format(0b0000011, 'b').zfill(7)
                    func3 = format(0b010, 'b').zfill(3)
                    rgstrs = asm_cmd[1].split(',')
                    off_rS =  (rgstrs[1].strip()).replace(')', '')
                    rD = rgstrs[0].strip()
                    rD_val =  format(rgstrs_dict[rD], 'b').zfill(5)
                    off_rS_spl = off_rS.split('(')
                    rS1 = off_rS_spl[1].strip()
                    rS1_val = format(rgstrs_dict[rS1], 'b').zfill(5)
                    #offset given in int string form directly
                    offset_val = int(off_rS_spl[0], 10) #convert decimal string (denoting offset) to an integer
                    #print(offset_val)
                    #offset_val_hexB = offset_val.to_bytes(2, byteorder = 'big', signed = True)
                    #fmt = ('{:02x} ' * len(offset_val_hexB))[:-1]
                    #offset_val_hexB_fmt = fmt.format(*offset_val_hexB) #this prevents values like 9, 10being read as special characters eg newlinw, tab
                    #also it strips last character. reference from: https://stackoverflow.com/questions/51579816/writing-binary-files-in-python-3-why-im-not-getting-the-hexadecimal-representa
                    #offset_val_hexB_str = str(offset_val_hexB_fmt)
                    #offset_val_hexB_str_trim = offset_val_hexB_str.replace(' ', '') 
                    #print(offset_val_hexB_str_trim)
                    #2 bytes = 4 nibbles = 16 bits, need only 13
                    offset_val_binB = (bin(offset_val& 0b111111111111).replace('0b', '')).zfill(12)
                    #print(offset_val_binB)
                    offset_val_bin12b = offset_val_binB[-12:]
                    #print(offset_val_bin12b)

                    cmd_code = offset_val_bin12b + rS1_val + func3 + rD_val + opcode
                    
                    cmd_code_hex = (hex(int(cmd_code,2))[2:]).zfill(8)
                    
                    print(cmd_code_hex, end =" ")
                    a[instCount] = cmd_code_hex
                elif asm_cmd[0] == "lh":
                    opcode = format(0b0000011, 'b').zfill(7)
                    func3 = format(0b001, 'b').zfill(3)
                    rgstrs = asm_cmd[1].split(',')
                    off_rS =  (rgstrs[1].strip()).replace(')', '')
                    rD = rgstrs[0].strip()
                    rD_val =  format(rgstrs_dict[rD], 'b').zfill(5)
                    off_rS_spl = off_rS.split('(')
                    rS1 = off_rS_spl[1].strip()
                    rS1_val = format(rgstrs_dict[rS1], 'b').zfill(5)
                    #offset given in int string form directly
                    offset_val = int(off_rS_spl[0], 10) #convert decimal string (denoting offset) to an integer
                    offset_val_binB = (bin(offset_val& 0b111111111111).replace('0b', '')).zfill(12)
                    offset_val_bin12b = offset_val_binB[-12:]
                    cmd_code = offset_val_bin12b + rS1_val + func3 + rD_val + opcode  
                    cmd_code_hex = (hex(int(cmd_code,2))[2:]).zfill(8)
                    print(cmd_code_hex, end =" ")
                    a[instCount] = cmd_code_hex
                elif asm_cmd[0] == "lb":
                    opcode = format(0b0000011, 'b').zfill(7)
                    func3 = format(0b000, 'b').zfill(3)
                    rgstrs = asm_cmd[1].split(',')
                    off_rS =  (rgstrs[1].strip()).replace(')', '')
                    rD = rgstrs[0].strip()
                    rD_val =  format(rgstrs_dict[rD], 'b').zfill(5)
                    off_rS_spl = off_rS.split('(')
                    rS1 = off_rS_spl[1].strip()
                    rS1_val = format(rgstrs_dict[rS1], 'b').zfill(5)
                    #offset given in int string form directly
                    offset_val = int(off_rS_spl[0], 10) #convert decimal string (denoting offset) to an integer
                    offset_val_binB = (bin(offset_val& 0b111111111111).replace('0b', '')).zfill(12)
                    offset_val_bin12b = offset_val_binB[-12:]
                    cmd_code = offset_val_bin12b + rS1_val + func3 + rD_val + opcode  
                    cmd_code_hex = (hex(int(cmd_code,2))[2:]).zfill(8)
                    print(cmd_code_hex, end =" ")
                    a[instCount] = cmd_code_hex



                elif asm_cmd[0] == "sw":
                    opcode = format(0b0100011, 'b').zfill(7)
                    func3 = format(0b010, 'b').zfill(3)

                    rgstrs = asm_cmd[1].split(',')
                    rS2 = rgstrs[0].strip()
                    rS2_val =  format(rgstrs_dict[rS2], 'b').zfill(5)
                    off_rS =  (rgstrs[1].strip()).replace(')', '')
                    off_rS_spl = off_rS.split('(')
                    rS1 = off_rS_spl[1].strip()
                    rS1_val = format(rgstrs_dict[rS1], 'b').zfill(5)
                    #offset given in int string form directly
                    offset_val = int(off_rS_spl[0], 10) #convert decimal string (denoting offset) to an integer
                    #print(offset_val)
                    #offset_val_hexB = offset_val.to_bytes(2, byteorder = 'big', signed = True)
                    #fmt = ('{:02x} ' * len(offset_val_hexB))[:-1]
                    #offset_val_hexB_fmt = fmt.format(*offset_val_hexB) #this prevents values like 9, 10being read as special characters eg newlinw, tab
                    #also it strips last character. reference from: https://stackoverflow.com/questions/51579816/writing-binary-files-in-python-3-why-im-not-getting-the-hexadecimal-representa
                    #offset_val_hexB_str = str(offset_val_hexB_fmt)
                    #offset_val_hexB_str_trim = offset_val_hexB_str.replace(' ', '') 
                    #print(offset_val_hexB_str_trim)
                    #2 bytes = 4 nibbles = 16 bits, need only 13
                    offset_val_binB = (bin(offset_val& 0b111111111111).replace('0b', '')).zfill(12)
                    #print(offset_val_binB)
                    offset_val_bin12b = offset_val_binB[-12:]
                    #print(offset_val_bin12b)
                    #print(offset_val_bin12b[0:7])
                    #print(offset_val_bin12b[7:12])

                    cmd_code = offset_val_bin12b[0:7] + rS2_val + rS1_val + func3 + offset_val_bin12b[7:12] + opcode
                    
                    cmd_code_hex = (hex(int(cmd_code,2))[2:]).zfill(8)
                    
                    print(cmd_code_hex, end =" ")
                    a[instCount] = cmd_code_hex     
                
                elif asm_cmd[0] == "sh":
                    opcode = format(0b0100011, 'b').zfill(7)
                    func3 = format(0b001, 'b').zfill(3)
                    rgstrs = asm_cmd[1].split(',')
                    rS2 = rgstrs[0].strip()
                    rS2_val =  format(rgstrs_dict[rS2], 'b').zfill(5)
                    off_rS =  (rgstrs[1].strip()).replace(')', '')
                    off_rS_spl = off_rS.split('(')
                    rS1 = off_rS_spl[1].strip()
                    rS1_val = format(rgstrs_dict[rS1], 'b').zfill(5)
                    #offset given in int string form directly
                    offset_val = int(off_rS_spl[0], 10) #convert decimal string (denoting offset) to an integer 
                    offset_val_binB = (bin(offset_val& 0b111111111111).replace('0b', '')).zfill(12)
                    offset_val_bin12b = offset_val_binB[-12:]
                    cmd_code = offset_val_bin12b[0:7] + rS2_val + rS1_val + func3 + offset_val_bin12b[7:12] + opcode
                    cmd_code_hex = (hex(int(cmd_code,2))[2:]).zfill(8) 
                    print(cmd_code_hex, end =" ")
                    a[instCount] = cmd_code_hex     
                elif asm_cmd[0] == "sb":
                    opcode = format(0b0100011, 'b').zfill(7)
                    func3 = format(0b000, 'b').zfill(3)
                    rgstrs = asm_cmd[1].split(',')
                    rS2 = rgstrs[0].strip()
                    rS2_val =  format(rgstrs_dict[rS2], 'b').zfill(5)
                    off_rS =  (rgstrs[1].strip()).replace(')', '')
                    off_rS_spl = off_rS.split('(')
                    rS1 = off_rS_spl[1].strip()
                    rS1_val = format(rgstrs_dict[rS1], 'b').zfill(5)
                    #offset given in int string form directly
                    offset_val = int(off_rS_spl[0], 10) #convert decimal string (denoting offset) to an integer 
                    offset_val_binB = (bin(offset_val& 0b111111111111).replace('0b', '')).zfill(12)
                    offset_val_bin12b = offset_val_binB[-12:]
                    cmd_code = offset_val_bin12b[0:7] + rS2_val + rS1_val + func3 + offset_val_bin12b[7:12] + opcode
                    cmd_code_hex = (hex(int(cmd_code,2))[2:]).zfill(8) 
                    print(cmd_code_hex, end =" ")
                    a[instCount] = cmd_code_hex     
        print(line_raw)
                    

#print(a[0:100])


#print(labels_dict)
count8 = 0
with open(os.path.join(sys.path[0], filename+'_assembled'), "w") as f_asm:
    for curr_hex in a:
        f_asm.write(curr_hex + ' ')
        count8 = count8 + 1
        if count8==8:
            f_asm.write('\n') #for readability
            count8=0
