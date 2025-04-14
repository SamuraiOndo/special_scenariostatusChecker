from binary_reader import BinaryReader
from readBin import getChaptersAndStates
import sys

CONDITIONS = ['NONE', 'AND', 'OR']
#thank you ret-hz for the C# loading code this is based on
def read_scenario_status(reader):
    reader.set_endian('little')
    scenario_status = {}
    scenario_status['scenario_category'] = reader.read_int16()
    scenario_status['expected_result'] = (scenario_status['scenario_category'] & 0x8000) != 0
    scenario_status['scenario_category'] &= 0x7FFF
    scenario_status['scenario_state'] = reader.read_int16()

    try: 
        next_condition = reader.read_int32()
        if next_condition != -1:  
            scenario_status['next_condition'] = ((CONDITIONS[next_condition * -1 - 1]), read_scenario_status(reader))
    except:
        scenario_status['next_condition'] = None
    
    return scenario_status

# def pretty_print(scenario_status, indent=0):
#     prefix = '\t' * indent
#     print(f"{prefix}Scenario Category: {scenario_status['scenario_category']}")
#     print(f"{prefix}Expected Result: {scenario_status['expected_result']}")
#     print(f"{prefix}Scenario State: {scenario_status['scenario_state']}")
#     if scenario_status['next_condition']:
#         print(f"{prefix + '\t'}Next Condition: {scenario_status['next_condition'][0]}")
#         pretty_print(scenario_status['next_condition'][1], indent + 1)

def printNeededChapters(scenario_status, nodes, passThrough = 0):
    if (passThrough == 0):
        print('Chapter: ',end='')
    print(f'{nodes[scenario_status['scenario_category']][0]}',end=' ')
    if scenario_status['next_condition']:
        print(f'and ',end='')
        passThrough += 1
        printNeededChapters(scenario_status['next_condition'][1],nodes,passThrough)

def printNeededScenarios(scenario_status, nodes, passThrough=0):
    if passThrough == 0:
        print('Scenario State: ', end='')
    prefix = "NOT " if not scenario_status.get('expected_result', True) else ""
    print(f'{prefix}{nodes[scenario_status["scenario_category"]][1][scenario_status["scenario_state"]]}', end=' ')
    if scenario_status['next_condition']:
        print(f'{scenario_status["next_condition"][0]} ', end='')
        passThrough += 1
        printNeededScenarios(scenario_status['next_condition'][1], nodes, passThrough)

def prettyPrint(scenario_status, nodes):
    printNeededChapters(scenario_status,nodes)
    print()
    printNeededScenarios(scenario_status,nodes)
    print()
byteString = sys.argv[1]
bytesObject = bytes.fromhex(byteString)

nodes = getChaptersAndStates()
prettyPrint(read_scenario_status(BinaryReader(bytesObject)),nodes)
