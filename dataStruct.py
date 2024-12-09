'''
data structure module

the format is :
    
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

This is a parallel model, when we input multiple data streams, they will be calculated parallely.

we need two class: DataStreams and Data 
'''

class Data:
    def __init__(self, value, node=None, flag=None):
        self.node = node  # Node associated with this data
        self.flag = flag  # Direction flag ('left' or 'right')
        self.value = value  # Value of the data

    def __repr__(self):
        return f"Data(node={str(self.node.address)}, flag={self.flag}, value={self.value})"


class DataStreams:
    def __init__(self):
        self.streams = {}  # Dictionary to hold multiple streams

    def add_stream(self, stream_name):
        if stream_name not in self.streams:
            self.streams[stream_name] = {}  # Add a new stream
        else:
            raise ValueError(f"Stream '{stream_name}' already exists.")

    def add_data(self, stream_name, data_name, node, flag, value):
        if stream_name in self.streams:
            if data_name not in self.streams[stream_name]:
                self.streams[stream_name][data_name] = Data(node=node, flag=flag, value=value)  # Add data to the stream
            else:
                raise ValueError(f"Data '{data_name}' already exists in stream '{stream_name}'.")
        else:
            raise ValueError(f"Stream '{stream_name}' does not exist.")

    def __repr__(self):
        streams_repr = "\n".join([f"{stream}: {data}" for stream, data in self.streams.items()])
        return f"DataStreams(\n{streams_repr}\n)"

def main () :
    from node import Node

    # Example usage
    node1 = Node(address='0x0011', calType='uni', func='getSign')
    node2 = Node(address='0x0012', calType='uni', func='cp0')

    # Create data streams
    data_streams = DataStreams()
    data_streams.add_stream('stream0')
    data_streams.add_stream('stream1')

    # Add data to streams
    data_streams.add_data('stream0', 'data0', node1, 'left', '0x3F000000')
    data_streams.add_data('stream1', 'data0', node2, 'left', '0x3F000000')

    print(data_streams)

if __name__ == "__main__" :
    main()