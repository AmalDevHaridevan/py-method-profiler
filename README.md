# Profiling Wrapper

A Python module that provides transparent method profiling for any object through a wrapper class.

## Features

- **Transparent Wrapping**: Wrap any object and use it normally while automatically collecting timing data
- **Method Timing**: Automatically times every method call with high precision using `time.perf_counter()`
- **Statistical Analysis**: Built-in statistics including mean, median, std dev, min, max, and total execution time
- **Class-level Storage**: Timing data stored in a static dictionary accessible across all wrapper instances
- **NumPy Integration**: Returns timing data as NumPy arrays for easy analysis

## Installation

Requires Python 3.6+ and NumPy:

```bash
pip install numpy
```

## Quick Start

```python
from profiling_wrapper import ProfilingWrapper

# Your class
class Calculator:
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b

# Wrap the object
calc = ProfilingWrapper(Calculator())

# Use it normally
calc.add(5, 10)
calc.add(3, 7)
calc.multiply(4, 6)

# Get profiling data
add_times = ProfilingWrapper.get_profiling_data("Calculator.add")
print(f"add() was called {len(add_times)} times")
print(f"Execution times: {add_times}")

# Get statistics
stats = ProfilingWrapper.get_statistics("Calculator.add")
print(f"Mean execution time: {stats['mean']:.6f}s")
```

## API Reference

### Constructor

```python
wrapper = ProfilingWrapper(obj)
```

Creates a profiling wrapper around any object.

**Parameters:**
- `obj`: Any object whose methods should be profiled

### Class Methods

#### `get_profiling_data(key: str) -> np.ndarray`

Retrieve timing data for a specific method.

**Parameters:**
- `key`: Method identifier in format `"{ClassName}.{method_name}"`

**Returns:**
- NumPy array of execution times in seconds (length = number of calls)

**Example:**
```python
times = ProfilingWrapper.get_profiling_data("Calculator.add")
```

#### `get_statistics(key: str) -> Dict[str, float]`

Get statistical summary for a method's execution times.

**Parameters:**
- `key`: Method identifier in format `"{ClassName}.{method_name}"`

**Returns:**
- Dictionary with keys: `count`, `mean`, `median`, `std`, `min`, `max`, `total`

**Example:**
```python
stats = ProfilingWrapper.get_statistics("Calculator.add")
print(f"Average time: {stats['mean']:.6f}s")
print(f"Total calls: {stats['count']}")
```

#### `get_all_profiling_data() -> Dict[str, np.ndarray]`

Retrieve timing data for all profiled methods.

**Returns:**
- Dictionary mapping method keys to NumPy arrays of execution times

**Example:**
```python
all_data = ProfilingWrapper.get_all_profiling_data()
for method, times in all_data.items():
    print(f"{method}: {len(times)} calls")
```

#### `clear_profiling_data(key: str = None)`

Clear profiling data.

**Parameters:**
- `key`: Optional method identifier. If provided, clears only that method's data. If `None`, clears all data.

**Example:**
```python
# Clear all data
ProfilingWrapper.clear_profiling_data()

# Clear specific method data
ProfilingWrapper.clear_profiling_data("Calculator.add")
```

## Usage Examples

### Example 1: Basic Profiling

```python
from profiling_wrapper import ProfilingWrapper

class DataProcessor:
    def process(self, data):
        # Some processing
        return len(data)

# Wrap and use
processor = ProfilingWrapper(DataProcessor())
processor.process([1, 2, 3])
processor.process([4, 5, 6, 7])

# Get results
times = ProfilingWrapper.get_profiling_data("DataProcessor.process")
print(f"Called {len(times)} times with average time {times.mean():.6f}s")
```

### Example 2: Multiple Instances

```python
# Create multiple wrapped instances
calc1 = ProfilingWrapper(Calculator())
calc2 = ProfilingWrapper(Calculator())

# All calls are tracked together
calc1.add(1, 2)
calc2.add(3, 4)

# Get combined data
times = ProfilingWrapper.get_profiling_data("Calculator.add")
print(f"Total calls across all instances: {len(times)}")
```

### Example 3: Performance Analysis

```python
import numpy as np

# Run some operations
obj = ProfilingWrapper(MyClass())
for i in range(100):
    obj.expensive_operation()

# Analyze performance
stats = ProfilingWrapper.get_statistics("MyClass.expensive_operation")
print(f"Performance Analysis:")
print(f"  Calls: {stats['count']}")
print(f"  Average: {stats['mean']*1000:.2f}ms")
print(f"  Median: {stats['median']*1000:.2f}ms")
print(f"  Std Dev: {stats['std']*1000:.2f}ms")
print(f"  Range: {stats['min']*1000:.2f}ms - {stats['max']*1000:.2f}ms")
print(f"  Total Time: {stats['total']:.2f}s")
```

### Example 4: Comparing Methods

```python
# Profile multiple methods
obj = ProfilingWrapper(Calculator())

for i in range(50):
    obj.add(i, i+1)
    obj.multiply(i, 2)

# Compare performance
all_data = ProfilingWrapper.get_all_profiling_data()
for method, times in all_data.items():
    avg_time = times.mean()
    print(f"{method}: {avg_time*1000:.4f}ms average ({len(times)} calls)")
```

## How It Works

1. **Wrapping**: When you wrap an object, `ProfilingWrapper` intercepts all attribute access via `__getattr__`
2. **Method Detection**: When a callable method is accessed, it's wrapped with timing logic
3. **Timing**: Each method call is timed using `time.perf_counter()` (high-resolution timer)
4. **Storage**: Execution times are stored in a class-level dictionary with keys like `"ClassName.method_name"`
5. **Retrieval**: Timing data can be retrieved at any time using class methods

## Notes

- The wrapper is transparent - wrapped objects behave exactly like unwrapped ones
- Only methods are profiled; regular attributes are passed through unchanged
- Profiling data persists across wrapper instances (class-level storage)
- Use `clear_profiling_data()` to reset between test runs
- Timing precision depends on the system's `time.perf_counter()` implementation

## Performance Overhead

The wrapper adds minimal overhead to each method call:
- Attribute lookup
- Function wrapping
- Two `time.perf_counter()` calls
- One dictionary append operation

For most use cases, this overhead is negligible (typically < 1 microsecond).

## License

MIT License
