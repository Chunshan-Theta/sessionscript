import unittest
from manger import Stag, Plan
from result import RunResult


class StagCompute(Stag):
    def run(self) -> RunResult:
        assert 1+2 == 3
        return RunResult(success=True, body={
            "Q": "1+2",
            "A": 3
        })


class StagError(Stag):

    def run(self) -> RunResult:
        assert 1+2 == 3
        return RunResult(success=False, body={}, err=AssertionError("just Error"))


class MyTestCase(unittest.TestCase):
    def test_something(self):
        plan_a = Plan([StagCompute("DefaultStagCompute"), StagError("DefaultStagError")])
        res = plan_a.run_complete_plan()
        print(res)

if __name__ == '__main__':
    unittest.main()
