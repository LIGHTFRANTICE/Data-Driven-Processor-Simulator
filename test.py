from lib.dataStruct import DataStreams, Data
from lib.node import Node
import lib.operators as opr
from lib.convert import convert2Machine

import numpy as np

def fp32ToFp16(inputValue: float, nodeList: list[Node], dataStreams: DataStreams) -> tuple[list[Node], DataStreams]:

    fp32 = np.float32(inputValue)
    fp32_hex = ''.join(f'{byte:02x}' for byte in fp32.tobytes()[::-1]) 

    for streamCnt in range(15):
        
        dataStreams.add_stream(f'stream{streamCnt}')
        
        for dataSet in range(1):
            # Add data to stream
            dataStreams.add_data(f'stream{streamCnt}', node_name="0x0000", flag="left", value=f'0x{fp32_hex}')
            dataStreams.add_data(f'stream{streamCnt}', node_name="0x0002", flag="left", value='0x80000000')
            dataStreams.add_data(f'stream{streamCnt}', node_name="0x0003", flag="left", value="0x7F800000")
            dataStreams.add_data(f'stream{streamCnt}', node_name="0x0004", flag="right", value="0x007FE000")
            dataStreams.add_data(f'stream{streamCnt}', node_name="0x0005", flag="left", value=f"0x{(127<<23):08X}")
            dataStreams.add_data(f'stream{streamCnt}', node_name="0x0006", flag="left", value=f"0x{(15<<23):08X}")
            dataStreams.add_data(f'stream{streamCnt}', node_name="0x0007", flag="right", value="0x0F800000")

    nxtAddr = ''.join(f'{byte:02x}' for byte in np.int16(len(nodeList)).tobytes()[::-1])
    nodeList.append(opr.copy(nodeList[-1], f'0x{nxtAddr}')) #CP1
    nxtAddr = ''.join(f'{byte:02x}' for byte in np.int16(len(nodeList)).tobytes()[::-1])
    nodeList.append(opr.andByBit(Data(), nodeList[0], f'0x{nxtAddr}'))
    nxtAddr = ''.join(f'{byte:02x}' for byte in np.int16(len(nodeList)).tobytes()[::-1])
    nodeList.append(opr.andByBit(Data(), nodeList[1], f'0x{nxtAddr}'))
    nxtAddr = ''.join(f'{byte:02x}' for byte in np.int16(len(nodeList)).tobytes()[::-1])
    nodeList.append(opr.andByBit(nodeList[1], Data(), f'0x{nxtAddr}'))
    nxtAddr = ''.join(f'{byte:02x}' for byte in np.int16(len(nodeList)).tobytes()[::-1])
    nodeList.append(opr.sub(Data(), nodeList[3], f'0x{nxtAddr}'))
    nxtAddr = ''.join(f'{byte:02x}' for byte in np.int16(len(nodeList)).tobytes()[::-1])
    nodeList.append(opr.sub(Data(), nodeList[5], f'0x{nxtAddr}'))
    nxtAddr = ''.join(f'{byte:02x}' for byte in np.int16(len(nodeList)).tobytes()[::-1])
    nodeList.append(opr.andByBit(nodeList[6], Data(), f'0x{nxtAddr}'))
    nxtAddr = ''.join(f'{byte:02x}' for byte in np.int16(len(nodeList)).tobytes()[::-1])
    nodeList.append(opr.orByBit(nodeList[7], nodeList[4], f'0x{nxtAddr}'))
    nxtAddr = ''.join(f'{byte:02x}' for byte in np.int16(len(nodeList)).tobytes()[::-1])
    nodeList.append(opr.orByBit(nodeList[2], nodeList[8], f'0x{nxtAddr}'))

    return nodeList, dataStreams

def main () :
    nodeList: list[Node] = []

    # initial node
    nodeList.append(opr.copy(Data(), '0x0000')) #CP0
    
    dataStreams = DataStreams()
    
    inputValue = 0.496

    nodeList, dataStreams = fp32ToFp16(inputValue, nodeList, dataStreams)

    nxtAddr = ''.join(f'{byte:02x}' for byte in np.int16(len(nodeList)).tobytes()[::-1])
    # output node
    nodeList.append(opr.out(nodeList[-1], f'0x{nxtAddr}'))

    convert2Machine(nodeList, dataStreams)


if __name__ == "__main__" :
    main()