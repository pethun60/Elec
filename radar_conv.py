import sys
import re
import argparse

version = '1.0.0'

# TODO: git version

# Convert Radar 1.0 DB to Codesys

def parseLine(line, devIx):
    """ Search line for patterns to convert
    
    Parameters
    ----------
    line : string
        The line to parse
    devIx : integer
        The device number
    
    Returns
    -------
    Tuple with the Parsed line or empty string and boolean indicating new device
    """

    device = False
    result = ""
    items = line.strip().split('|||')   # Split on seperator
    if line != '\n' and line.find('//', 0, 3) < 0 and len(items) > 2:  # Filter lines
        adrOffset = [0x000, 0x200, 0x400, 0x600, 0xA00]
        name = items[0]                             # Get name
        adr = int(re.split(r",|;", items[1])[1])    # Get address
        if devIx < 6:
            if adr > adrOffset[devIx - 1]:
                adr -= adrOffset[devIx - 1]

        if len(items) == 4:                     # Ordinary values
            if items[3] == "":                  # Get Scale with default value
                scale = "1.0"
            else:
                scale = re.split(r"[(|,]", items[3])[1] 
            
            result = "{}:=scaleFunction(modbus_var_1000[{}],{}, 0);\n".format(name, adr, scale)
        elif len(items) == 5 and adr < 10:      # Bitmask
            regs = ['Trip_BITs_0_to_15', 'Trip_BITs_16_to_31', 'Trip_BITs_32_to_47', 'Trip_BITs_48_to_63', 'Trip_BITs_64_to_79',
                    'Alarm_BITs_80_to_95', 'Alarm_BITs_96_to_111', 'Statusbits_1032', 'Statusbits_1033', 'Statusbits_10']
            
            reg = regs[int(adr)]
            mask = re.split(r"[(|)]", items[4])  # Convert binary to integer)
            bit = 0
            if len(mask) > 3:
                bit = mask[3]

            result = "{}:=maskbitFunction({},{});\n".format(name, reg, bit)
    elif line.find('[DEVICENAME]') != -1:
        device = True

    return result, device

#------------------------------------------------------------------------------

if __name__ == '__main__':
    # Used when called directly
    try:
        # Create comandline parser
        parser = argparse.ArgumentParser(description='Convert Radar 1.0 DB for Codesys')
        parser.add_argument('--v', action='store_true', help='Display version')
        parser.add_argument('--i', default='./DB_Modbus_Vipa.txt', help='Input file')
        args = parser.parse_args()
        
        # The actual program
        if args.v:
            print('RadarConv version ' + version) # Print version information
        else:
            print('Beginning processing!')
            print(' Input file : ' + args.i)

            # Open input file
            fileIn = open(args.i, 'r')
            linesIn = fileIn.readlines()
            
            count = 0
            device = 0
            linesOut = []
            nameOut = "./Device{}_dB.txt".format(device)
            # Loop all lines - be aware of newline
            for line in linesIn:
                newLine, newDevice = parseLine(line, device)

                if newDevice:
                    if len(linesOut) > 0:
                        # save temporary result
                        fileOut = open(nameOut, 'w')
                        fileOut.writelines(linesOut)
                        fileOut.close()
                    
                    device += 1
                    linesOut.clear()
                    nameOut = "./Device{}_dB.txt".format(device)

                if newLine != "":
                    count += 1
                    linesOut.append(newLine)
                    print("Line{}: {}".format(count, line.strip()))

            # Print & save final result
            nameOut = "./Device{}_dB.txt".format(device)
            fileOut = open(nameOut, 'w')
            fileOut.writelines(linesOut)
            fileOut.close()
            print("Done, {} line found!".format(count))
            
    except Exception as e:
        print(repr(e))                                  # Print exception information

    finally:
        if fileIn != None:      # Close file if open
            fileIn.close()

