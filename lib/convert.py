from lib.dataStruct import DataStreams
from lib.node import Node
from lib.toYaml import convert2Yaml
from lib.yaml2Machine import getProgram, getTokens
import yaml

def convert2Machine(nodeList: list[Node], dataStreams: DataStreams) -> bool:

    for node in nodeList :
        print(node)

    print("\n\n")
          
    print(dataStreams)

    print("\n\n\n\n")

    convert2Yaml(nodeList, dataStreams, "test.yaml")

    with open("test.yaml", 'r') as yml:
        ddp = yaml.safe_load(yml)   


    programLines = getProgram(ddp)
    with open("program.txt", 'w') as programFile:        
        for line in programLines.values() :
            programFile.write(line + "\n")


    tokens = getTokens(ddp)
    with open("tokens.txt", 'w') as programFile:        
        for line in tokens :
            programFile.write(line + "\n")

    return True