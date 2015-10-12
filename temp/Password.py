__author__ = 'Xu Zhao'

def password_test(str):
    if len(str) < 8:
        return False
    charFlag = False
    numFlag = False
    for ch in str:
        if ord(ch)>=65 and ord(ch)<=90:
            charFlag = True
        if ord(ch)>=97 and ord(ch)<=122:
            charFlag = True
        if ord(ch)>=32 and ord(ch)<=64:
            numFlag = True
    if charFlag and numFlag:
        return True
    else:
        return False

if __name__ == "__main__":
    print password_test("123459@")