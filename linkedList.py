class Node() :
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList():
    def __init__(self):
        self.head = None

    def insert(self, data):
        node = Node(data)
        if self.head == None:
            self.head = node
            return
        curr = self.head
        while(curr.next != None):
            curr = curr.next
        curr.next = node
    
    def pop(self) -> int:
        # removing the head because the head is smallest available frame
        next_node = self.head.next
        data = self.head.data
        self.head = next_node
        return data

    def remove(self, data):
        curr = self.head
        if curr != None and curr.data == data:
            self.head = curr.next
            return

        prev = None
        while curr != None and curr.data != data:
            prev = curr
            curr = curr.next

        if curr == None:
            return
    
        prev.next = curr.next