#------------------------------------------------------------------------------
# Name : Fibonacci Iterative Advanced
# Author: paroxyste
#------------------------------------------------------------------------------

def fibonacci(n) :
    memo = [1,1] # f(0) = 1, f(1) = 1

    for i in range (2, n):
        memo[i % 2] = memo[0] + memo[1]

    return memo[n % 2]

print(fibonacci(1000000))

