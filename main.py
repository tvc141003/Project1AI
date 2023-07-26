import queue

class Node:
    def __init__(self, value = None, left = None, right = None):
        self._left = left
        self._right = right
        self._value = value

    def getValue(self):
        return self._value
    
    def getLeft(self):
        return self._left
    
    def getRight(self):
        return self._right

    def run(self, result):
        lengthResult = len(result)
        lengthValue = len(self._value)
        value = 0
        for i in range(lengthValue):
            for j in range(lengthResult):
                if (self._value[i] == result[j][0]):
                    value += result[j][1] * (10 ** (lengthValue - i - 1))
        return value

    def display(self):
        print(self._left, self._right, self._value)

class AddNode(Node):
    def __init__(self, value = None, left = None, right = None):
        Node.__init__(self, value, left, right)

    def run(self, result):
        leftValue = self._left.run(result)
        rightValue = self._right.run(result)

        return leftValue + rightValue

    def display(self):
        print('+', self._value)

class SubNode(Node):
    def __init__(self, value = None, left = None, right = None):
        Node.__init__(self, value, left, right)

    def run(self, result):
        leftValue = self._left.run(result)
        rightValue = self._right.run(result)

        return leftValue - rightValue

    def display(self):
        print('-', self._value)

class MultiNode(Node):
    def __init__(self, value = None, left = None, right = None):
        Node.__init__(self, value, left, right)

    def run(self, result):
        leftValue = self._left.run(result)
        rightValue = self._right.run(result)

        return leftValue * rightValue

    def display(self):
        print('*', self._value)

class DivideNode(Node):
    def __init__(self, value = None, left = None, right = None):
        Node.__init__(self, value, left, right)

    def run(self, result):
        leftValue = self._left.run(result)
        rightValue = self._right.run(result)

        return leftValue / rightValue

    def display(self):
        print('/', self._value)

class IValueConverter():
    def __init__(self, object = ""):
        self._items = object

    def convert(self):
        pass

class BalanValueConverter(IValueConverter):
    def priority(operator):
        if (operator == '-' or operator == '+'):
            return 0
        
        return 1
    
    def convert(self):
        stack = queue.LifoQueue()
        frontier = queue.Queue()
        for item in self._items:

            if (item == '(' or item == '*'):
                stack.put(item)
            elif (item == ')'):
                getStack = stack.get()
                while (getStack != '('):
                    frontier.put(getStack)

                    if (not stack.empty()):
                        getStack = stack.get()
                    else: break
            elif (item == '+' or item == '-'):
                getStack = ''
                if (not stack.empty()):
                    getStack = stack.get()

                while (getStack != '(' and getStack != ""):
                    frontier.put(getStack)

                    if (not stack.empty()):
                        getStack = stack.get()
                    else:
                        break
                
                if (getStack == '('): stack.put('(')
                stack.put(item)
            else: frontier.put(item)
                
        while (not stack.empty()):
            frontier.put(stack.get())

        result = []
        while (not frontier.empty()):
            result.append(frontier.get())

        return result

class InputValueConverter(IValueConverter):
    def convert(self):
        t = self._items.split('=')
        s = t[0]
        result = []
        temp = ''
        for i in range(len(s)):
            if s[i] == '+' or s[i] == '-' or s[i] == '*' or s[i] == '(' or s[i] == ')' or s[i] == '/':
                result.append(temp)
                temp = ''
                result.append(s[i])
            else:
                temp+=s[i]
        result.append(temp)
        result = list(filter(lambda x: x != "", result))
        return result,t[1]    

class VariableValueConverter(IValueConverter):
    def convert(self):
        variable = []
        for i in self._items:
            if ('A' <= i <= 'Z'):
                item = [i, [True for _ in range(10)]]
                if (item not in variable):
                    variable.append(item)
        variable.sort()
        return variable

class Tree():
    def __init__(self, items = None):
        self._items = items

    def build(self):
        frontier = queue.LifoQueue()
        for item in self._items:
            if (item == '+'):

                right = frontier.get()
                left = frontier.get()
                node = AddNode(left = left, right = right)
                frontier.put(node)

            elif (item == '-'):

                right = frontier.get()
                left = frontier.get()
                node = SubNode(left = left, right = right)
                frontier.put(node)

            elif (item == '*'):

                right = frontier.get()
                left = frontier.get()
                node = MultiNode(left = left, right = right)
                frontier.put(node)

            else:
                node = Node(value = item)
                frontier.put(node)
        
        return frontier.get()
    
    def displayTree(self, tree):
        if (tree == None): return
        tree.display()
        self.displayTree(tree._left) 
        self.displayTree(tree._right) 

class Constraint():
    def __init__(self, items):
        self._items = items

    def setItem(self, items):
        self._items = items

    def check(self):
        pass

class AlldiffConstraint(Constraint):
    def check(self):
        lengthItems = len(self._items)
        for i in range(lengthItems):
            itemI = self._items[i][1]
            for j in range(i):
                itemJ = self._items[j][1]

                # Check all domain in I
                for k in range(10):
                    if (itemI[k] == False): continue
                    flag =  False   

                    # Each domain in I check any domain in J valid diff domain I
                    for l in range(10):
                        if (l != k and itemJ[l] == True):
                            flag = True
                            break
                    if (flag == False): return False, self._items[i][0], k

        return True, -1, -1

class DiffZeroConstraint(Constraint):
    def __init__(self, items, tree):
        self._items = items
        self._tree = tree
    
    def check(self):
        stack = queue.LifoQueue()
        stack.put(self._tree)
        while (not stack.empty()):
            node = stack.get()
            value = node.getValue()

            if (value != None):
                for item in self._items:
                    if (item[0] == value[0] and item[1][0] == True):
                        return False, item[0], 0
            else:
                stack.put(node.getLeft())
                stack.put(node.getRight())

        return True, -1, -1

class CSPSearch():
    def __init__(self, origin = None):
        converter = VariableValueConverter(origin)
        variable = converter.convert()
        
        converter = InputValueConverter(origin)
        arr, result = converter.convert()
        
        converter = BalanValueConverter(arr)
        balan = converter.convert()
        
        tree = Tree(balan).build()

        self._variable = variable
        self._leftValue = tree
        self._rightValue = Node(value = result)
        self._result = [[item[0], None] for item in variable]

        self._constraint = [AlldiffConstraint(variable), DiffZeroConstraint(variable, tree), DiffZeroConstraint(variable, self._rightValue)]

    def getLeftValue(self):
        return self._leftValuele

    def ArcConsistency(self):
        flag = True
        while (flag):
            flag = False
            for constraint in self._constraint:
                valid, letter, position = constraint.check()
                if (valid == False):
                    flag = True
                    for i in range(len(self._variable)):
                        if (self._variable[i][0] == letter):
                            self._variable[i][1][position] = False
        
    def forwardChecking(self, position, index):
        checkIndex = []
        for i in range(len(self._variable)):
            if (i == position or self._variable[i][1][index] == False): continue
            checkIndex.append([i, index])
            self._variable[i][1][index] = False

        return checkIndex
    
    def run(self, position):
        if (position == len(self._variable)):
            leftValue = self._leftValue.run(self._result)
            rightValue = self._rightValue.run(self._result)

            if (leftValue == rightValue):
                return self._result
            
            return "Cutoff"

        for i in range(10):
            if (self._variable[position][1][i] == True):
                self._result[position][1] = i
                checkIndex = self.forwardChecking(position, i)

                result = self.run(position + 1)
                if (result != "Cutoff"): return result 
                self._result[position][1] = None
                for item in checkIndex:
                    self._variable[item[0]][1][item[1]] = True

        return "Cutoff"

class BruteForceSearch():
    def __init__(self, origin = None):
        converter = VariableValueConverter(origin)
        variable = converter.convert()
        
        converter = InputValueConverter(origin)
        arr, result = converter.convert()
        
        converter = BalanValueConverter(arr)
        balan = converter.convert()
        
        tree = Tree(balan).build()

        self._variable = variable
        self._leftValue = tree
        self._rightValue = Node(value = result)
        self._result = [[item[0], None] for item in variable]
        self._letters = arr
        self._letters.append(result)

    def isValid(self):
        length = len(self._result)
        # Check all diff digit
        for i in range(length):
            for j in range(i):
                if (self._result[i][1] == self._result[j][1]):
                    return False
                
        # Check first digit diff Zero
        for i in range(length):
            item = self._result[i]
            if (item[1] != 0): continue

            for letter in self._letters:
                if ('A' <= letter[0] <= 'Z' and letter[0] == item[0]): return False

        # Check correct equation
        leftValue = self._leftValue.run(self._result)
        rightValue = self._rightValue.run(self._result)
        if (leftValue != rightValue): return False

        return True

    def run(self, position = 0):
        if (position == len(self._result)):
            if (self.isValid() == True): return self._result
            return "Cutoff"
        
        for i in range(10):
            self._result[position][1] = i
            result = self.run(position+1)
            if (result != "Cutoff"): return self._result
        

        return "Cutoff"

if (__name__ == "__main__"):
    fileIn = input("Nhap ten file: ")
    
    data = ''
    with open(fileIn, 'r') as file:
        data = file.read()
        file.close()
    
    cspSearch = CSPSearch(data)
    cspSearch.ArcConsistency()
    cspResult = cspSearch.run(0)

    result = ''
    if (cspResult == "Cutoff"):
        result = "NO SOLUTION"
    else:
        for item in cspResult:
            result = f'{result}{item[1]}'

    fileOut = fileIn.replace('input', 'output')
    with open(fileOut, 'w') as file:
        file.write(result)
        file.close()

    # bruteForceSearch = BruteForceSearch(data)
    # bruteForceResult = bruteForceSearch.run(0)


    # print(bruteForceResult)