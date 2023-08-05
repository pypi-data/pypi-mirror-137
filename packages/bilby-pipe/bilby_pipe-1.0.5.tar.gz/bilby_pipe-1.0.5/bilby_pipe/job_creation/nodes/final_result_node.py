from ..node import Node


class FinalResultNode(Node):
    def __init__(self, inputs, parent_node, dag):
        super().__init__(inputs)
        self.dag = dag
        self.request_cpus = 1
        self.job_name = f"{parent_node.label}_final_result"

        self.setup_arguments(
            add_ini=False, add_unknown_args=False, add_command_line_args=False
        )

        self.arguments.add("result", parent_node.result_file)
        self.arguments.add("outdir", inputs.final_result_directory)
        self.arguments.add("extension", self.inputs.result_format)
        self.arguments.add("max-samples", self.inputs.final_result_nsamples)
        self.arguments.add_flag("lightweight")
        self.arguments.add_flag("save")

        self.process_node()
        self.job.add_parent(parent_node.job)

    @property
    def executable(self):
        return self._get_executable_path("bilby_result")

    @property
    def request_memory(self):
        return "4 GB"

    @property
    def log_directory(self):
        return self.inputs.data_analysis_log_directory
