import time

def allocate_memory(size):
    data.append([0] * size)

initial_size = 1000000
data = []

for i in range(100) :
    # Allocate memory
    allocate_memory(initial_size)
    # Increase the memory allocation by a fixed amount
    time.sleep(0.1)
