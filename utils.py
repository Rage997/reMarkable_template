import pexpect

def effortless_scp(origin, destination, password):
    '''Funcion to make scp calls easier'''
    child = pexpect.spawn('scp ' + origin + ' ' + destination)
    r = child.expect ('[pP]assword:')
    if r==0:
        child.sendline (password)
        child.expect(pexpect.EOF)
    if r!=0:
        raise RuntimeError
    child.close()

def yer_or_no():
    print('Continue? [y/n]:')
    while True:
        answer = input().lower()
        if answer == 'y':
            return True
        elif answer == 'y':
            return False
        else:
            print('Please, answer only Y or N')