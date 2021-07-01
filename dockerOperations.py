import subprocess
import json
from numpy import array as nparr


def getProcessOutput(cmd):
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE)
    process.wait()
    data, err = process.communicate()
    if process.returncode is 0:
        return 0, data.decode('utf-8')
    else:
        return 1, {}


def container_cmd(data):
    portexist = False
    string = ''
    for s in data:
        if s == "--name" and data[s] != "":
            string = string+' --name '+data['--name']
            continue
        if s == "-p":
            if data["-p"] == "":
                if data["c_p"] != "":
                    string = string+' -p '+data["c_p"]
                break
            else:
                op = getProcessOutput("netstat -tnlp")[1]
                arr = [x.split() for x in op.split('\n')]
                arr = arr[2:-1]
                narr = nparr(arr)
                m = []
                for i in narr[:, 3]:
                    m.append(i[i.rindex(":")+1:])
                if data[s] in m:
                    portexist = True
                    return portexist, ""
                string = string+f' -p {data["-p"]}:{data["c_p"]}'
                break
    return portexist, string+' '+data["image"]


def intojson(output):
    jsondata = {}
    for i, detail in enumerate(output.splitlines()):
        jsondata[i] = json.loads(detail)
    return jsondata


class container:
    def __init__(self, data):
        self.data = data

    def create(self):
        portexist, string = container_cmd(self.data)
        if(portexist):
            return 2, {}
        return getProcessOutput(f"sudo docker run -dit {string}")

    def remove(self):
        return getProcessOutput(f"sudo docker rm {self.data['id']}")

    def start(self):
        return subprocess.getstatusoutput(f"sudo docker start {self.data['id']}")

    def stop(self):
        return getProcessOutput(f"sudo docker stop {self.data['id']}")

    def inspect(self):
        return getProcessOutput(f"sudo docker inspect {self.data['id']}")

    def rename(self):
        return getProcessOutput(f"sudo docker rename {self.data['id']}  {self.data['new_container_name']}")

    def commit(self):
        return getProcessOutput(f"sudo docker commit {self.data['id']}  {self.data['new_image_name']}")

    def list(self):
        rc, output = getProcessOutput(
            "sudo docker ps -a --format='{{json .}}'")
        if rc == 0:
            jsonc = intojson(output)
            return 0, jsonc
        return rc, output


class image:
    def __init__(self, data):
        self.data = data

    def pull(self):
        return getProcessOutput(f"sudo docker pull {self.data['id']}")

    def inspect(self):
        return getProcessOutput(f"sudo docker inspect {self.data['id']}")

    def remove(self):
        return getProcessOutput(f"sudo docker rmi {self.data['id']}")

    def list(self):
        rc, output = getProcessOutput(
            "sudo docker images --format='{{json .}}'")
        if rc == 0:
            jsoni = intojson(output)
            return 0, jsoni
        return rc, output
