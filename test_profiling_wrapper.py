"""
Test suite for ProfilingWrapper
"""

import time
from profiling_wrapper import ProfilingWrapper


class SampleClass:
    """Sample class for testing the profiling wrapper."""
    
    def __init__(self):
        self.counter = 0
    
    def fast_method(self):
        """A fast method."""
        time.sleep(0.001)
        return "fast"
    
    def slow_method(self):
        """A slower method."""
        time.sleep(0.01)
        return "slow"
    
    def method_with_args(self, x, y):
        """Method that takes arguments."""
        time.sleep(0.002)
        return x + y
    
    def increment_counter(self):
        """Method that modifies state."""
        self.counter += 1
        return self.counter


def test_basic_functionality():
    """Test basic wrapping and timing functionality."""
    print("=" * 60)
    print("Test 1: Basic Functionality")
    print("=" * 60)
    
    # Clear any previous profiling data
    ProfilingWrapper.clear_profiling_data()
    
    # Create wrapped object
    obj = ProfilingWrapper(SampleClass())
    
    # Call methods
    obj.fast_method()
    obj.slow_method()
    obj.fast_method()
    
    # Get profiling data
    fast_times = ProfilingWrapper.get_profiling_data("SampleClass.fast_method")
    slow_times = ProfilingWrapper.get_profiling_data("SampleClass.slow_method")
    
    print(f"\nfast_method called {len(fast_times)} times")
    print(f"slow_method called {len(slow_times)} times")
    
    assert len(fast_times) == 2, "fast_method should be called 2 times"
    assert len(slow_times) == 1, "slow_method should be called 1 time"
    
    print("Basic functionality test passed!")


def test_method_arguments():
    """Test methods with arguments."""
    print("\n" + "=" * 60)
    print("Test 2: Methods with Arguments")
    print("=" * 60)
    
    ProfilingWrapper.clear_profiling_data()
    
    obj = ProfilingWrapper(SampleClass())
    
    # Call method with different arguments
    result1 = obj.method_with_args(5, 10)
    result2 = obj.method_with_args(3, 7)
    
    print(f"\nmethod_with_args(5, 10) = {result1}")
    print(f"method_with_args(3, 7) = {result2}")
    
    times = ProfilingWrapper.get_profiling_data("SampleClass.method_with_args")
    print(f"\nMethod called {len(times)} times")
    
    assert result1 == 15, "Method should return correct result"
    assert result2 == 10, "Method should return correct result"
    assert len(times) == 2, "Method should be tracked correctly"
    
    print("Arguments test passed!")


def test_state_modification():
    """Test that wrapper preserves object state."""
    print("\n" + "=" * 60)
    print("Test 3: State Modification")
    print("=" * 60)
    
    ProfilingWrapper.clear_profiling_data()
    
    obj = ProfilingWrapper(SampleClass())
    
    # Increment counter multiple times
    for i in range(5):
        result = obj.increment_counter()
        print(f"Counter: {result}")
    
    # Access attribute directly
    print(f"\nFinal counter value: {obj.counter}")
    
    assert obj.counter == 5, "Counter should be 5"
    
    print("State modification test passed!")


def test_statistics():
    """Test statistical analysis of profiling data."""
    print("\n" + "=" * 60)
    print("Test 4: Statistics")
    print("=" * 60)
    
    ProfilingWrapper.clear_profiling_data()
    
    obj = ProfilingWrapper(SampleClass())
    
    # Call method multiple times
    for _ in range(10):
        obj.fast_method()
    
    stats = ProfilingWrapper.get_statistics("SampleClass.fast_method")
    
    print(f"\nStatistics for SampleClass.fast_method:")
    print(f"  Count: {stats['count']}")
    print(f"  Mean: {stats['mean']:.6f}s")
    print(f"  Median: {stats['median']:.6f}s")
    print(f"  Std Dev: {stats['std']:.6f}s")
    print(f"  Min: {stats['min']:.6f}s")
    print(f"  Max: {stats['max']:.6f}s")
    print(f"  Total: {stats['total']:.6f}s")
    
    assert stats['count'] == 10, "Should have 10 calls"
    assert stats['mean'] > 0, "Mean should be positive"
    
    print("Statistics test passed!")


def test_multiple_objects():
    """Test that profiling works across multiple instances of the same class."""
    print("\n" + "=" * 60)
    print("Test 5: Multiple Objects")
    print("=" * 60)
    
    ProfilingWrapper.clear_profiling_data()
    
    # Create two wrapped objects
    obj1 = ProfilingWrapper(SampleClass())
    obj2 = ProfilingWrapper(SampleClass())
    
    # Call methods on both objects
    obj1.fast_method()
    obj1.fast_method()
    obj2.fast_method()
    
    times = ProfilingWrapper.get_profiling_data("SampleClass.fast_method")
    
    print(f"\nTotal calls to SampleClass.fast_method: {len(times)}")
    
    assert len(times) == 3, "Should track all calls across instances"
    
    print("Multiple objects test passed!")


def test_all_profiling_data():
    """Test retrieving all profiling data at once."""
    print("\n" + "=" * 60)
    print("Test 6: All Profiling Data")
    print("=" * 60)
    
    ProfilingWrapper.clear_profiling_data()
    
    obj = ProfilingWrapper(SampleClass())
    
    # Call various methods
    obj.fast_method()
    obj.slow_method()
    obj.method_with_args(1, 2)
    
    all_data = ProfilingWrapper.get_all_profiling_data()
    
    print(f"\nProfiling data for {len(all_data)} methods:")
    for method, times in all_data.items():
        print(f"  {method}: {len(times)} calls")
    
    assert len(all_data) == 3, "Should have data for 3 methods"
    
    print("All profiling data test passed!")


def test_nonexistent_method():
    """Test behavior when querying non-existent method."""
    print("\n" + "=" * 60)
    print("Test 7: Nonexistent Method")
    print("=" * 60)
    
    data = ProfilingWrapper.get_profiling_data("NonExistent.method")
    
    print(f"\nData for nonexistent method: {data}")
    print(f"Length: {len(data)}")
    
    assert len(data) == 0, "Should return empty array for nonexistent method"
    
    print("Nonexistent method test passed!")


if __name__ == "__main__":
    test_basic_functionality()
    test_method_arguments()
    test_state_modification()
    test_statistics()
    test_multiple_objects()
    test_all_profiling_data()
    test_nonexistent_method()
    
    print("\n" + "=" * 60)
    print("All tests passed!" )
    print("=" * 60)
