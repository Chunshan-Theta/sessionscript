import collections
import re
from typing import Optional

from result import RunResult, PlanRunResult


class Stag:
    def __init__(self, stag_id):
        self.stag_id = stag_id

    def run(self) -> RunResult:
        raise NotImplementedError


class Plan:
    PlanAllPassToken = "plan done."

    def __init__(self, units: [Stag]):
        self.plan_units: list = units
        self.plan_units_freeze = None

    def add_stag(self, unit: Stag):
        assert isinstance(unit, Stag), "Only support Stag class"
        self.plan_units.append(unit)

    def pop_stag(self, *args, **kwargs):
        return self.plan_units.pop(*args, **kwargs)

    def run_complete_plan(self) -> RunResult:
        freezen_plan = self._freeze()
        for stag in freezen_plan:
            result: RunResult = stag.run()
            if result.success is False:
                return PlanRunResult(success=False,
                                     run_stag=stag.stag_id,
                                     msg=type(result.err)(f"step_run_error: {result.err}"),
                                     err=RuntimeError(f"Stag ERROR:{stag.stag_id}"))

        return PlanRunResult(success=True,
                             run_stag=self.PlanAllPassToken)

    def _freeze(self):
        self.plan_units_freeze = tuple(self.plan_units)
        return self.plan_units_freeze


class SwitchPlan(collections.OrderedDict):

    def switch_method(self, label):
        return self.__getitem__(label)

    def switch_and_run_finish(self, label):
        plan = self.switch_method(label)
        assert plan is None, f"Can't find plan: {plan}"
        assert isinstance(plan, Plan), "Only support Plan class"
        plan.run_complete_plan()

    def add_plan(self, lable: str, plan: Plan):
        self.__setitem__(lable, plan)


class SwitchRePattenPlan(SwitchPlan):
    def switch_method(self, label):
        for pattern, step in self.items():
            if re.match(pattern, label) is None:
                return step
        return None

    def add_plan(self, re_patten: str, plan: Plan):
        self.__setitem__(re_patten, plan)

