from lib.node import Node
from lib.dataStruct import Data
from typing import Literal

def IsSingleOprType(funcName: str) -> bool:
    singleTypeList = ['not', 'gen_get', 'out', 'copy']

    if funcName in singleTypeList:
        return True
    else:
        return False

def isValiable(x: Node | Data) -> bool:
    if isinstance(x, Data):
        if x.node is not None:
            return False
        else:
            return True
    else:
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

def addNode(
        x: Node | Data, 
        y: Node | Data, 
        address: str, 
        operator: Literal[
            'add',
            'sub',
            'mul',
            'shift-l',
            'shift-r',
            'and',
            'or',
            'not',
            'sw',
            'eq',
            'geq',
            'gen_get',
            'gen_set',
            'out',
            'copy']
    ) -> Node:
    name = address
    oprNode = Node(name, address, calType=('uni' if IsSingleOprType(operator) else 'bin'), func=operator)

    if isinstance(x, Node):
        if not isValiable(x):
            raise ValueError(
                    f"{x.name} is a full node, it can't be connectted to an adder!!")
        if isinstance(y, Node):
            if not isValiable(y):
                raise ValueError(
                    f"{y.name} is a full node, it can't be connectted to an adder!!")

            if x.goto["left"]["node"] is None:
                x.connect("left", oprNode.name, "left")
            elif x.goto["right"]["node"] is None:
                x.connect("right", oprNode.name, "left")
            else:
                raise ValueError(
                    f"{x.name} is a full node, it can't be connectted to an adder!!")

            if y.goto["left"]["node"] is None:
                y.connect("left", oprNode.name, "right")
            elif y.goto["right"]["node"] is None:
                y.connect("right", oprNode.name, "right")
            else:
                raise ValueError(
                    f"{y.name} is a full node, it can't be connectted to an adder!!")

        if isinstance(y, Data):

            if y.node is not None:
                raise ValueError(
                    f"{y} is a used data, it can't be connectted to an adder!!")

            if x.goto["left"]["node"] is None:
                x.connect("left", oprNode.name, "left")
            elif x.goto["right"]["node"] is None:
                x.connect("right", oprNode.name, "left")
            else:
                raise ValueError(
                    f"{x.name} is a full node, it can't be connectted to an adder!!")

            y.node = oprNode.name
            y.flag = "right"

    if isinstance(x, Data):
        if isinstance(y, Node):

            if x.node is not None:
                raise ValueError(
                    f"{x} is a used data, it can't be connectted to an adder!!")

            if not isValiable(y):
                raise ValueError(
                    f"{y.name} is a full node, it can't be connectted to an adder!!")

            x.node = oprNode.name
            x.flag = "left"

            if y.goto["left"]["node"] is None:
                y.connect("left", oprNode.name, "right")
            elif y.goto["right"]["node"] is None:
                y.connect("right", oprNode.name, "right")
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

            x.node = oprNode.name
            x.flag = "left"

            y.node = oprNode.name
            y.flag = "right"

    return oprNode

def add(x: Node | Data, y: Node | Data, address: str) -> Node:

    return addNode(x, y, address, operator='add')

def sub(x: Node | Data, y: Node | Data, address: str) -> Node:

    return addNode(x, y, address, operator='sub')
    
def mul(x: Node | Data, y: Node | Data, address: str) -> Node:

    return addNode(x, y, address, operator='mul')

def shift_l(x: Node | Data, y: Node | Data, address: str) -> Node:

    return addNode(x, y, address, operator='shift-l')

def shift_r(x: Node | Data, y: Node | Data, address: str) -> Node:

    return addNode(x, y, address, operator='shift-r')

def andByBit(x: Node | Data, y: Node | Data, address: str) -> Node:

    return addNode(x, y, address, operator='and')

def orByBit(x: Node | Data, y: Node | Data, address: str) -> Node:

    return addNode(x, y, address, operator='or')

def notByBit(x: Node | Data, y: Node | Data, address: str) -> Node:

    return addNode(x, y, address, operator='not')

# def sw(x: Node | Data, y: Node | Data, address: str) -> Node:

#     return addNode(x, y, address, operator='sw')

def eq(x: Node | Data, y: Node | Data, address: str) -> Node:

    return addNode(x, y, address, operator='eq')

def geq(x: Node | Data, y: Node | Data, address: str) -> Node:

    return addNode(x, y, address, operator='geq')

def genGet(x: Node | Data, y: Node | Data, address: str) -> Node:

    return addNode(x, y, address, operator='gen_get')

def genSet(x: Node | Data, y: Node | Data, address: str) -> Node:

    return addNode(x, y, address, operator='gen_set')

def copy(x: Node | Data, address: str) -> Node:
    name = address
    oprNode = Node(name, address, calType='uni', func='copy')

    if isinstance(x, Node):
        if not isValiable(x):
            raise ValueError(
                    f"{x.name} is a full node, it can't be connectted to another Node!!")

        if x.goto["left"]["node"] is None:
            x.connect("left", oprNode.name, "left")
        elif x.goto["right"]["node"] is None:
            x.connect("right", oprNode.name, "left")
        else:
            raise ValueError(
                f"{x.name} is a full node, it can't be connectted to another Node!!")

    if isinstance(x, Data):
            if x.node is not None:
                raise ValueError(
                    f"{x} is a used data, it can't be connectted to a Node!!")
            
            x.node = oprNode.name
            x.flag = "left"

    return oprNode

def out(x: Node | Data, address: str) -> Node:
    name = address
    oprNode = Node(name, address, calType='uni', func='out')

    if isinstance(x, Node):
        if not isValiable(x):
            raise ValueError(
                    f"{x.name} is a full node, it can't be connectted to another Node!!")

        if x.goto["left"]["node"] is None:
            x.connect("left", oprNode.name, "left")
        elif x.goto["right"]["node"] is None:
            x.connect("right", oprNode.name, "left")
        else:
            raise ValueError(
                f"{x.name} is a full node, it can't be connectted to another Node!!")

    if isinstance(x, Data):
            if x.node is not None:
                raise ValueError(
                    f"{x} is a used data, it can't be connectted to a Node!!")
            
            x.node = oprNode.name
            x.flag = "left"

    return oprNode

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
