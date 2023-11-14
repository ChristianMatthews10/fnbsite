import matplotlib.pyplot as plt

def fibonacci(n):
    """Return the first n terms of the Fibonacci sequence."""
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])
    return sequence

n_terms = 1000  # Change this value to plot more or fewer terms
fib_sequence = fibonacci(n_terms)
plt.plot(fib_sequence, 'bo-')
plt.xlabel('Term Number')
plt.ylabel('Fibonacci Value')
plt.title(f'First {n_terms} Terms of the Fibonacci Sequence')
plt.show()


