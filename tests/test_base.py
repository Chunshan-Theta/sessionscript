import unittest
from sessionscript.manger import Stage, Plan, SwitchPlan
from sessionscript.result import RunResult


class StageCompute(Stage):
    def run(self,*args,**kwargs) -> RunResult:
        assert 1+2 == 3
        return RunResult(success=True,label=self.stage_id,body={
            "Q": "1+2",
            "A": 3
        })


class StageError(Stage):

    def run(self,*args,**kwargs) -> RunResult:
        return RunResult(success=False,label=self.stage_id, body={}, err=AssertionError("just Error"))


class MyTestCase(unittest.TestCase):
    def test_something(self):
        plan_a = Plan([StageCompute("DefaultStageCompute"), StageError(stage_id="StageError-customize")])
        res = plan_a.run_complete_plan()
        print(res)

    def test_plans(self):
        switch_plan_handler = SwitchPlan()
        switch_plan_handler.add_plan(switch_label="error",plan=Plan([StageError()]))
        switch_plan_handler.add_plan(switch_label="math",plan=Plan([StageCompute()]))
        print(switch_plan_handler.switch_and_run_finish(switch_label="math"))

    def test_plans_default(self):
        switch_plan_handler = SwitchPlan()
        switch_plan_handler.add_plan(switch_label="error",plan=Plan([StageError()]))
        switch_plan_handler.add_plan(switch_label="math",plan=Plan([StageCompute()]))
        switch_plan_handler.add_default_plan(plan=Plan([StageCompute()]))
        print(switch_plan_handler.switch_and_run_finish(switch_label="123"))

    def test_something_error(self):
        plan_a = Plan([StageCompute(), StageError(),StageCompute(),])
        res = plan_a.run_complete_plan()
        print(res)

if __name__ == '__main__':
    unittest.main()
