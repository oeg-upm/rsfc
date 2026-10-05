class TestRegistry:
    def __init__(self):
        self._registry = {}

    def register_test(self, test_id, args):
        def decorator(func):
            self._registry[test_id] = {
                "func": func,
                "args": args
            }
            return func
        return decorator

    def get_test(self, test_id):
        return self._registry.get(test_id)

test_registry = TestRegistry()