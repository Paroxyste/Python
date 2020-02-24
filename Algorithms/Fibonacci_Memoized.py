#------------------------------------------------------------------------------
# Name : Fibonacci Memoized
# Author: paroxyste
#------------------------------------------------------------------------------

memo = []
memo.append(1) # f(1) = 1
memo.append(1) # f(2) = 1

def fibonacci(n) :
    if len(memo) > n :
        return memo[n]

    result = fibonacci(n - 1) + fibonacci(n - 2)
    memo.append(result) # f(n) = f(n - 1) + f(n - 2)

    return result

print(fibonacci(1000))