class Node:
    def __init__(self,data):
        self.data = data
        self.next = None 
class Solution: 
    def display(self,head):
        current = head
        while current:
            print(current.data,end=' ')
            current = current.next

    def insert(self,head,data): 
        new_node = Node(data)
        if (head == None) : # starting a new list
            return new_node # return new node as head
        # iterate through linked list
        current_node = head
        while (current_node.next != None) : # current_node is not last node
            current_node = current_node.next
        # insert node at the end of linked list
        current_node.next = new_node # set next pointer to new node
        return head

mylist= Solution()
T=int(input())
head=None
for i in range(T):
    data=int(input())
    head=mylist.insert(head,data)    
mylist.display(head);