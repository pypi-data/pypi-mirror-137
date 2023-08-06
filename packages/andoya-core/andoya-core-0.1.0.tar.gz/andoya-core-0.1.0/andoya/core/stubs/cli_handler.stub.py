import base64
import os
import subprocess


def handle(event, context):
    command = event["command"]

    result = subprocess.run(
        command,
        capture_output=True,
        cwd=os.getenv("LAMBDA_TASK_ROOT"),
        shell=True,
    )

    return {
        "requestId": os.getenv("AWS_REQUEST_ID"),
        "logGroup": os.getenv("AWS_LAMBDA_LOG_GROUP_NAME"),
        "logStream": os.getenv("AWS_LAMBDA_LOG_STREAM_NAME"),
        "exitCode": result.returncode,
        "output": base64.b64encode(
            result.stdout if result.returncode == 0 else result.stderr
        ),
    }
