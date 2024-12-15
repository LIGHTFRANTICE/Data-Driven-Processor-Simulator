from lib.dataStruct import DataStreams, Data
from lib.node import Node
import lib.operators as opr
from lib.convert import convert2Machine

import numpy as np

def main () :
    
    inputValue = 0.496

    fp16 = np.float16(inputValue)
    fp16_binary = ''.join(f'{c:08b}' for c in fp16.tobytes()[::-1])  # 转成二进制表示

    result = input("result: ")

    result = result[0] + result[4:19]

    print(f"result: {result}")
    print(f"expect: {fp16_binary}")

    int_value = int(result, 2)

    fp16Result = np.frombuffer(int_value.to_bytes(2, 'little'), dtype=np.float16)[0]

    print(f"expect: {inputValue}")
    print(f"result: {fp16Result}")

    if (abs(fp16Result - inputValue)<0.001):       
        print("PASS!!")
    else:
        print("ERROR!!")

if __name__ == "__main__" :
    main()