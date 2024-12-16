from lib.dataStruct import DataStreams, Data
from lib.node import Node
import lib.operators as opr
from lib.convert import convert2Machine

import numpy as np
import struct

def adjust_exponent(exponent_bits, original_bias, target_bits, target_bias):
    """
    调整指数部分，使其符合目标浮点数精度的指数范围。
    
    参数：
    - exponent_bits: 原始浮点数的指数部分（整数表示）
    - original_bias: 原始浮点数的偏移量（如 FP64 的 1023）
    - target_bits: 目标指数位数（如 BF16 为 8 位，FP16 为 5 位）
    - target_bias: 目标浮点数的偏移量（如 BF16 和 FP32 为 127）

    返回值：
    - 截断后符合目标精度的指数值（整数表示）
    """
    # 将原始指数转换为十进制表示
    exponent_decimal = int(exponent_bits, base=2) - original_bias

    # 计算目标指数范围
    max_exponent = (2 ** (target_bits - 1)) - 1  # 最大值（如 BF16 的 127）
    min_exponent = -max_exponent + 1             # 最小值（如 BF16 的 -126）

    # 检查并调整指数范围
    if exponent_decimal > max_exponent:
        # 超过目标精度的指数范围，则设置为最大值
        adjusted_exponent = max_exponent + target_bias
    elif exponent_decimal < min_exponent:
        # 指数低于最小值，表示为非规格化数
        adjusted_exponent = 0  # 非规格化数的指数为 0
    else:
        # 指数在范围内，重新调整为目标偏移量
        adjusted_exponent = exponent_decimal + target_bias
    
    return format(adjusted_exponent, f'0{target_bits}b')

def fp32ToFp16_x86(inputValue: float) -> str :
    fp32 = np.float32(inputValue)
    fp32_binary = ''.join(f'{byte:08b}' for byte in fp32.tobytes()[::-1]) 

    sign = fp32_binary[0]

    mantissa = fp32_binary[9:19]

    exp = adjust_exponent(exponent_bits=fp32_binary[1:9], original_bias=127, target_bits=5, target_bias=15)

    return sign + exp + mantissa

def main () :   
    inputValue = 0.496

    fp32 = np.float32(inputValue)
    fp32_binary = ''.join(f'{byte:08b}' for byte in fp32.tobytes()[::-1]) 

    fp16_binary = fp32ToFp16_x86(inputValue)

    print(f"Original input 32 bits: {fp32_binary}")
    
    result = input("result: ")
    result = result[0] + result[4:19]
    print(f"Expect          : {fp16_binary}")
    print(f"Formatted Result: {result}")

    int_value = int(result, 2)
    fp16Result = np.frombuffer(int_value.to_bytes(2, 'little'), dtype=np.float16)[0]
    print(f"Float Expect: {inputValue}")
    print(f"Float Result: {fp16Result}")

    if (abs(fp16Result - inputValue)<0.001):       
        print("PASS!!")
    else:
        print("ERROR!!")

if __name__ == "__main__" :
    main()