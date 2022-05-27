from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal

class ExtraExecutor(Executor):
    def execute(
        self,
        task_name: str,
        shareable: Shareable,
        fl_ctx: FLContext,
        abort_signal: Signal,
    ) -> Shareable:
        if task_name == "EXTRA_PREPROCESS_TASK":
            self.log_info(fl_ctx, "THIS IS AN EXTRA WORKFLOW TASK RECEIVED BY THE CLIENT.")
            shareable = Shareable()
            shareable.set_return_code(ReturnCode.OK)
            return shareable
        else:
            # If unknown task name, set ReturnCode accordingly.
            shareable = Shareable()
            shareable.set_return_code(ReturnCode.TASK_UNKNOWN)
            return shareable