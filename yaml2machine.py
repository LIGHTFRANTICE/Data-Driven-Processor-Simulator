import yaml
import sys

def getNodeAddr (ddpDict: dict, nodeName: str) -> str:
    if nodeName == 'output' :
        return '0'*16
    elif nodeName in ddpDict['nodes'] :
        return format(ddpDict['nodes'][nodeName]['address'], '016b')
    else :
        raise ValueError(f"Node {nodeName} do not exist !!")

def getNodeOprType (ddpDict: dict, nodeName: str) -> str:
    if nodeName == 'output' :
        return '0'
    elif nodeName in ddpDict['nodes'] :
        if ddpDict['nodes'][nodeName]['calType'] == 'uni' :
            return '1'
        elif ddpDict['nodes'][nodeName]['calType'] == 'bin' :
            return '0'
        else :
            raise ValueError(f"Wrong Oparator Type: {ddpDict[nodeName]['calType']} is setted in node: {nodeName} !!")
    else :
        raise ValueError(f"Node {nodeName} do not exist !!")

def getGoto (ddpDict: dict, goToDict: dict) -> str:
    if not goToDict:
        flag = '0'
        addr = '0'*16
        oprType = '0'
        direction = '0'
    else :

        if goToDict['node'] == 'output' :
            flag = '1'
            addr = '0'*16
            oprType = '0'
            direction = '0'
        else :
            flag = '1'
            addr = getNodeAddr(ddpDict, goToDict['node'])
            oprType = getNodeOprType(ddpDict, goToDict['node'])

            if goToDict['flag']=='left' :
                direction = '0'
            elif goToDict['flag']=='right' :
                direction = '1'
            else :
                raise ValueError("The flag set in goto is invaliable !!")

    return flag + '_' + addr + '_' + oprType + '_' + direction

def getConst (constDict: dict) -> str :
    if not constDict :
        flag = '0'
        direction = '0'
        value = '0'*16
    else :
        flag = '1'
        if constDict['flag']=='left' :
            direction = '0'
        elif constDict['flag']=='right' :
            direction = '1'
        else :
            raise ValueError("The flag set in const is invaliable !!")
        value = format(constDict['value'], '016b')
    
    return flag + '_' + direction + '_' + value

def funcMap (func : str) -> str :
    funcDic = {
        'add' : '0000',
        'sub' : '0001',
        'mul' : '0010',
        'shift-l' : '0011',
        'shift-r' : '0100',
        'and' : '0101',
        'or' : '0110',
        'not' : '0111',
        'sw' : '1000',
        'eq' : '1001',
        'geq' : '1010',
        'gen_get' : '1011',
        'gen_set' : '1100',
        'out' : '1110',
        'copy' : '1111'
    }

    if func in funcDic :
        return funcDic[func]
    else :
        raise ValueError(f"The function {func} is not supported !!")

def getProgram (ddp: dict) -> dict :
    programLines = {}
    for node in ddp['nodes'].values():
        address = node['address']
        func = funcMap(node['func'])

        if 'left' in node['goto'] : 
            leftCode = getGoto(ddp, node['goto']['left'])
        else :
            leftCode = getGoto(ddp, None)
            
        if 'right' in node['goto'] :
            rightCode = getGoto(ddp, node['goto']['right'])
        else :
            rightCode = getGoto(ddp, None)
        
        if 'const' in node:
            constCode = getConst(node['const'])
        else :
            constCode = getConst(None)

        totalProgramLine = func + '_' + leftCode + '_' + rightCode + '_' + constCode
        programLines[address] = totalProgramLine
    
    outputCode = funcMap('out') + '_1_' + '0'*16 + '_0_0_0_' + '0'*16 + '_0_0_0_0_' + '0'*16
    programLines[10000] = outputCode
    programLines = dict(sorted(programLines.items()))
    return programLines
        
def getTokens (ddp: dict) -> list :
    tokens = []
    color = 0
    for stream in ddp['streams'].values() :
        colorCode = format(color, '012b')
        color = color + 1

        for data in stream.values() :
            address = getNodeAddr(ddp, data['node'])
            oprType = getNodeOprType(ddp, data['node'])
            if data['flag']=='left' :
                direction = '0'
            elif data['flag']=='right' :
                direction = '1'
            else :
                raise ValueError(f"The flag set in {stream}.{data} is invaliable !!")
            
            value = format(data['value'], '032b')

            token = address + '_' + direction + '_' + oprType + '_' + colorCode + '_' + value
            tokens.append(token)
    
    return tokens

def main() :
    with open(sys.argv[1], 'r') as yml:
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

if __name__ == '__main__' :
    main()
