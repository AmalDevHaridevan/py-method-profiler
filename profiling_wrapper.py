"""
Profiling Wrapper Module

A wrapper class that enables timing of object methods with statistical profiling capabilities.
"""

import time
import numpy as np
from typing import Any, Dict, List
from collections import defaultdict


class ProfilingWrapper:
    """
    A wrapper that profiles method calls on any object.
    
    Each method call is timed and stored in a class-level dictionary.
    Profiling data can be retrieved using get_profiling_data().
    """
    
    # Class-level dictionary to store timing data
    _profiling_data: Dict[str, List[float]] = defaultdict(list)
    
    def __init__(self, obj: Any):
        """
        Initialize the profiling wrapper.
        
        Args:
            obj: Any object whose methods should be profiled
        """
        self._wrapped_obj = obj
        self._class_name = obj.__class__.__name__
    
    def __getattr__(self, name: str) -> Any:
        """
        Intercept attribute access to wrap methods with timing logic.
        
        Args:
            name: Attribute name being accessed
            
        Returns:
            The attribute value, wrapped if it's a callable method
        """
        attr = getattr(self._wrapped_obj, name)
        
        # If it's a method, wrap it with timing logic
        if callable(attr):
            def timed_method(*args, **kwargs):
                key = f"{self._class_name}.{name}"
                
                start_time = time.perf_counter()
                result = attr(*args, **kwargs)
                end_time = time.perf_counter()
                
                execution_time = end_time - start_time
                ProfilingWrapper._profiling_data[key].append(execution_time)
                
                return result
            
            return timed_method
        
        # If it's not a method, return it as-is
        return attr
    
    def __setattr__(self, name: str, value: Any) -> None:
        """
        Handle attribute setting.
        
        Args:
            name: Attribute name
            value: Value to set
        """
        # Internal attributes start with underscore
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            setattr(self._wrapped_obj, name, value)
    
    @classmethod
    def get_profiling_data(cls, key: str) -> np.ndarray:
        """
        Retrieve profiling data for a specific method.
        
        Args:
            key: Method key in format "{cls_name}.{method_name}"
            
        Returns:
            NumPy array of execution times (in seconds)
        """
        if key in cls._profiling_data:
            return np.array(cls._profiling_data[key])
        return np.array([])
    
    @classmethod
    def get_all_profiling_data(cls) -> Dict[str, np.ndarray]:
        """
        Retrieve all profiling data.
        
        Returns:
            Dictionary mapping method keys to NumPy arrays of execution times
        """
        return {key: np.array(times) for key, times in cls._profiling_data.items()}
    
    @classmethod
    def clear_profiling_data(cls, key: str = None) -> None:
        """
        Clear profiling data.
        
        Args:
            key: Optional specific method key to clear. If None, clears all data.
        """
        if key is None:
            cls._profiling_data.clear()
        elif key in cls._profiling_data:
            cls._profiling_data[key].clear()
    
    @classmethod
    def get_statistics(cls, key: str) -> Dict[str, float]:
        """
        Get statistical summary of profiling data for a method.
        
        Args:
            key: Method key in format "{cls_name}.{method_name}"
            
        Returns:
            Dictionary with statistics (mean, median, std, min, max, total, count)
        """
        data = cls.get_profiling_data(key)
        
        if len(data) == 0:
            return {
                'count': 0,
                'mean': 0.0,
                'median': 0.0,
                'std': 0.0,
                'min': 0.0,
                'max': 0.0,
                'total': 0.0
            }
        
        return {
            'count': len(data),
            'mean': float(np.mean(data)),
            'median': float(np.median(data)),
            'std': float(np.std(data)),
            'min': float(np.min(data)),
            'max': float(np.max(data)),
            'total': float(np.sum(data))
        }

