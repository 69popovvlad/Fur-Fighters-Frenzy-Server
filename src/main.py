import docker
import subprocess
from constants import CONTAINER_NAME_MASK, CONTAINERS_COUNT

client = docker.from_env()

def stop_and_remove_containers_by_mask(mask):
    print("Stop old containers")

    containers = client.containers.list(all=True)
    for container in containers:
        if mask in container.name:
            destroy_container(container.name)


def create_container(container_id):
    subprocess.run(["python", "container_creator.py", str(container_id)])


def destroy_container(container_name):
    subprocess.run(["python", "container_destroyer.py", str(container_name)])


def listen_and_manage_containers():
    subprocess.run(["python", "commands_listener.py"])


if __name__ == "__main__":
    # Останавливаем и удаляем контейнеры по маске
    stop_and_remove_containers_by_mask(CONTAINER_NAME_MASK)

    # Создаем N контейнеров с уникальными портами и именами
    for i in range(CONTAINERS_COUNT):
        create_container(i)

    # Запускаем слушатель для запросов от контейнеров
    listen_and_manage_containers()
