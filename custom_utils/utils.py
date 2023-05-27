
import subprocess
from custom_utils.configurer.utils import logger

def run_cli_command(command):
    """
    Run S3 CLI
    :param string command: command to run
    :return output : output of the command
    """
    try:
        cli_cmd = command.split()
        p = subprocess.Popen(cli_cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        output, _ = p.communicate()
        output = output.decode('utf-8')
        return output
    except Exception as err:
            logger.error(err)

