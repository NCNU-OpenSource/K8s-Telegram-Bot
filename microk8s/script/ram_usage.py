import psutil
import time

def allocate_memory(size):
    # Allocate memory by creating a list
    # with the specified size
    data.append([0] * size)

# Initial memory allocation (in bytes)
initial_size = 1000000
data = []

for i in range(100) :
    ram_usage = psutil.virtual_memory().percent
    print(f"Current RAM usage: {ram_usage}%")
    # Allocate memory
    allocate_memory(initial_size)
    
    # Increase the memory allocation by a fixed amount
    time.sleep(0.1)
