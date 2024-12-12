import lib.node as nd
import lib.dataStruct as ds

import yaml

def convertNodeList(nodeList: list[nd.Node]) -> dict :
    nodeDict = {}
    for node in nodeList:
        nodeDict[node.name] = {}
        nodeDict[node.name]["address"] = node.address
        nodeDict[node.name]["calType"] = node.calType
        nodeDict[node.name]["func"] = node.func
        nodeDict[node.name]["goto"] = {}
        if node.goto["left"]["node"] is not None:
            nodeDict[node.name]['goto']['left'] = {}
            nodeDict[node.name]['goto']['left']['node'] = node.goto["left"]["node"]
            nodeDict[node.name]['goto']['left']['flag'] = node.goto["left"]["flag"]
        if node.goto["right"]["node"] is not None:
            nodeDict[node.name]['goto']['right'] = {}
            nodeDict[node.name]['goto']['right']['node'] = node.goto["right"]["node"]
            nodeDict[node.name]['goto']['right']['flag'] = node.goto["right"]["flag"]
    return nodeDict

def convertDataStreams(dataStreams: ds.DataStreams) -> dict :
    dataStreamsDict = {}

    for dataStreamName, dataStream in dataStreams.streams.items() :
        dataStreamsDict[dataStreamName] = {}
        for dataName, data in dataStream.items():
            dataStreamsDict[dataStreamName][dataName] = {}
            dataStreamsDict[dataStreamName][dataName]['node'] = data.node
            dataStreamsDict[dataStreamName][dataName]['flag'] = data.flag
            dataStreamsDict[dataStreamName][dataName]['value'] = data.value

    return dataStreamsDict


def convert2Yaml(nodeList: list[nd.Node], dataStreams: ds.DataStreams, fileName: str) -> None:

    nodeDict = convertNodeList(nodeList)

    dataStreamsDict = convertDataStreams(dataStreams)

    convertDict = {}

    convertDict["nodes"] = nodeDict
    convertDict["streams"] = dataStreamsDict

    with open(fileName, 'w', encoding='utf-8') as f:
        yaml.dump(data=convertDict, stream=f, allow_unicode=True)


def main () :

    from lib.dataStruct import DataStreams
    from lib.node import Node
    from lib.operators import add

    nodeList = []

    # Example usage
    nodeList.append(Node(name="node0", address='0x0011', calType='uni', func='copy'))
    nodeList.append(Node(name="node1", address='0x0012', calType='uni', func='copy'))


    # Create data streams
    data_streams = DataStreams()
    data_streams.add_stream('stream0')
    data_streams.add_stream('stream1')

    # Add data to streams
    data_streams.add_data('stream0', 'data0', nodeList[0], 'left', '0x3F000000')
    data_streams.add_data('stream1', 'data1', nodeList[1], 'left', '0x3F000000')

    nodeList.append(add(nodeList[0], nodeList[1],'0x0013'))
    
    
    for node in nodeList :
        print(node)

    print("\n\n\n\n")
          
    print(data_streams)

    convert2Yaml(nodeList, data_streams, "test.yaml")

if __name__ == "__main__" :
    main()