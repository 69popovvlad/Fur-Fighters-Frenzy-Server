import docker
from flask import Flask, request, jsonify
from constants import INTERNAL_PORT, CONTAINER_NAME_MASK

app = Flask(__name__)
client = docker.from_env()


@app.route('/<container_id>/someaction', methods=['GET'])
def some_action(container_id):
    # Ваша логика обработки запроса someaction
    return jsonify({'message': f'Some action performed for container {container_id}'})


@app.route('/<container_id>/stop_me', methods=['POST'])
def stop_and_restart_container(container_id):
    container_name = f"{CONTAINER_NAME_MASK}{container_id}"

    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
        # Здесь вы можете добавить логику для создания нового контейнера с тем же портом и уникальным ID
        return jsonify({'message': f'Container {container_id} stopped and removed'})
    except docker.errors.NotFound:
        return jsonify({'error': f'Container {container_id} not found'}), 404


if __name__ == "__main__":
    app.run(port=INTERNAL_PORT)
