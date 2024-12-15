from lib.dataStruct import DataStreams, Data
from lib.node import Node
import lib.operators as opr
from lib.convert import convert2Machine

import numpy as np

def fp32ToFp16(inputValue: float) -> tuple[list[Node], DataStreams]:

    nodeList: list[Node] = []

    fp32 = np.float32(inputValue)
    fp32_hex = ''.join(f'{byte:02x}' for byte in fp32.tobytes()[::-1]) 

    # Create data streams
    dataStreams = DataStreams()

    for streamCnt in range(15):
        
        dataStreams.add_stream(f'stream{streamCnt}')
        
        dataCnt = 0
        for dataSet in range(1):
            # Add data to stream
            dataStreams.add_data(f'stream{streamCnt}', f'data{dataCnt}', node_name="0x0000", flag="left", value=f'0x{fp32_hex}')
            dataCnt += 1
            dataStreams.add_data(f'stream{streamCnt}', f'data{dataCnt}', node_name="0x0002", flag="left", value='0x80000000')
            dataCnt += 1
            dataStreams.add_data(f'stream{streamCnt}', f'data{dataCnt}', node_name="0x0003", flag="left", value="0x7F800000")
            dataCnt += 1
            dataStreams.add_data(f'stream{streamCnt}', f'data{dataCnt}', node_name="0x0004", flag="right", value="0x007FE000")
            dataCnt += 1
            dataStreams.add_data(f'stream{streamCnt}', f'data{dataCnt}', node_name="0x0005", flag="left", value=f"0x{(127<<23):08X}")
            dataCnt += 1
            dataStreams.add_data(f'stream{streamCnt}', f'data{dataCnt}', node_name="0x0006", flag="left", value=f"0x{(15<<23):08X}")
            dataCnt += 1
            dataStreams.add_data(f'stream{streamCnt}', f'data{dataCnt}', node_name="0x0007", flag="right", value="0x0F800000")
            dataCnt += 1

            

    nodeList.append(opr.copy(Data(), '0x0000')) #CP0
    nodeList.append(opr.copy(nodeList[0], '0x0001')) #CP1
    nodeList.append(opr.andByBit(Data(), nodeList[0], '0x0002'))
    nodeList.append(opr.andByBit(Data(), nodeList[1], '0x0003'))
    nodeList.append(opr.andByBit(nodeList[1], Data(), '0x0004'))
    nodeList.append(opr.sub(Data(), nodeList[3], '0x0005'))
    nodeList.append(opr.sub(Data(), nodeList[5], '0x0006'))
    nodeList.append(opr.andByBit(nodeList[6], Data(), '0x0007'))
    nodeList.append(opr.orByBit(nodeList[7], nodeList[4], '0x0008'))
    nodeList.append(opr.orByBit(nodeList[2], nodeList[8], '0x0009'))
    nodeList.append(opr.out(nodeList[9], '0x000a'))

    return nodeList, dataStreams

def main () :
    nodeList: list[Node] = []
    
    inputValue = 0.496

    nodeList, dataStreams = fp32ToFp16(inputValue)

    convert2Machine(nodeList, dataStreams)


if __name__ == "__main__" :
    main()