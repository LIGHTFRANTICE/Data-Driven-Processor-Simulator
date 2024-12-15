from node import Node

def isValidNodeList(nodeList: list[Node]) -> None:
    if nodeList[-1].func != "out" :
        raise ValueError("The last node must be output!!")
    
    if nodeList[0].address != "0x0000":
        raise ValueError(f"The first node should located in 0x0000, but now it is in {nodeList[0].address}")
    
    for node in nodeList[:-1]:
        if node.goto is None:
            raise ValueError(f"Node {node.name} should connect to another Node!!")
        if node.goto['left']['node'] is None and  node.goto['right']['node'] is None:
            raise ValueError(f"Node {node.name} should connect to another Node!!")
    

def isValidDataStream(dataStream: dict) -> None:
    pass
