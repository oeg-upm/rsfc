from rsfc.utils.registry import test_registry
import rsfc.rsfc_checks
from rsfc.utils.exceptions import GithubRateLimitExceeded

class RSFCEvaluator:
    
    def __init__(self, context):
        self.context = context
        self.results = []
        
    
    def assess_indicators(self, test_id = None):
        
        print("Assessing repository...")
        execution_data = self.context

        if test_id is not None:
            tests_to_run = [test_id]
        else:
            tests_to_run = self.context.get("evaluated_tests", [])

        try:
            for tid in tests_to_run:
                test_info = test_registry.get_test(tid)
                
                if not test_info:
                    print(f"Warning: Test '{tid}' is not registered.")
                    continue

                func = test_info["func"]
                required_args = test_info["args"]

                try:
                    kwargs = {arg_name: execution_data[arg_name] for arg_name in required_args}
                except KeyError as e:
                    print(f"Error at test {tid}: Context does not include necessary data '{e.args[0]}'")
                    continue

                result = func(**kwargs)
                self.results.append(result)
        except Exception as e:
            if "Token lacks required permissions or scopes" in str(e):
                raise GithubRateLimitExceeded() from e
    
    
    def get_results(self):
        return self.results