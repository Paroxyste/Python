#------------------------------------------------------------------------------
# Name : Fibonacci Iterative
# Author: paroxyste
#------------------------------------------------------------------------------

def fibonacci(n) :
    memo = [1,1] # f(0) = 1, f(1) = 1

    for i in range(2, n + 1):
        memo.append(memo[i - 1] + memo[i - 2])

    return memo[n]

print(fibonacci(1000))

