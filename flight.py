class Flight:
    def __init__(self, flight_no, start_city, departure_time, end_city, arrival_time, fare):
        """ Class for the flights

        Args:
            flight_no (int): Unique ID of each flight
            start_city (int): The city no. where the flight starts
            departure_time (int): Time at which the flight starts
            end_city (int): The city no where the flight ends
            arrival_time (int): Time at which the flight ends
            fare (int): The cost of taking this flight
        """
        self.flight_no = flight_no
        self.start_city = start_city
        self.departure_time = departure_time
        self.end_city = end_city
        self.arrival_time = arrival_time
        self.fare = fare


"""
If there are n flights, and m cities:

1. Flight No. will be an integer in {0, 1, ... n-1}
2. Cities will be denoted by an integer in {0, 1, .... m-1}
3. Time is denoted by a non negative integer - we model time as going from t=0 to t=inf
"""

class Heap:
    def __init__(self, comparison_function, init_array):
        self.init_array = init_array
        self.comparator = comparison_function
        # Write your code here
        if self.init_array:
            for i in range((len(self.init_array) - 2) // 2, -1, -1):
                self._downheap(i)
        pass

    def insert(self, value):
        self.init_array.append(value)
        self._upheap(len(self.init_array)-1)
        return

    def extract(self):
        if len(self) == 0:
            return None
        self._swap(0, len(self) - 1)
        element = self.init_array.pop()
        self._downheap(0)
        return element

    def top(self):
        if len(self.init_array) == 0:
            return None
        return self.init_array[0]

    def __len__(self):
        return len(self.init_array)

    def _parent(self,index):
        return (index-1)//2

    def _left(self,index):
        return 2*index + 1

    def _right(self,index):
        return 2*index + 2

    def _has_left(self,index):
        return self._left(index) < len(self.init_array)

    def _has_right(self,index):
        return  self._right(index) < len(self.init_array)

    def _swap(self, index1, index2):
        self.   init_array[index1], self.init_array[index2] = self.init_array[index2], self.init_array[index1]

    def _upheap(self, index):
        parent = self._parent(index)
        if index > 0 and self.comparator(self.init_array[index], self.init_array[parent]):
            self._swap(index, parent)
            self._upheap(parent)

    def _downheap(self, index):
        if self._has_left(index):
            left = self._left(index)
            small_child = left
            if self._has_right(index):
                right = self._right(index)
                if self.comparator(self.init_array[right], self.init_array[left]):
                    small_child = right
            if self.comparator(self.init_array[small_child], self.init_array[index]):
                self._swap(index, small_child)
                self._downheap(small_child)
                self._downheap(small_child)



class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedQueue:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def pop(self):
        if not self.head:
            return None
        data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return data

    def is_empty(self):
        return self.head is None
