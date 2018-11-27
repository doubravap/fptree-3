#%%
#coding:utf-8
import csv
import copy
class treeNode:
    def __init__(self, nameValue, num, parentNode):
        self.name = nameValue           #存放节点名字
        self.count = num                #用于计数
        self.nodeLink = None            #用于连接相似结点（箭头）
        self.parent = parentNode        #用于存放父节点
        self.children = {}              #存放儿子节点

    def add(self, num):
        self.count += num

def getData():
    getData = []
    Data = csv.reader(open('/home/joker/Downloads/MSBD5002_Assignment_1/groceries.csv','r'))
    for line in Data:
        while '' in line:
            line.remove('')
        getData.append(line)
    return getData

def FormatData(dataSet):  
    forzendata = {}  
    for lines in dataSet:  
        forzendata[frozenset(lines)] = forzendata.get(frozenset(lines), 0) + 1 
        #frozenset是冻结的集合，它是不可变的，存在哈希值，好处是它可以作为字典的key，也可以作为其它集合的元素。
        #若没有相同事项，则为1；若有相同事项，则加1  
    return forzendata

def createTree(dataSet, minSup):
    '''
    创建FP树
    '''
    headerTable = {}
    freqItemDict = {}
    for lines in dataSet:
        for item in lines:
            headerTable[item] = headerTable.get(item, 0) + dataSet[lines]
            #dict.get(key, default=None)
    for i in list(headerTable.keys()):
        if headerTable[i]<minSup:
            del(headerTable[i])
    headerTable=dict(sorted(headerTable.items(), key=lambda item: (item[1], item[0]), reverse=True))
    for i in list(headerTable.keys()):
    #字典在遍历时不能进行修改，建议转成列表或集合处理
        freqItemDict=headerTable.keys()
    if len(freqItemDict) == 0: 
        return None,None
    #如果没有元素项满足要求，则退出
    for k in headerTable:
        headerTable[k] = [headerTable[k], None] ##element:[count,node]
    root= treeNode('Null Set', 1, None) #创建树的根结点
    for line, count in dataSet.items():  
        #def items() D.items() -> a set-like object providing a view on D's items
        newline = {}
        for item in line: 
            if item in freqItemDict:
                newline[item] = headerTable[item][0]
        if len(newline) > 0:
            orderedItems = [v[0] for v in sorted(newline.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, root, headerTable, count)#将排序后的item集合填充的树中
    return root,headerTable 

def updateTree(items, Tree, headerTable, count):
    if items[0] in Tree.children:#检查第一个元素项是否作为子节点存在
        Tree.children[items[0]].add(count) 
    else:   #	创建新的分支
        Tree.children[items[0]] = treeNode(items[0], count, Tree)
        if headerTable[items[0]][1] == None: 
            headerTable[items[0]][1] = Tree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], Tree.children[items[0]])
    if len(items) > 1:#每次都从列表中的第二个元素开始
        updateTree(items[1::], Tree.children[items[0]], headerTable, count)

#更新表头
def updateHeader(node, targetNode):
    while (node.nodeLink != None):    
        node = node.nodeLink
    node.nodeLink = targetNode

#找到结点的父节点一直到根
def findTree(leafNode, Path): 
    if leafNode.parent != None:
        Path.append(leafNode.name)
        findTree(leafNode.parent, Path)
        
#找到所有路径
def findPath(basePat, treeNode): 
    condPats = {}
    while treeNode != None:
        Path = []
        findTree(treeNode, Path)
        if len(Path) > 1: 
            condPats[frozenset(Path[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats
def mineTree(Tree, headerTable, minSup, nf, freqItemList):
    headertb = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]# 1.排序头指针表
    for basePat in headertb:  
        newFreqSet = nf.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        Bases = findPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(Bases, minSup)
        tree=copy.deepcopy(myCondTree)
        lista=[]
        #打印conditional tree的函数
        def printtree(tree,i=0):
            listb=[]
            if tree!=None:
                for child in tree.children.values():
                    b=child.name+' '+str(child.count) 
                    listb.append(b)
                    printtree(child,i+1)
            if listb!=[]:
                lista.insert(i,listb)
            return lista   
        a=printtree(tree)
        if a!=[]:    
            a.insert(0,'Null Set 1')
            print(a)
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)
    return freqItemList

minSup = 300
Data = getData()
FormatData = FormatData(Data)
myFPtree, myHeaderTab = createTree(FormatData, minSup)
myFreqList=[]
frequentitemset=mineTree(myFPtree, myHeaderTab, minSup, set([]), myFreqList)
print(frequentitemset)
print(len(frequentitemset))
print(type(frequentitemset))

rows = frequentitemset

with open('qiye.csv','w') as f:

    f_csv = csv.writer(f)
    f_csv.writerows(rows)