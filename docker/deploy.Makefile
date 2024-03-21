###> docker ###
## Path to docker binary
DOCKER_BIN ?= $(shell test "$(USE_PODMAN)" == "yes" && echo podman || echo docker)
###< docker ###

DOCKERFILE ?= docker/Dockerfile
USER ?= root
DEPLOY_REMOTE ?= ${USER}@127.0.0.1
PROJECT_NAME ?= fur_fighters_server
EXPORT_OUT_PATH ?= /tmp/${PROJECT_NAME}.image.tar
SSH_CONFIG_FILE_PATH ?= ${HOME}/.ssh/config


build:
	${DOCKER_BIN} build --tag ${PROJECT_NAME} --file ${DOCKERFILE} .


build-export:
	"${DOCKER_BIN}" save -o "${EXPORT_OUT_PATH}" docker.io/${PROJECT_NAME}:latest


build-deploy: build-export
	rsync --verbose -rvazpc --progress -e "ssh -F ${SSH_CONFIG_FILE_PATH}" "${EXPORT_OUT_PATH}" "${DEPLOY_REMOTE}:${EXPORT_OUT_PATH}"
	ssh -F "${SSH_CONFIG_FILE_PATH}" "${DEPLOY_REMOTE}" docker load -i "${EXPORT_OUT_PATH}"


host-prepare:
	# Create directory if it doesn't exist
	ssh -F "${SSH_CONFIG_FILE_PATH}" "${DEPLOY_REMOTE}" 'mkdir -p "projects/${PROJECT_NAME}"'

	rsync -av -e "ssh" --progress --exclude-from='.gitignore' ./src/ "${DEPLOY_REMOTE}:/${USER}/projects/${PROJECT_NAME}/"


deploy: build
	${MAKE} host-prepare
	${MAKE} build-deploy

	# Run python script
	ssh -F "${SSH_CONFIG_FILE_PATH}" "${DEPLOY_REMOTE}" "\
		source projects/${PROJECT_NAME}/venv/bin/activate && \
		cd projects/${PROJECT_NAME} && \
		pip install -r requirements.txt && \
		nohup python3 main.py &"
