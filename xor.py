def xor_shellcode(input_shellcode, xor_key):
    input_shellcode = input_shellcode.replace("\n", "").replace("\"", "").replace(" ", "")

    shellcode_bytes = [int(byte, 16) for byte in input_shellcode.split("\\x") if byte]


    xored_bytes = [(byte ^ xor_key) & 0xFF for byte in shellcode_bytes]

    formatted_bytes = [f"0x{byte:02x}" for byte in xored_bytes]

    lines = []
    for i in range(0, len(formatted_bytes), 16):
        lines.append(", ".join(formatted_bytes[i:i+16]))

    formatted_shellcode = ",\n    ".join(lines)

    c_code = f"unsigned char shellcode[] = {{\n    {formatted_shellcode}\n}};"
    
    return c_code


input_shellcode = open("inputSC.txt","r").read()
xor_key = 0xa1b1 & 0xFF 
formatted_c_shellcode = xor_shellcode(input_shellcode, xor_key)
print(formatted_c_shellcode)