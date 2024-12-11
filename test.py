from dataStruct import DataStreams
from node import Node, Const
from operators import add, sub
from toYaml import convert2Yaml
from yaml2Machine import getProgram, getTokens
# import sys
import yaml

def main () :

    nodeList: list[Node] = []

    # Example usage
    nodeList.append(Node(name="node0", address='0x0000', calType='uni', func='copy'))
    # nodeList.append(Node(name="node1", address='0x0001', calType='uni', func='copy'))


    # Create data streams
    data_streams = DataStreams()
    data_streams.add_stream('stream0')
    data_streams.add_stream('stream1')

    # Add data to streams
    data_streams.add_data('stream0', 'data0', nodeList[0].name, 'left', '0x3F000000')
    data_streams.add_data('stream1', 'data1', nodeList[1].name, 'left', '0x3F000000')
    #data_streams.add_data('stream1', 'data2', value="0x3F000000")

    nodeList.append(add(nodeList[0], nodeList[1],'0x0002'))
    #nodeList.append(sub(nodeList[2], data_streams.streams["stream1"]["data2"], '0x0003'))
    
    for node in nodeList :
        print(node)

    print("\n\n")
          
    print(data_streams)

    print("\n\n\n\n")

    convert2Yaml(nodeList, data_streams, "test.yaml")

    with open("test.yaml", 'r') as yml:
        ddp = yaml.safe_load(yml)   

    programLines = getProgram(ddp)
    tokens = getTokens(ddp)

    print(f"{'='*10}PROGRAM{'='*10}")
    for line in programLines.values() :
        print(line)

    print()
    print()

    print(f"{'='*10}TOKENS{'='*10}")
    for token in tokens :
        print(token)

if __name__ == "__main__" :
    main()