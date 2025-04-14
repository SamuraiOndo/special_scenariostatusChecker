from binary_reader import BinaryReader

def read_string(reader):
    pointer = reader.read_uint32()
    stay3 = reader.pos()
    reader.seek(pointer)
    string = reader.read_str()
    reader.seek(stay3)
    return string

def getChaptersAndStates():
    f = open("scenario_state.bin","rb")
    reader = BinaryReader(f.read())
    reader.set_encoding('shift-jis')
    reader.set_endian(True)
    f.close()
    reader.seek(4)
    p1Offset = reader.read_uint32()
    reader.seek(0x38)
    count = reader.read_uint32()
    pointer = reader.read_uint32()
    reader.seek(pointer)
    p1Nodes = []
    for i in range(count):
        nodeName = read_string(reader)
        prevPartCount = reader.read_uint16() 
        p1Count = reader.read_uint16()
        stay = reader.pos()
        reader.seek(p1Offset + (0x2c * prevPartCount))

        for j in range(p1Count):
            chapName = read_string(reader)
            stringCount = reader.read_uint32()
            stringPointerPointer = reader.read_uint32()
            strings = []
            stay2 = reader.pos()
            if (stringPointerPointer > 0):
                reader.seek(stringPointerPointer)
                for k in range(stringCount):
                    string = read_string(reader)
                    strings.append(string)
            p1Nodes.append([chapName,strings])
            reader.seek(stay2)
            reader.read_uint32(8)

        reader.seek(stay)

    return p1Nodes
            

if __name__ == '__main__':
    getChaptersAndStates()