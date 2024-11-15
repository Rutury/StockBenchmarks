import main

def test1():
    return True

def test2():
    return 1 / 0

def test3():
    return False

def test4():
    return True

tests = [test1, test2, test3, test4]
crashedCounter, passedCounter, failedCounter, totalCounter = 0, 0, 0, 0
for test in tests:
    try:
        if (test()):
            passedCounter += 1
            result = "PASSED"
        else:
            failedCounter += 1
            result = "FAILED"
    except:
        crashedCounter += 1
        result = "CRAHSED"
    if result != "PASSED":
        print(f"{totalCounter:2} : {result}")
    totalCounter += 1
print(f"\n{totalCounter} tests run, {passedCounter} passed, {failedCounter} failed, {crashedCounter} crashed")
print(f"{totalCounter - passedCounter - failedCounter - crashedCounter} undefined")