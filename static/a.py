import subprocess
import json


def getProcessOutput(cmd):
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE)
    process.wait()
    data, err = process.communicate()
    if process.returncode is 0:
        return data.decode('utf-8')
    else:
        print("Error:", process.returncode)
    return ""


getProcessOutput("docker rmi centos:7")
# jsonia = {}
# for i, data in enumerate(getProcessOutput("docker images --format='{{json .}}'").splitlines()):
#     jsonia[i] = json.loads(data)
# print(jsonia)
