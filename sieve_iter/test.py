import sieve

def test1():
    test = sieve.sieve()
    assert test.next() == 3
    print "Test1 finished"

def test2():
    test = sieve.sieve()
    test.next()
    assert test.next() == 5
    print "Test2 finished"

def test3():
    test = sieve.sieve()
    test.next()
    test.next()
    assert test.next() == 7
    print "Test3 finished"



test1()
test2()
test3()
