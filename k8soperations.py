from kubernetes import client, config
import json
config.load_kube_config('admin.conf')
apps_api = client.AppsV1Api()
v1 = client.CoreV1Api()


class ns:
    def __init__(self, data):
        self.data = data
        self.fail_mess = "sorry! There is something wrong in configuration, we can not proceed this request"

    def create(self):
        try:
            ns = client.V1Namespace()
            ns.metadata = client.V1ObjectMeta(name=self.data["name"])
            rdata = v1.create_namespace(ns, pretty='true')
            return 0, "namespace successfully created", str(rdata)
        except Exception as e:
            return 1, self.fail_mess, str(e)

    def delete(self):
        try:
            rdata = v1.delete_namespace(name=self.data["name"], pretty='true')
            return 0, "namespace successfully deleted", str(rdata)
        except Exception as e:
            return 1, self.fail_mess, str(e)

    def show_all(self):
        try:
            nss = v1.list_namespace()

            namespace_list = {'namespace': {}}
            for index, item in enumerate(nss.items):
                namespace_list['namespace'][str(index)] = item.metadata.name
            json_object = json.loads(str(namespace_list).replace("'", '"'))
            json_formatted_str = json.dumps(json_object, indent=4)
            return 0, "To see information about particular pod you can tell me to describe them with their name", json_formatted_str
        except Exception as e:
            return 1, self.fail_mess, str(e)

    def describe(self):
        try:
            rdata = v1.read_namespace(name=self.data["name"], pretty='true')
            return 0, f'Namespace: {self.data["name"]}', str(rdata)
        except Exception as e:
            return 1, self.fail_mess, str(e)
    create.struct = delete.struct = describe.struct = {
        "name": {
            "value": "",
            "desc": "Namespace name",
            "dtype": "string",
            "placeholder": "Type here",
        },
    }
    show_all.struct = {}
    list_all = show_all
    show = describe
    remove = delete


class pod:
    def __init__(self, data):
        self.data = data
        self.fail_mess = "sorry! There is something wrong in configuration, we can not proceed this request"
        print(type(self.data))

    def configuration(self):
        pod = client.V1Pod()
        pod.metadata = client.V1ObjectMeta(
            name=self.data["name"], labels=eval(self.data["labels"]))
        spec = client.V1PodSpec(containers=int(self.data["containers"]))
        if not len(self.data["port"]) == 0:
            ports = [client.V1ContainerPort(
                container_port=int(self.data["port"]))]
        else:
            ports = []
        container = client.V1Container(
            name=self.data["container_name"],
            ports=ports
        )
        container.image = self.data["image"]
        spec.containers = [container]
        pod.spec = spec
        return pod

    def create(self):
        try:
            rdata = v1.create_namespaced_pod(
                namespace=self.data["namespace"], body=self.configuration(), pretty='true')
            return 0, "Pod successfully created", str(rdata)
        except Exception as e:
            return 1, self.fail_mess, str(e)

    def delete(self):
        try:
            rdata = v1.delete_namespaced_pod(
                name=self.data["name"], namespace=self.data["namespace"], body=client.V1DeleteOptions(), pretty='true')
            return 0, "Pod successfully deleted", str(rdata)
        except Exception as e:
            return 1, self.fail_mess, str(e)

    def show_all(self):
        try:
            pods = v1.list_namespaced_pod(namespace=self.data["namespace"])
            pod_list = {}
            for item in pods.items:
                pod_list[str(item.metadata.name)] = {}
                pod_list[str(item.metadata.name)
                         ]["namespace"] = item.metadata.namespace
                pod_list[str(item.metadata.name)]["status"] = item.status.phase

            json_object = json.loads(str(pod_list).replace("'", '"'))
            json_formatted_str = json.dumps(json_object, indent=4)
            return 0, "To see information about particular pod you can tell me to describe them with their name", json_formatted_str
        except Exception as e:
            return 1, self.fail_mess, str(e)

    def delete_all(self):
        try:
            rdata = v1.delete_collection_namespaced_pod(
                self.data["namespace"], pretty='true')
            return 0, "Process started it may take some time", str(rdata)
        except Exception as e:
            return 1, self.fail_mess, str(e)

    def describe(self):
        try:
            rdata = v1.read_namespaced_pod(
                namespace=self.data["namespace"], name=self.data["name"], pretty='true')
            return 0, f'Pod: {self.data["name"]}', str(rdata)
        except Exception as e:
            return 1, self.fail_mess, str(e)
    create.struct = {
        "name": {
            "value": "null",
            "desc": "Name",
            "dtype": "string",
            "placeholder": "Type here",
        },
        "namespace": {
            "value": "default",
            "desc": "Namespace",
            "dtype": "string",
            "placeholder": "Type here",
        },
        "container_name": {
            "value": "null",
            "desc": "Container Name",
            "dtype": "string",
            "placeholder": "Type here",
        },
        "containers": {
            "value": "1",
            "desc": "Container's Count",
            "dtype": "number",
            "placeholder": "1",
        },
        "image": {
            "value": "null",
            "desc": "Image",
            "dtype": "string",
            "placeholder": "Image:tag",
        },
        "port": {
            "value": "null",
            "desc": "Expose port",
            "dtype": "number",
            "placeholder": "80",
        },
        "labels": {
            "value": "null",
            "desc": "Labels",
            "dtype": "dict",
            "placeholder": "should be json object",
        },
    }
    delete.struct = {
        "name": {
            "value":  "null",
            "desc": "Name of pod",
            "dtype": "string",
            "placeholder": "Type here",
        },
        "namespace": {
            "value": "default",
            "desc": "Namespace of pod",
            "dtype": "string",
            "placeholder": "Type here",
        },
    }
    describe.struct = delete.struct
    show_all.struct = delete_all.struct = {
        "namespace": {
            "value": 'default',
            "desc": "Namespace",
            "dtype": "string",
            "placeholder": "Type here",
        },
    }
    list_all = show_all
    show = describe
    launch = run = create


class deploy:
    def __init__(self, data):
        self.data = data
        self.fail_mess = "sorry! There is something wrong in configuration, we can not proceed this request"

    def configuration(self):
        if not len(self.data["port"]) == 0:
            ports = [client.V1ContainerPort(
                container_port=int(self.data["port"]))]
        else:
            ports = []
        container = client.V1Container(
            name=self.data["container_name"],
            image=self.data["image"],
            ports=ports
        )
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels=eval(self.data["labels"])),
            spec=client.V1PodSpec(containers=[container])
        )
        spec = client.V1DeploymentSpec(
            replicas=int(self.data["replicas"]),
            selector=client.V1LabelSelector(
                match_labels=eval(self.data["labels"])),
            template=template
        )
        deployment = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name=self.data["name"]),
            spec=spec
        )
        return deployment

    def create(self):
        try:
            rdata = apps_api.create_namespaced_deployment(
                namespace=self.data["namespace"],
                body=self.configuration(),
                pretty='true'
            )
            return 0, "deployment created successfully", str(rdata)
        except Exception as e:
            return 1, self.fail_mess, str(e)

    def delete(self):
        try:
            rdata = apps_api.delete_namespaced_deployment(name=self.data["name"], namespace=self.data["namespace"], body=client.V1DeleteOptions(
                propagation_policy="Foreground", grace_period_seconds=1), pretty='true')
            return 0, "deployment deleted successfully", str(rdata)
        except Exception as e:
            return 1, self.fail_mess, str(e)

    def update(self):
        try:
            rdata = apps_api.replace_namespaced_deployment(
                name=self.data["name"], namespace=self.data["namespace"], body=self.configuration(), pretty='true')
            return 0, "deployment updated successfully", str(rdata)
        except Exception as e:
            return 1, self.fail_mess, str(e)

    def show_all(self):
        try:
            deps = apps_api.list_namespaced_deployment(
                namespace=self.data["namespace"])
            deployment_list = {}
            for item in deps.items:
                deployment_list[str(item.metadata.name)] = {}
                # deployment_list[str(item.metadata.name)]["name"] = item.metadata.name
                deployment_list[str(item.metadata.name)
                                ]["replicas"] = item.spec.replicas
                deployment_list[str(item.metadata.name)
                                ]["ready"] = str(item.status.ready_replicas)
                deployment_list[str(item.metadata.name)
                                ]["namespace"] = item.metadata.namespace
            json_object = json.loads(str(deployment_list).replace("'", '"'))
            json_formatted_str = json.dumps(json_object, indent=4)
            return 0, "To see information about particular pod you can tell me to describe them with their name", json_formatted_str
        except Exception as e:
            return 1, self.fail_mess, str(e)

    def describe(self):
        try:
            rdata = apps_api.read_namespaced_deployment(
                namespace=self.data["namespace"], name=self.data["name"], pretty='true')
            return 0, f'Deployment: {self.data["name"]}', str(rdata)
        except Exception as e:
            return 1, self.fail_mess, str(e)

    def delete_all(self):
        try:
            rdata = apps_api.delete_collection_namespaced_deployment(
                self.data["namespace"], pretty='true')
            return 0, "Process started it may take some time", str(rdata)
        except Exception as e:
            return 1, self.fail_mess, str(e)

    def scale(self):
        try:
            obj = {'spec': {'replicas': int(self.data["replicas"])}}
            rdata = apps_api.patch_namespaced_deployment_scale(
                name=self.data["name"], namespace=self.data["namespace"], body=obj, pretty='true')
            return 0, "Deployment scale successfully", str(rdata)
        except Exception as e:
            return 1, self.fail_mess, str(e)
    update.struct = create.struct = {
        "name": {
            "value": "null",
            "desc": "Name",
            "dtype": "string",
            "placeholder": "Type here",
        },
        "namespace": {
            "value": "default",
            "desc": "Namespace",
            "dtype": "string",
            "placeholder": "Type here",
        },
        "container_name": {
            "value": "null",
            "desc": "Container Name",
            "dtype": "string",
            "placeholder": "Type here",
        },
        "replicas": {
            "value": "1",
            "desc": "Replica's Count",
            "dtype": "number",
            "placeholder": "1",
        },
        "image": {
            "value": "null",
            "desc": "Image",
            "dtype": "string",
            "placeholder": "Image:tag",
        },
        "port": {
            "value": "null",
            "desc": "Expose port",
            "dtype": "number",
            "placeholder": "80",
        },
        "labels": {
            "value": "null",
            "desc": "Labels",
            "dtype": "dict",
            "placeholder": "should be json object",
        },
    }
    scale.struct = {
        "name": {
            "value": "",
            "desc": "name of deployment",
            "dtype": "string",
            "placeholder": "Type here",
        },
        "namespace": {
            "value": "default",
            "desc": "namespace of deployment",
            "dtype": "string",
            "placeholder": "Type here",
        },
        "replicas": {
            "value": "",
            "desc": "Number of replicas",
            "dtype": "number",
            "placeholder": "1",
        },
    }
    delete.struct = {
        "name": {
            "value": "",
            "desc": "name of deployment",
            "dtype": "string",
            "placeholder": "Type here",
        },
        "namespace": {
            "value": "default",
            "desc": "namespace of deployment",
            "dtype": "string",
            "placeholder": "Type here",
        },
    }
    show_all.struct = {
        "namespace": {
            "value": 'default',
            "desc": "name of namespace ",
            "dtype": "string",
            "placeholder": "Type here",
        },
    }
    describe.struct = delete.struct
    delete_all.struct = show_all.struct
    list_all = show_all
    show = describe
    launch = run = create
