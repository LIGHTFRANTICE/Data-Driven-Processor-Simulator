'''
Integers Module
'''
from node import Node
from dataStruct import Data

def add (x: Node | Data, y: Node | Data, address: str) -> Node :
    if isinstance(x, Node) :
        if isinstance(y, Node) :
            if (x.goto["left"]["node"] != None and x.goto["right"]["node"] != None):
                raise ValueError(f"{x} is a full node, it can't be connectted to an adder!!")
            
            if (y.goto["left"]["node"] != None and y.goto["right"]["node"] != None):
                raise ValueError(f"{y} is a full node, it can't be connectted to an adder!!")
            
            name = address
            adder = Node(name, address, calType="bin", func="add")
            
            if x.goto["left"]["node"] == None :
                x.connect("left", adder.name, "left")
            elif x.goto["right"]["node"] == None :
                x.connect("right", adder.name, "left")
            else :
                raise ValueError(f"{x} is a full node, it can't be connectted to an adder!!")
            
            if y.goto["left"]["node"] == None :
                y.connect("left", adder.name, "right")
            elif y.goto["right"]["node"] == None :
                y.connect("right", adder.name, "right")
            else :
                raise ValueError(f"{y} is a full node, it can't be connectted to an adder!!")
        
        if isinstance(y, Data) :
            if (x.goto["left"]["node"] != None and x.goto["right"]["node"] != None):
                raise ValueError(f"{x} is a full node, it can't be connectted to an adder!!")
            
            if y.node != None :
                raise ValueError(f"{y} is a used data, it can't be connectted to an adder!!")
            
            name = address
            adder = Node(address, calType="bin", func="add")

            if x.goto["left"]["node"] == None :
                x.connect("left", adder.name, "left")
            elif x.goto["right"]["node"] == None :
                x.connect("right", adder.name, "left")
            else :
                raise ValueError(f"{x} is a full node, it can't be connectted to an adder!!")
            
            y.node = adder.name
            y.flag = "right"
    
    if isinstance(x, Data) :
        if isinstance(y, Node) :

            if x.node != None:
                raise ValueError(f"{x} is a used data, it can't be connectted to an adder!!")
            
            if (y.goto["left"]["node"] != None and y.goto["right"]["node"] != None):
                raise ValueError(f"{y} is a full node, it can't be connectted to an adder!!")
            
            name = address
            adder = Node(address, calType="bin", func="add")
            
            x.node = adder.name
            x.flag = "left"

            if y.goto["left"]["node"] == None :
                y.connect("left", adder.name, "right")
            elif y.goto["right"]["node"] == None :
                y.connect("right", adder.name, "right")
            else :
                raise ValueError(f"{y} is a full node, it can't be connectted to an adder!!")
        
        if isinstance(y, Data) :
            if x.node != None:
                raise ValueError(f"{x} is a used data, it can't be connectted to an adder!!")
            
            if y.node != None :
                raise ValueError(f"{y} is a used data, it can't be connectted to an adder!!")
            
            name = address
            adder = Node(address, calType="bin", func="add")

            x.node = adder.name
            x.flag = "left"
            
            y.node = adder.name
            y.flag = "right"
        
    return adder

def main () :

    from dataStruct import DataStreams

    nodeList = []

    # Example usage
    nodeList.append(Node(name="node0", address='0x0011', calType='uni', func='cp'))
    nodeList.append(Node(name="node1", address='0x0012', calType='uni', func='cp'))


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

if __name__ == "__main__" :
    main()