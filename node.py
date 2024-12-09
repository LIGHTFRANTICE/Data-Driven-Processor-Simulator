

class Node:
    '''
    node can connect to another node

    struct node :
        name
        address, //16'b
        calType, // uni | bin
        func, //key in func list
        goto : //a list with left? and right?
            left :
                node,
                flag,
            right :
                node,
                flag,
    '''

    def __init__(self, name, address, calType, func, goto=None):
        self.name = name
        self.address = address  # 16-bit address
        self.calType = calType  # calculation type
        self.func = func  # Function key in function list
        self.goto = goto if goto else {'left': {'node': None, 'flag': None}, 'right': {'node': None, 'flag': None}}

    def connect(self, direction: str, nodeName: str, flag: str):
        if direction in ['left', 'right']:
            self.goto[direction]['node'] = nodeName
            self.goto[direction]['flag'] = flag
        else:
            raise ValueError("Direction must be either 'left' or 'right'")

    def __repr__(self):
        return (f"Node(name={str(self.address)}, address={self.address}, calType={self.calType}, func={self.func}, "
                f"goto={{'left': {self.goto['left']}, 'right': {self.goto['right']}}})")