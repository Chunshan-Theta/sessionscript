import json


class RunResult:
    def __init__(self, success: bool, body, err: Exception = None):
        self.success = success
        self.err = err
        self.body = body

    def __str__(self):
        return json.dumps({
            "success": self.success,
            "err": str(self.err),
            "body": str(self.body)
        },ensure_ascii=False)


class PlanRunResult(RunResult):
    def __init__(self, success: bool, run_stag, msg, err: Exception = None):
        body = {
            "run_stag": run_stag,
            "msg": msg
        }
        super().__init__(success, body, err)