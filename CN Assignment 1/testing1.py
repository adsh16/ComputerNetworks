# Defining the recurrence relation for the number of tries needed to get n consecutive failures
def expected_tries_consecutive_failures(n, p):
    # Initialize the base case: E_0 = 0 (no failures needed if no consecutive failures required)
    E = [0] * (n + 1)
    
    # Apply the recurrence relation to compute E_n
    for i in range(1, n + 1):
        E[i] = (2 / p) * E[i - 1] + (1 / p)
    
    return E[n]

# For 3 consecutive failures with a 30% failure rate (p = 0.3)
n_consecutive_failures = 3
failure_rate = 0.3

expected_tries = expected_tries_consecutive_failures(n_consecutive_failures, failure_rate)
print(expected_tries)
