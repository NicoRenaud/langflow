import json
from typing import Any

from lfx.hpc import HPCTool
from lfx.io import BoolInput, DataInput, Output
from lfx.schema.data import Data


def hpc_component(
    function_name,
    file_path,
    input_file=["hpc_tool.py"],
    output_file=["hpc_result.dat"],
    output_method_name="execute_tool",
):
    def hpc_decorator(cls):
        """Class decorator to turn regular component into an HPC component."""

        class HPCComponent(cls):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                self.inputs.append(
                    [
                        BoolInput(
                            name="use_hpc",
                            display_name="HPC",
                            info="If True, the calculation will be processed on HPC",
                            value=True,
                            required=True,
                            real_time_refresh=True,
                        ),
                        DataInput(
                            name="slurm_data",
                            display_name="SLURM specifications",
                            info="Specify the user name, api key and compute requirements",
                            show=True,
                            required=False,
                            real_time_refresh=True,
                        ),
                        DataInput(
                            name="os_data",
                            display_name="Object Store specifications",
                            info="specifications of the object store space",
                            show=True,
                            required=False,
                            real_time_refresh=True,
                        ),
                    ]
                )

                self.hpc_input_files = input_file
                self.hpc_output_files = output_file

            async def update_build_config(
                self, build_config: dict, field_value: Any, field_name: str | None = None
            ) -> dict:
                """Update build configuration based on field updates."""
                # super().update_build_config(build_config, field_value, field_name)

                try:
                    if field_name is None or field_name == "use_hpc":
                        # Update model_id options based on task
                        if field_value is True:
                            build_config["slurm_data"]["show"] = True
                            build_config["slurm_data"]["required"] = True
                            build_config["os_data"]["show"] = True
                            build_config["os_data"]["required"] = True
                        else:
                            build_config["slurm_data"]["show"] = False
                            build_config["slurm_data"]["required"] = False
                            build_config["os_data"]["show"] = False
                            build_config["os_data"]["required"] = False
                    return build_config
                except (KeyError, AttributeError) as e:
                    self.log(f"Error updating build config: {e!s}")
                return build_config

            def update_outputs(self, frontend_node: dict, field_name: str, field_value: Any) -> dict:
                """Dynamically show only the relevant output based on the selected output type."""
                if field_name == "use_hpc":
                    # Start with empty outputs
                    frontend_node["outputs"] = []

                    # Add only the selected output type
                    if field_value == False:
                        frontend_node["outputs"].append(
                            Output(
                                display_name="Local Calculation",
                                name="result",
                                # type_=Data,
                                method=output_method_name,
                            ).to_dict()
                        )
                    elif field_value == True:
                        frontend_node["outputs"].append(
                            Output(
                                display_name="HPC Calculation",
                                name="result",
                                # type_=Data,
                                method="execute_tool_hpc",
                            ).to_dict()
                        )

                return frontend_node

            @staticmethod
            def extract_function_definition(file):
                """Extracts the definition of a function from a given file.

                Parameters
                ----------
                file : str
                    The path to the file containing the function definition.
                function_name : str
                    The name of the function to extract.

                Returns:
                -------
                str
                    The function definition as a string.
                """
                with open(file) as f:
                    lines = f.readlines()
                    function_definition = []
                    record = False
                    for line in lines:
                        if line.startswith(f"def {function_name}("):
                            record = True
                        if record:
                            function_definition.append(line)
                return "".join(function_definition)

            def job_script_str(self):
                return (
                    "#!/bin/bash\npython "
                    + self.hpc_input_files[0]
                    + " "
                    + self.expression
                    + " "
                    + self.hpc_output_files[0]
                )

            def execute_tool_hpc(self) -> Data:
                """Evaluate the mathematical expression and return the result."""
                try:
                    # instantiate the HPCTool
                    hpctool = HPCTool(slurm_data=self.slurm_data.data, os_data=self.os_data.data)

                    # create the Python file we need for execution on HPC and upload it to OS
                    file_data = self.extract_function_definition(file_path, "calculate_expression")
                    hpctool.os_connector.create_bucket()
                    hpctool.os_connector.put_object_to_os(file_data, self.hpc_input_files[0])

                    # create the job script we need on HPC
                    job_script = hpctool._insert_os_sync_in_job_script(self.job_script_str())
                    print(job_script)

                    # # submit the job to the SLURM API
                    hpctool.slurm_connector.submit_and_monitor_slurm_job(job_script=job_script, monitor_interval=10)

                    # read the result from the Object Store
                    data = hpctool.os_connector.read_files_from_os(self.hpc_output_files)
                    print(data)

                    # # purge the OS bucket
                    # hpctool.os_connector.purge_bucket()

                    # parse the result
                    result = json.loads(data[0])
                    print(result)

                except Exception as e:
                    result = {"error": e}
                    return result

                if "error" in result:
                    self.status = result["error"]
                else:
                    self.status = result["result"]
                    self.log(f"Calculation result: {result['result']}")

                return Data(data=result)

        return HPCComponent

    return hpc_decorator
