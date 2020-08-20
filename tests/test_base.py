import unittest
from manger import Stag, Plan, SwitchPlan
from result import RunResult


class StagCompute(Stag):
    def run(self,*args,**kwargs) -> RunResult:
        assert 1+2 == 3
        return RunResult(success=True,label=self.stag_id,body={
            "Q": "1+2",
            "A": 3
        })


class StagError(Stag):

    def run(self,*args,**kwargs) -> RunResult:
        return RunResult(success=False,label=self.stag_id, body={}, err=AssertionError("just Error"))


class MyTestCase(unittest.TestCase):
    def test_something(self):
        plan_a = Plan([StagCompute("DefaultStagCompute"), StagError(stag_id="StagError-customize")])
        res = plan_a.run_complete_plan()
        print(res)

    def test_plans(self):
        switch_plan_handler = SwitchPlan()
        switch_plan_handler.add_plan(lable="error",plan=Plan([StagError()]))
        switch_plan_handler.add_plan(lable="math",plan=Plan([StagCompute()]))
        print(switch_plan_handler.switch_and_run_finish(switch_label="math"))

    def test_plans_default(self):
        switch_plan_handler = SwitchPlan()
        switch_plan_handler.add_plan(lable="error",plan=Plan([StagError()]))
        switch_plan_handler.add_plan(lable="math",plan=Plan([StagCompute()]))
        switch_plan_handler.add_default_plan(plan=Plan([StagCompute()]))
        print(switch_plan_handler.switch_and_run_finish(switch_label="123"))

    def test_something_error(self):
        plan_a = Plan([StagCompute(), StagError(),StagCompute(),])
        res = plan_a.run_complete_plan()
        print(res)

if __name__ == '__main__':
    unittest.main()
