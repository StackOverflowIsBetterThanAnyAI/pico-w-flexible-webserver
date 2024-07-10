import gc

def print_memory():
    gc.collect()
    free_memory = gc.mem_free()
    allocated_memory = gc.mem_alloc()
    total_memory = free_memory + allocated_memory
    print(f"Total memory: {total_memory} Bytes")
    print(f"Allocated memory: {allocated_memory} Bytes")
    print(f"Free memory: {free_memory} Bytes")
    print('')
