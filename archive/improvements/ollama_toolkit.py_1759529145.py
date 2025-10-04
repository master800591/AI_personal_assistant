# AI Corporation Evolution - Add caching layer for model responses
# Generated: 2025-10-03T15:05:45.948595
# Priority: high
# Type: performance


# Add response caching for better performance
class ResponseCache:
    def __init__(self, max_size=1000):
        self.cache = {}
        self.max_size = max_size
        
    def get(self, key):
        return self.cache.get(key)
        
    def set(self, key, value):
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            oldest = next(iter(self.cache))
            del self.cache[oldest]
        self.cache[key] = value
