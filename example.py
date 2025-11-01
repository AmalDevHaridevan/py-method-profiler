from profiling_wrapper import ProfilingWrapper
import time
import numpy as np

# Example usage
if __name__ == "__main__":
    # Example class to profile
    class Calculator:
        def add(self, a, b):
            time.sleep(0.01)  # Simulate some work
            return a + b
        
        def multiply(self, a, b):
            time.sleep(0.02)  # Simulate more work
            return a * b
        
        def fibonacci(self, n):
            """Calculate fibonacci number (inefficient recursive version)"""
            if n <= 1:
                return n
            return self.fibonacci(n - 1) + self.fibonacci(n - 2)
    
    # Create wrapped object
    calc = ProfilingWrapper(Calculator())
    
    # Use the object normally
    print("Performing calculations...")
    for i in range(5):
        result = calc.add(i, i + 1)
        print(f"add({i}, {i+1}) = {result}")
    
    for i in range(3):
        result = calc.multiply(i, 2)
        print(f"multiply({i}, 2) = {result}")
    
    # Get profiling data
    print("\n--- Profiling Results ---")
    add_times = ProfilingWrapper.get_profiling_data("Calculator.add")
    print(f"\nCalculator.add called {len(add_times)} times")
    print(f"Execution times: {add_times}")
    
    multiply_times = ProfilingWrapper.get_profiling_data("Calculator.multiply")
    print(f"\nCalculator.multiply called {len(multiply_times)} times")
    print(f"Execution times: {multiply_times}")
    
    # Get statistics
    print("\n--- Statistics ---")
    add_stats = ProfilingWrapper.get_statistics("Calculator.add")
    print(f"\nCalculator.add statistics:")
    for key, value in add_stats.items():
        print(f"  {key}: {value}")
    
    multiply_stats = ProfilingWrapper.get_statistics("Calculator.multiply")
    print(f"\nCalculator.multiply statistics:")
    for key, value in multiply_stats.items():
        print(f"  {key}: {value}")
    
    # Show all profiling data
    print("\n--- All Profiling Data ---")
    all_data = ProfilingWrapper.get_all_profiling_data()
    for method, times in all_data.items():
        print(f"{method}: {len(times)} calls, total time: {np.sum(times):.6f}s")
