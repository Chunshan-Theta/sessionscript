import unittest
from sessionscript.manger import Stage, Plan, SwitchPlan, SwitchRePattenPlan
from sessionscript.result import RunResult


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
            "txt": f"i got this-> 『{text}』.  I will repeat it again."
        })

class StageStaticResponds_A(Stage):
    def run(self,text) -> RunResult:
        return RunResult(success=True,label="RepeatText",body={
            "txt": f"I'm Plan A. i got this-> 『{text}』.  I will repeat it again."
        })

class StageStaticResponds_B(Stage):
    def run(self,text) -> RunResult:
        return RunResult(success=True,label="RepeatText",body={
            "txt": f"I'm Plan B. i got this-> 『{text}』.  I will repeat it again."
        })

class ChatBotCase(unittest.TestCase):

    @staticmethod
    def say(res:RunResult):
        for i in res.json()['body']['data']:
            print("BOT: ",i['body']['txt'])

    def test_control_by_user_stage(self):
        #
        received_text = "hihi"
        user_stage = "responds"

        #
        switch_plan_handler = SwitchPlan()
        default_plan = Plan(units=[StageRepeat_default()])
        base_responds_plan = Plan(units=[StageStaticResponds(),StageRepeat()])

        #
        switch_plan_handler.add_default_plan(plan=default_plan)
        switch_plan_handler.add_plan(switch_label="responds",plan=base_responds_plan)

        #
        print('-' * 20)
        self.say(switch_plan_handler.switch_and_run_finish(switch_label=user_stage, text=received_text))


        #
        print('-' * 20)
        user_stage = "unknown_stage"
        self.say(switch_plan_handler.switch_and_run_finish(switch_label=user_stage, text=received_text))

    def test_control_by_user_say(self):
        #
        switch_plan_handler = SwitchRePattenPlan()
        default_plan = Plan(units=[StageRepeat_default()])
        base_responds_planA = Plan(units=[StageStaticResponds_A(), StageRepeat()])
        base_responds_planB = Plan(units=[StageStaticResponds_B(), StageRepeat()])

        #
        switch_plan_handler.add_default_plan(plan=default_plan)
        switch_plan_handler.add_plan(re_patten="search:.*", plan=base_responds_planA)
        switch_plan_handler.add_plan(re_patten="save:.*", plan=base_responds_planB)

        #
        print('-' * 20)
        received_text = "search:台北101"
        self.say(switch_plan_handler.switch_and_run_finish(switch_label=received_text, text=received_text))

        #
        print('-' * 20)
        received_text = "save:台北101"
        self.say(switch_plan_handler.switch_and_run_finish(switch_label=received_text, text=received_text))

        #
        print('-' * 20)
        received_text = "unknown:台北101"
        self.say(switch_plan_handler.switch_and_run_finish(switch_label=received_text, text=received_text))

if __name__ == '__main__':
    unittest.main()
