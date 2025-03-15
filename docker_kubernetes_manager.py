import os
import subprocess
import json
import time


class DockerManager:
    def __init__(self):
        print("Initializing Docker Manager...")

    def run_command(self, command):
        """Execute a system command and return the output."""
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(f"Error executing command: {command}\n{stderr.decode()}")
            return None
        return stdout.decode()

    def list_containers(self):
        """List all Docker containers."""
        command = ["docker", "ps", "-a", "--format", "{{.ID}} {{.Names}} {{.Status}}"]
        return self.run_command(command)

    def pull_image(self, image_name):
        """Pull a Docker image from the registry."""
        command = ["docker", "pull", image_name]
        return self.run_command(command)

    def run_container(self, image_name, name=None):
        """Run a new Docker container."""
        command = ["docker", "run", "-d"]
        if name:
            command += ["--name", name]
        command.append(image_name)
        return self.run_command(command)

    def stop_container(self, container_name):
        """Stop a running Docker container."""
        command = ["docker", "stop", container_name]
        return self.run_command(command)

    def remove_container(self, container_name):
        """Remove a stopped Docker container."""
        command = ["docker", "rm", container_name]
        return self.run_command(command)

    def remove_image(self, image_name):
        """Remove a Docker image."""
        command = ["docker", "rmi", image_name]
        return self.run_command(command)


class KubernetesManager:
    def __init__(self):
        print("Initializing Kubernetes Manager...")

    def run_command(self, command):
        """Execute a system command and return the output."""
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(f"Error executing command: {command}\n{stderr.decode()}")
            return None
        return stdout.decode()

    def list_pods(self):
        """List all Kubernetes pods."""
        command = ["kubectl", "get", "pods", "-o", "json"]
        output = self.run_command(command)
        if output:
            return json.loads(output)
        return None

    def create_deployment(self, deployment_name, image_name):
        """Create a new Kubernetes deployment."""
        command = ["kubectl", "create", "deployment", deployment_name, "--image", image_name]
        return self.run_command(command)

    def scale_deployment(self, deployment_name, replicas):
        """Scale a Kubernetes deployment."""
        command = ["kubectl", "scale", "deployment", deployment_name, "--replicas", str(replicas)]
        return self.run_command(command)

    def delete_deployment(self, deployment_name):
        """Delete a Kubernetes deployment."""
        command = ["kubectl", "delete", "deployment", deployment_name]
        return self.run_command(command)

    def get_logs(self, pod_name):
        """Get logs from a specific pod."""
        command = ["kubectl", "logs", pod_name]
        return self.run_command(command)

    def exec_command_in_pod(self, pod_name, command):
        """Execute a command inside a running pod."""
        exec_command = ["kubectl", "exec", pod_name, "--"] + command
        return self.run_command(exec_command)


def main():
    print("Docker and Kubernetes Manager")
    docker_manager = DockerManager()
    k8s_manager = KubernetesManager()

    # Example Docker usage
    print("\nDocker - List Containers:")
    print(docker_manager.list_containers())

    print("\nDocker - Pull nginx Image:")
    print(docker_manager.pull_image("nginx"))

    print("\nDocker - Run a Container:")
    print(docker_manager.run_container("nginx", name="my-nginx"))

    print("\nDocker - Stop the Container:")
    print(docker_manager.stop_container("my-nginx"))

    print("\nDocker - Remove the Container:")
    print(docker_manager.remove_container("my-nginx"))

    print("\nDocker - Remove nginx Image:")
    print(docker_manager.remove_image("nginx"))

    # Example Kubernetes usage
    print("\nKubernetes - Create Deployment:")
    print(k8s_manager.create_deployment("my-nginx-deployment", "nginx"))

    print("\nKubernetes - List Pods:")
    pods = k8s_manager.list_pods()
    print(json.dumps(pods, indent=2))

    print("\nKubernetes - Scale Deployment:")
    print(k8s_manager.scale_deployment("my-nginx-deployment", 3))

    print("\nKubernetes - Get Logs from Pod:")
    pod_name = pods['items'][0]['metadata']['name'] if pods and 'items' in pods else 'my-nginx-deployment-xxxxx'
    print(k8s_manager.get_logs(pod_name))

    print("\nKubernetes - Delete Deployment:")
    print(k8s_manager.delete_deployment("my-nginx-deployment"))


if __name__ == "__main__":
    main()