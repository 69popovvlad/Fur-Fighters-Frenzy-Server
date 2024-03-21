import docker
import subprocess
from constants import EXTERNAL_SERVER_IP, IMAGE_NAME, CONTAINER_NAME_MASK, EXECUTABLE_FILE_PATH, START_PORT

client = docker.from_env()


def create_container(container_id):
    external_port = START_PORT + container_id
    container_name = f"{CONTAINER_NAME_MASK}{container_id}"

    destroy_container(container_name)

    container = client.containers.run(
        IMAGE_NAME,
        name=container_name,
        ports={
            f"{external_port}/tcp": external_port,
            f"{external_port}/udp": external_port,
        },
        detach=True,
        command=[EXECUTABLE_FILE_PATH, "--server", "--serverBindAddressIpv4",
                 EXTERNAL_SERVER_IP, "--serverPort", str(external_port)]
    )

    print(f"Container created with ID: {container.id}")


def destroy_container(container_name):
    subprocess.run(["python", "container_destroyer.py", str(container_name)])


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python container_creator.py <container_id>")
        sys.exit(1)

    container_id = int(sys.argv[1])
    create_container(container_id)
