from dataclasses import dataclass
from numpy import uint16

@dataclass
class Const:
    flag: str | None = None
    value: uint16 | None = None

class Node:
    '''
    struct node :
        name: str
        address: 16'b
        calType: uni | bin
        func: key in func list
        goto : a list with left? and right?
            left :
                node: nodeName
                flag: left or right
            right :
                node: nodeName
                flag: left or right
        const :
            flag: left or right
            value: 16'b
    '''

    def __init__(self, name: str, address: str, calType: str, func: str, goto: dict | None = None, const: Const | None = None):
        self.name: str = name
        self.address: str = address  # 16-bit address
        self.calType: str = calType  # calculation type
        self.func: str = func  # Function key in function list
        self.goto: dict = goto if goto else {'left': {'node': None, 'flag': None}, 'right': {'node': None, 'flag': None}}
        self.const: Const | None = const if const else None

    def connect(self, direction: str, nodeName: str, flag: str):
        if direction in ['left', 'right']:
            self.goto[direction]['node'] = nodeName
            self.goto[direction]['flag'] = flag
        else:
            raise ValueError("Direction must be either 'left' or 'right'")

    def __repr__(self):
        return (f"Node(name={str(self.address)}, address={self.address}, calType={self.calType}, func={self.func}, "
                f"goto={{'left': {self.goto['left']}, 'right': {self.goto['right']}}})")