from nvflare.apis.client import Client
from nvflare.apis.fl_context import FLContext
from nvflare.apis.impl.controller import Controller, Task
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal

class ExtraWorkflow(Controller):
    def __init__(self):
        Controller.__init__(self)
    
    def start_controller(self, fl_ctx: FLContext) -> None:
        self.log_info(fl_ctx, "Starting extra workflow.")

    def control_flow(self, abort_signal: Signal, fl_ctx: FLContext) -> None:
        # Start an extra task from the server
        self.log_info(fl_ctx, "THIS IS AN EXTRA WORKFLOW TASK GIVEN BY THE SERVER.")

        # Create a Shareable and add to a task
        extra_task = Task(
                    name="EXTRA_PREPROCESS_TASK",
                    data=Shareable(),
                    props={},
                    timeout=300,
                )

        # Send the task and wait for results
        self.broadcast_and_wait(
            task=extra_task,
            min_responses=1,
            wait_time_after_min_received=30,
            fl_ctx=fl_ctx,
            abort_signal=abort_signal,
        )

        # Finally, exit
        return

    def stop_controller(self, fl_ctx: FLContext):
        self.cancel_all_tasks(fl_ctx=fl_ctx)

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        super().handle_event(event_type, fl_ctx)

    def process_result_of_unknown_task(
        self, client: Client, task_name: str, client_task_id: str, result: Shareable, fl_ctx: FLContext
    ):
        self.log_info(fl_ctx, "Ignoring result from unknown task.")