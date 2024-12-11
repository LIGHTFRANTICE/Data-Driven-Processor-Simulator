'''
Definition of data stream struct
'''

from dataclasses import dataclass
from node import Node

@dataclass
class Data:
    '''
    Data:
        node: Node associated with this data
        flag: Direction flag ('left' or 'right')
        value: Value of the data
    '''
    node : str | None = None
    flag : str | None = None
    value: str | None = None


class DataStreams:
    '''
    streams :
        stream0 :
            data0 :
                node : cp0
                flag : left
                value : 0x3F000000
            ...    
        stream1 :
            data0 :
                node : cp0
                flag : left
                value : 0x3F000000            
            ...       
        ...
    '''
    def __init__(self):
        self.streams = {}  # Dictionary to hold multiple streams

    def add_stream(self, stream_name: str):
        if stream_name not in self.streams:
            self.streams[stream_name] = {}  # Add a new stream
        else:
            raise ValueError(f"Stream '{stream_name}' already exists.")

    def add_data(self, stream_name: str, data_name: str, node_name: str | None = None, flag: str | None = None, value: str | None = None):
        if stream_name in self.streams:
            if data_name not in self.streams[stream_name]:
                self.streams[stream_name][data_name] = Data(node=node_name, flag=flag, value=value)
            else:
                raise ValueError(f"Data '{data_name}' already exists in stream '{stream_name}'.")
        else:
            raise ValueError(f"Stream '{stream_name}' does not exist.")

    def __repr__(self):
        streams_repr = "\n".join([f"{stream}: {data}" for stream, data in self.streams.items()])
        return f"DataStreams(\n{streams_repr}\n)"

def main () :
    '''
    module test
    '''
    # Example usage
    node1 = Node(name="node0", address='0x0011', calType='uni', func='getSign')
    node2 = Node(name="node1", address='0x0012', calType='uni', func='cp0')

    # Create data streams
    data_streams = DataStreams()
    data_streams.add_stream('stream0')
    data_streams.add_stream('stream1')

    # Add data to streams
    data_streams.add_data('stream0', 'data0', node1.name, 'left', '0x3F000000')
    data_streams.add_data('stream1', 'data0', node2.name, 'left', '0x3F000000')

    print(data_streams)

if __name__ == "__main__" :
    main()
