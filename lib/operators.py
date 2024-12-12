from lib.node import Node
from lib.dataStruct import Data

def isValiable(x: Node) -> bool:
    outputPortDict = {
        'add' : 1,
        'sub' : 1,
        'mul' : 1,
        'shift-l' : 1,
        'shift-r' : 1,
        'and' : 1,
        'or' : 1,
        'not' : 1,
        'sw' : 2,
        'eq' : 1,
        'geq' : 1,
        'gen_get' : 1,
        'gen_set' : 1,
        'out' : 1,
        'copy' : 2
    }

    if x.func in outputPortDict.keys():
        if outputPortDict[x.func] == 1 and x.goto["left"]["node"] is not None:
            return False
        elif outputPortDict[x.func] == 2 and x.goto["left"]["node"] is not None and x.goto["right"]["node"] is not None:
            return False
        else:
            return True
    else:
        raise ValueError(f"Node {x.name} includes an unsupported operator {x.func}!")

def add(x: Node | Data, y: Node | Data, address: str) -> Node:

    name = address
    adder = Node(name, address, calType="bin", func="add")
    
    if isinstance(x, Node):
        if not isValiable(x):
            raise ValueError(
                    f"{x.name} is a full node, it can't be connectted to an adder!!")
        if isinstance(y, Node):
            if not isValiable(y):
                raise ValueError(
                    f"{y.name} is a full node, it can't be connectted to an adder!!")

            if x.goto["left"]["node"] is None:
                x.connect("left", adder.name, "left")
            elif x.goto["right"]["node"] is None:
                x.connect("right", adder.name, "left")
            else:
                raise ValueError(
                    f"{x.name} is a full node, it can't be connectted to an adder!!")

            if y.goto["left"]["node"] is None:
                y.connect("left", adder.name, "right")
            elif y.goto["right"]["node"] is None:
                y.connect("right", adder.name, "right")
            else:
                raise ValueError(
                    f"{y.name} is a full node, it can't be connectted to an adder!!")

        if isinstance(y, Data):

            if y.node is not None:
                raise ValueError(
                    f"{y} is a used data, it can't be connectted to an adder!!")

            if x.goto["left"]["node"] is None:
                x.connect("left", adder.name, "left")
            elif x.goto["right"]["node"] is None:
                x.connect("right", adder.name, "left")
            else:
                raise ValueError(
                    f"{x.name} is a full node, it can't be connectted to an adder!!")

            y.node = adder.name
            y.flag = "right"

    if isinstance(x, Data):
        if isinstance(y, Node):

            if x.node is not None:
                raise ValueError(
                    f"{x} is a used data, it can't be connectted to an adder!!")

            if not isValiable(y):
                raise ValueError(
                    f"{y.name} is a full node, it can't be connectted to an adder!!")

            x.node = adder.name
            x.flag = "left"

            if y.goto["left"]["node"] is None:
                y.connect("left", adder.name, "right")
            elif y.goto["right"]["node"] is None:
                y.connect("right", adder.name, "right")
            else:
                raise ValueError(
                    f"{y.name} is a full node, it can't be connectted to an adder!!")

        if isinstance(y, Data):
            if x.node is not None:
                raise ValueError(
                    f"{x} is a used data, it can't be connectted to an adder!!")

            if y.node is not None:
                raise ValueError(
                    f"{y} is a used data, it can't be connectted to an adder!!")

            x.node = adder.name
            x.flag = "left"

            y.node = adder.name
            y.flag = "right"

    return adder

def sub(x: Node | Data, y: Node | Data, address: str) -> Node:

    name = address
    subNode = Node(name, address, calType="bin", func="sub")
    
    if isinstance(x, Node):
        if not isValiable(x):
            raise ValueError(
                    f"{x.name} is a full node, it can't be connectted to a sub node!!")
        
        if isinstance(y, Node):

            if not isValiable(y):
                raise ValueError(
                    f"{y.name} is a full node, it can't be connectted to a sub node!!")

            if x.goto["left"]["node"] is None:
                x.connect("left", subNode.name, "left")
            elif x.goto["right"]["node"] is None:
                x.connect("right", subNode.name, "left")
            else:
                raise ValueError(
                    f"{x.name} is a full node, it can't be connectted to a sub node!!")

            if y.goto["left"]["node"] is None:
                y.connect("left", subNode.name, "right")
            elif y.goto["right"]["node"] is None:
                y.connect("right", subNode.name, "right")
            else:
                raise ValueError(
                    f"{y.name} is a full node, it can't be connectted to a sub node!!")

        if isinstance(y, Data):

            if y.node is not None:
                raise ValueError(
                    f"{y} is a used data, it can't be connectted to a sub node!!")

            if x.goto["left"]["node"] is None:
                x.connect("left", subNode.name, "left")
            elif x.goto["right"]["node"] is None:
                x.connect("right", subNode.name, "left")
            else:
                raise ValueError(
                    f"{x.name} is a full node, it can't be connectted to a sub node!!")

            y.node = subNode.name
            y.flag = "right"

    if isinstance(x, Data):
        if isinstance(y, Node):

            if x.node is not None:
                raise ValueError(
                    f"{x} is a used data, it can't be connectted to a sub node!!")

            if not isValiable(y):
                raise ValueError(
                    f"{y.name} is a full node, it can't be connectted to a sub node!!")

            x.node = subNode.name
            x.flag = "left"

            if y.goto["left"]["node"] is None:
                y.connect("left", subNode.name, "right")
            elif y.goto["right"]["node"] is None:
                y.connect("right", subNode.name, "right")
            else:
                raise ValueError(
                    f"{y.name} is a full node, it can't be connectted to a sub node!!")

        if isinstance(y, Data):
            if x.node is not None:
                raise ValueError(
                    f"{x} is a used data, it can't be connectted to a sub node!!")

            if y.node is not None:
                raise ValueError(
                    f"{y} is a used data, it can't be connectted to a sub node!!")

            x.node = subNode.name
            x.flag = "left"

            y.node = subNode.name
            y.flag = "right"

    return subNode

def main():

    from lib.dataStruct import DataStreams

    nodeList = []

    # Example usage
    nodeList.append(Node(name="node0", address='0x0011',
                    calType='uni', func='copy'))
    nodeList.append(Node(name="node1", address='0x0012',
                    calType='uni', func='copy'))

    # Create data streams
    data_streams = DataStreams()
    data_streams.add_stream('stream0')
    data_streams.add_stream('stream1')

    # Add data to streams
    data_streams.add_data('stream0', 'data0',
                          nodeList[0].name, 'left', '0x3F000000')
    data_streams.add_data('stream1', 'data1',
                          nodeList[1].name, 'left', '0x3F000000')
    data_streams.add_data('stream1', 'data2', value="0xFF")
    data_streams.add_data('stream1', 'data3', value="0xFF")

    nodeList.append(add(nodeList[0], nodeList[1], '0x0013'))
    nodeList.append(sub(nodeList[2], data_streams.streams["stream1"]["data2"], '0x0014'))
    nodeList.append(sub(nodeList[2], data_streams.streams["stream1"]["data3"], '0x0015'))


    for node in nodeList:
        print(node)

    print("\n\n\n\n")

    print(data_streams)


if __name__ == "__main__":
    main()
