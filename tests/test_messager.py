import unittest
from manger import Stag, Plan, SwitchPlan, SwitchRePattenPlan
from result import RunResult


class StagRepeat_default(Stag):
    def run(self,text) -> RunResult:
        return RunResult(success=True,label="RepeatText",body={
            "txt": f"i don't known your plan,but i got this-> 『{text}』."
        })

class StagRepeat(Stag):
    def run(self,text) -> RunResult:
        return RunResult(success=True,label="RepeatText",body={
            "txt": f"『{text}』"
        })


class StagStaticResponds(Stag):
    def run(self,text) -> RunResult:
        return RunResult(success=True,label="RepeatText",body={
            "txt": f"i got this-> 『{text}』.  I will repeat it again."
        })

class StagStaticResponds_A(Stag):
    def run(self,text) -> RunResult:
        return RunResult(success=True,label="RepeatText",body={
            "txt": f"I'm Plan A. i got this-> 『{text}』.  I will repeat it again."
        })

class StagStaticResponds_B(Stag):
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
        default_plan = Plan(units=[StagRepeat_default()])
        base_responds_plan = Plan(units=[StagStaticResponds(),StagRepeat()])

        #
        switch_plan_handler.add_default_plan(plan=default_plan)
        switch_plan_handler.add_plan(lable="responds",plan=base_responds_plan)

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
        default_plan = Plan(units=[StagRepeat_default()])
        base_responds_planA = Plan(units=[StagStaticResponds_A(), StagRepeat()])
        base_responds_planB = Plan(units=[StagStaticResponds_B(), StagRepeat()])

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
