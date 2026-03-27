from .object_store_connector import ObjectStoreConnector
from .slurm_api_connector import SLURMAPIConnector


class HPCTool:
    def __init__(self, slurm_data: dict, os_data: dict):
        """Initializes the HPCToolComponent with the given SLURM and Object Store credentials.

        Parameters
        ----------
        slurm_data : dict
            A dictionary containing the SLURM API URL, API version, user name and SLURM JWT.
        os_data : dict
            A dictionary containing the Object Store URL, access key, secret key,
            the name of the bucket and the filename of the file to be uploaded.

        Notes:
        -----
        This function is called when an instance of the HPCToolComponent is created.
        """
        slurm_default_settings = {
            "output_file_name": "tool.out",
            "error_file_name": "tool.err",
            "jobname": "tool",
            "time": 600,
            "partition": "rome",
            "nodes": 1,
            "tasks": 1,
            "cpus_per_task": 1,
        }

        self.slurm_connector = SLURMAPIConnector(slurm_data, slurm_default_settings)
        self.os_connector = ObjectStoreConnector(os_data)

        self.input_files = ["./utils/say_hello.py"]
        self.output_files = [
            self.slurm_connector.settings["output_file_name"],
            self.slurm_connector.settings["error_file_name"],
        ]

    def _insert_os_sync_in_job_script(self, job_script: str) -> str:
        """Modifies the given job script by inserting the necessary s3cmd sync commands
        to synchronize the input and output files with the Object Store.

        Parameters
        ----------
        job_script : str
            The job script to be modified.

        Returns:
        -------
        str
            The modified job script with the s3cmd sync commands inserted.
        """

        idx = 0  # in case npo module are loaded
        job_script_split = job_script.split("\n")
        for iline, line in enumerate(job_script_split):
            if line.startswith("module load"):
                idx = iline

        job_script_split.insert(idx + 1, f"aws s3 sync s3://{self.os_connector.settings['bucketname']}/ ./")
        job_script_split.append(f"aws s3 sync ./ s3://{self.os_connector.settings['bucketname']}/")

        return "\n".join(job_script_split)

    def job_script_str(self):
        return '#!/bin/bash\n\necho "Hello World!"\nsleep 60\necho "Goodbye world"'

    def run(self):
        """Runs the HPCToolComponent.

        Creates a bucket in the Object Store, uploads a file to the Object Store, 
        submits a job to the SLURM API and reads a file from the Object Store.

        Returns:
        -------
        str
            The content of the file read from the Object Store.
        """
        # uplaod the files to the object store
        self.os_connector.upload_files_to_os(self.input_files)

        # get the script of the job and submit/monitor job vial slurm api
        job_script = self._insert_os_sync_in_job_script(self.job_script_str())
        _ = self.slurm_connector.submit_and_monitor_slurm_job(job_script=job_script)

        # get the files from the object store and return the data
        return self.os_connector.read_files_from_os(self.output_files)


# if __name__ == "__main__":
#     # SLURM Credential
#     slurm_data = {
#         "url": "https://slurm.snellius.surf.nl",
#         "api_ver": "v0.0.43",
#         "user_name": "nicolasr",
#         "slurm_jwt": "",
#         "cwd": "/home/nicolasr/test_rsa",
#     }

#     # Object Store Credential
#     os_data = {
#         "url": "https://objectstore.surf.nl",
#         "os_access_key": "",
#         "os_secret_key": "",
#     }

#     tool = HPCTool(slurm_data=slurm_data, os_data=os_data)
#     tool.os_connector.upload_files_to_os(tool.input_files)
#     job_script = tool._insert_os_sync_in_job_script(tool.job_script_str())
#     tool.slurm_connector.submit_and_monitor_slurm_job(job_script=job_script, monitor_interval=10)
#     data = tool.os_connector.read_files_from_os(tool.output_files)
#     tool.os_connector.purge_bucket()
