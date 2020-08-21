# sessionscript

---
### Stage

`stage` in the process, `Plan.run()` will follow index to run stages and return `RunResult`.
```
class Stage:
    def __init__(self, stage_id=None):
        self.stage_id = stage_id if stage_id is not None else self.__class__.__name__

    def run(self,*args,**kwargs) -> RunResult:
        raise NotImplementedError
````

example:
```
class StageRepeat_default(Stage):
    def run(self,text) -> RunResult:
        return RunResult(success=True,label="RepeatText",body={
            "txt": f"i don't known your plan,but i got this-> 『{text}』."
        })

class StageRepeat(Stage):
    def run(self,text) -> RunResult:
        return RunResult(success=True,label="RepeatText",body={
            "txt": f"『{text}』"
        })


class StageStaticResponds(Stage):
    def run(self,text) -> RunResult:
        return RunResult(success=True,label="RepeatText",body={
            "txt": f"i got this-> 『{text}』."
        })
```
---
### Plan
collection for `Stage`
```
class Plan:
    PlanAllPassToken = "plan done."

    def __init__(self, units: [Stage]):
        self.plan_units: list = units
        self.plan_units_freeze = None

    def add_stage(self, unit: Stage):
        assert isinstance(unit, Stage), "Only support Stage class"
        self.plan_units.append(unit)

    def pop_stage(self, *args, **kwargs):
        return self.plan_units.pop(*args, **kwargs)

    def run_complete_plan(self,*args,**kwargs) -> RunResult:
        freezen_plan = self._freeze()
        stages_result = []
        for stag in freezen_plan:
            result: RunResult = stag.run(*args,**kwargs)
            if result.success is False:
                return PlanRunResult(success=False,
                                     run_stage=stag.stage_id,
                                     msg=type(result.err)(f"step_run_error: {result.err}"),
                                     err=RuntimeError(f"Stage ERROR:{stag.stage_id}"))
            stages_result.append(result.json())

        return PlanRunResult(success=True,
                             run_stage=self.PlanAllPassToken,
                             data=stages_result)

    def _freeze(self):
        self.plan_units_freeze = tuple(self.plan_units)
        return self.plan_units_freeze
```

---
### RunResult
class RunResult:
    def __init__(self, success: bool, body,label, err: Exception = None):
        self.success = success
        self.label = label
        self.err = err
        self.body = body

    def __str__(self):
        return json.dumps(self.json(),ensure_ascii=False)

    def json(self):
        res ={
            "success": self.success,
            "label": self.label,
            "body": self.body if isinstance(self.body,dict) else str(self.body)
        }
        if self.success is False and self.err is not None:
            res.update({
                "err": str(self.err),
            })
        return res


class PlanRunResult(RunResult):
    def __init__(self, success: bool, run_stage,data=None, msg:str=None, err: Exception = None):
        body = {
            "run_stage": run_stage
        }
        if msg is not None:
            body.update({
                "msg":str(msg)
            })
        if data is not None:
            body.update({
                "data":data
            })
        super().__init__(success, body,run_stage, err)


---
### SwitchPlan
```
class SwitchPlan(collections.OrderedDict):
    __default_plan__ = None

    def switch_method(self, label):
        try:
            return self.__getitem__(label)
        except KeyError as e:
            return self.__default_plan__


    def switch_and_run_finish(self, switch_label,*args,**kwargs):
        plan = self.switch_method(switch_label)
        assert plan is not None, f"Can't find plan: {plan}"
        assert isinstance(plan, Plan), "Only support Plan class"
        return plan.run_complete_plan(*args,**kwargs)

    def add_plan(self, switch_label: str, plan: Plan):
        assert isinstance(plan, Plan), "Only support Plan class"
        self.__setitem__(switch_label, plan)

    def add_default_plan(self, plan: Plan):
        assert isinstance(plan, Plan), "Only support Plan class"
        self.__default_plan__ = plan
```
```
class SwitchRePattenPlan(SwitchPlan):
    def switch_method(self, switch_label):
        for pattern, step in self.items():
            if re.match(pattern, switch_label) is not None:
                return step
        return self.__default_plan__

    def add_plan(self, re_patten: str, plan: Plan):
        assert isinstance(plan, Plan), "Only support Plan class"
        self.__setitem__(re_patten, plan)
```
```
#
switch_plan_handler = SwitchPlan()
default_plan = Plan(units=[StageRepeat_default()])
base_responds_plan = Plan(units=[StageStaticResponds(),StageRepeat()])

#
switch_plan_handler.add_default_plan(plan=default_plan)
switch_plan_handler.add_plan(switch_label="responds",plan=base_responds_plan)
```
