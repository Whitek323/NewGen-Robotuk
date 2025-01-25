import time
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Use time.perf_counter() for high-resolution timing
        start_time = time.perf_counter()
        
        # Execute the original function
        result = func(*args, **kwargs)
        
        # Calculate total execution time
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        # Optional: print or log execution time
        print(f"{func.__name__} took {execution_time:.2f} s")
        
        return result
    
    return wrapper

@timer
def calculate_sum(n):
    return sum(range(n))

calculate_sum(1000000)

@timer
def hello_world():
    print("hello world")
hello_world()