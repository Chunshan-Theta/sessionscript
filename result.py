import json


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
    def __init__(self, success: bool, run_stag,data=None, msg:str=None, err: Exception = None):
        body = {
            "run_stag": run_stag
        }
        if msg is not None:
            body.update({
                "msg":str(msg)
            })
        if data is not None:
            body.update({
                "data":data
            })
        super().__init__(success, body,run_stag, err)