import queue

class Node:
    def __init__(self, value = None, left = None, right = None):
        self._left = left
        self._right = right
        self._value = value
    
    def run(self):
        return self._value

    def display(self):
        print(self._left, self._right, self._value)

class AddNode(Node):
    def __init__(self, value = None, left = None, right = None):
        Node.__init__(self, value, left, right)
        self._domain = None

    def run(self):
        pass

class SubNode(Node):
    def __init__(self, value = None, left = None, right = None):
        Node.__init__(self, value, left, right)
        self._domain = None

    def run(self):
        pass

class MultiNode(Node):
    def __init__(self, value = None, left = None, right = None):
        Node.__init__(self, value, left, right)
        self._domain = None

    def run(self):
        pass

def priority(operator):
    if (operator == '-' or operator == '+'):
        return 0
    
    return 1

def convertStringToBaLan(string):
    stack = queue.LifoQueue()
    frontier = queue.Queue()
    for char in string:
        if ('A' <= char <= 'Z'):
            frontier.put(char)
        
        if (char == '(' or char == '*'):
            stack.put(char)

        if (char == ')'):
            getStack = stack.get()
            while (getStack != '('):
                frontier.put(getStack)

                if (not stack.empty()):
                    getStack = stack.get()
                else: break

        if (char == '+' or char == '-'):
            getStack = ''
            if (not stack.empty()):
                getStack = stack.get()

            while (getStack != '('):
                frontier.put(getStack)

                if (not stack.empty()):
                    getStack = stack.get()
                else:
                    break
            
            if (getStack == '('): stack.put('(')
            stack.put(char)
    while (not stack.empty()):
        frontier.put(stack.get())

    result = ''
    while (not frontier.empty()):
        result = result + frontier.get()

    return result
def subString(str):
    t = str.split('=')
    s = ''
    s = t[0]
    result = []
    temp = ''
    for i in range(len(s)):
        if s[i] == '+' or s[i] == '-' or s[i] == '*' or s[i] == '(' or s[i] == ')':
            result.append(temp)
            temp = ''
            result.append(s[i])
        else:
            temp+=s[i]
    result.append(temp)
    result = list(filter(lambda x: x != "", result))
    return result,t[1]       

if (__name__ == "__main__"):
    string = input("Nhap da thuc: ")
    arr, result = subString(string)
    print(arr)
    #balan = convertStringToBaLan(string)

    #print(balan)