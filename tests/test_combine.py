__author__ = 'Xu Zhao'

def getBinary(n, num):
    ret = ''
    while n > 0:
        ret = str(n%2) + ret
        n = n/2
    if len(ret) > num:
        raise 'Not enough digits'
    for i in range(num-len(ret)):
        ret = '0'+ret
    return ret

def getCombine(L):
    myset = []
    for i in range(0, 2**len(L)):
        binset = getBinary(i, len(L))
        subset = []
        for j in range(len(binset)):
            if binset[j] == '1':
                subset.append(L[j])
        myset.append(subset)
    return myset

if __name__ == "__main__":
    print getBinary(10, 5)
    L = ['a', 'b', 'c', 'd']
    print len(getCombine(L))