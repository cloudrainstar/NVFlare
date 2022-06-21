import os

from monai.apps.utils import download_and_extract

from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import FLContextKey, ReturnCode
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
            # Extract info from Sharable
            url = shareable.get_header("url")
            dataset_folder_name = shareable.get_header("dataset_folder_name")
            # Extract info from FLContext
            workspace = fl_ctx.get_prop(FLContextKey.WORKSPACE_OBJECT)
            dataset_root = workspace.get_root_dir()
            # Combine dataset
            dataset_path = os.path.join(dataset_root, dataset_folder_name)
            if not os.path.exists(dataset_path):
                self.download_spleen_dataset(url, dataset_root, dataset_path)
            shareable = Shareable()
            shareable.set_return_code(ReturnCode.OK)
            return shareable
        else:
            # If unknown task name, set ReturnCode accordingly.
            shareable = Shareable()
            shareable.set_return_code(ReturnCode.TASK_UNKNOWN)
            return shareable

    def download_spleen_dataset(self, url: str, dataset_root: str, dataset_path: str):
        tarfile_name = f"{dataset_path}.tar"
        download_and_extract(url=url, filepath=tarfile_name, output_dir=dataset_root)
        