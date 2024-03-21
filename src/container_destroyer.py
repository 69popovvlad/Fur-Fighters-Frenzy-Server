import docker

client = docker.from_env()


def destroy_container(container_name):
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove(force=True)
        while True:
            try:
                client.containers.get(container_name)
            except docker.errors.NotFound:
                print(
                    f"Removed existing container with name: {container_name}")
                break
    except docker.errors.NotFound:
        print(f"No existing container found with name: {container_name}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python container_creator.py <container_name>")
        sys.exit(1)

    container_name = sys.argv[1]
    container_name = destroy_container(container_name)
