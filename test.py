from lib.dataStruct import DataStreams
from lib.node import Node
import lib.operators as opr
from lib.toYaml import convert2Yaml
from lib.yaml2Machine import getProgram, getTokens
# import sys
import yaml

import numpy as np

def main () :

    nodeList: list[Node] = []

    # Example usage
    
    inputValue = 0.496

    fp16 = np.float16(inputValue)
    fp16_binary = ''.join(f'{c:08b}' for c in fp16.tobytes()[::-1])  # 转成二进制表示

    fp32 = np.float32(inputValue)
    fp32_binary = ''.join(f'{c:08b}' for c in fp32.tobytes()[::-1])  # 转成二进制表示
    fp32_hex = ''.join(f'{byte:02x}' for byte in fp32.tobytes()[::-1]) 

    # Create data streams
    data_streams = DataStreams()
    data_streams.add_stream('stream0')
    data_streams.add_stream('stream1')

    # Add data to streams
    data_streams.add_data('stream0', 'data0', value= f'0x{fp32_hex}')
    data_streams.add_data('stream0', 'data1', value='0x80000000')
    data_streams.add_data('stream0', 'data2', value="0x7F800000")
    data_streams.add_data('stream0', 'data3', value="0x00780000")
    data_streams.add_data('stream0', 'data4', value=f"0x{(127<<23):08X}")
    data_streams.add_data('stream0', 'data5', value=f"0x{(15<<23):08X}")
    data_streams.add_data('stream0', 'data6', value="0x0F800000")

    nodeList.append(opr.copy(data_streams.streams["stream0"]["data0"], '0x0000')) #CP0
    nodeList.append(opr.copy(nodeList[0], '0x0001')) #CP1
    nodeList.append(opr.andByBit(data_streams.streams["stream0"]["data1"], nodeList[0], '0x0002'))
    nodeList.append(opr.andByBit(data_streams.streams["stream0"]["data2"], nodeList[1], '0x0003'))
    nodeList.append(opr.andByBit(nodeList[1], data_streams.streams["stream0"]["data3"], '0x0004'))
    nodeList.append(opr.sub(data_streams.streams["stream0"]["data4"], nodeList[3], '0x0005'))
    nodeList.append(opr.sub(data_streams.streams["stream0"]["data5"], nodeList[5], '0x0006'))
    nodeList.append(opr.andByBit(nodeList[6], data_streams.streams["stream0"]["data6"], '0x0007'))
    nodeList.append(opr.orByBit(nodeList[7], nodeList[4], '0x0008'))
    nodeList.append(opr.orByBit(nodeList[2], nodeList[8], '0x0009'))
    nodeList.append(opr.out(nodeList[9], '0x000a'))

    data_streams.add_data('stream1', 'data0', node_name="0x0000", flag="left", value=f'0x{fp32_hex}')
    data_streams.add_data('stream1', 'data1', node_name="0x0002", flag="left", value='0x80000000')
    data_streams.add_data('stream1', 'data2', node_name="0x0003", flag="left", value="0x7F800000")
    data_streams.add_data('stream1', 'data3', node_name="0x0004", flag="right", value="0x007FE000")
    data_streams.add_data('stream1', 'data4', node_name="0x0005", flag="left", value=f"0x{(127<<23):08X}")
    data_streams.add_data('stream1', 'data5', node_name="0x0006", flag="left", value=f"0x{(15<<23):08X}")
    data_streams.add_data('stream1', 'data6', node_name="0x0007", flag="right", value="0x0F800000")

    for node in nodeList :
        print(node)

    print("\n\n")
          
    print(data_streams)

    print("\n\n\n\n")

    convert2Yaml(nodeList, data_streams, "test.yaml")

    with open("test.yaml", 'r') as yml:
        ddp = yaml.safe_load(yml)   

    print(f"{'='*10}PROGRAM{'='*10}")
    programLines = getProgram(ddp)
    print()
    for line in programLines.values() :
        print(line)

    print()
    print()

    print(f"{'='*10}TOKENS{'='*10}")
    tokens = getTokens(ddp)
    print()
    for token in tokens :
        print(token)

    result = input("result: ")

    result = result[0] + result[4:19]

    print(f"result: {result}")
    print(f"expect: {fp16_binary}")

    int_value = int(result, 2)

    # 将整数转换为 numpy 的 FP16
    fp16Result = np.frombuffer(int_value.to_bytes(2, 'little'), dtype=np.float16)[0]

    print(f"expect: {inputValue}")
    print(f"result: {fp16Result}")

    if (abs(fp16Result - inputValue)<0.001):       
        print("PASS!!")
    else:
        print("ERROR!!")

if __name__ == "__main__" :
    main()