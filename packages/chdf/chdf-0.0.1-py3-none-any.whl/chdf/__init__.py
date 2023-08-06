import os
def chd(a):
    try:
        os.chdir(a)
    except:
        os.makedirs(a)
        os.chdir(a) 
def chf(a):
    try:
        b = open(a)
        c = int(b.read())
        b.close()
        b = open(a,'w')
        b.write(f'{c+1}')
        b.close()
    except:
        b = open(a,'w')
        b.write('1')
        b.close() 
        c = 0
    return c
def chff(a):
    try:
        b = open(a)
        c = b.read()
        b.close()
    except:
        b = open(a,'w')
        b.write('0')
        b.close() 
        c = '0'
    return c
