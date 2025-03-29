install:
	pip install -r requirements.txt

run:
	python3 main.py

run-docker:
	python3 main.py

docker-up:
	open -a XQuartz
	sleep 5          
	export DISPLAY=:0     
	xhost + 127.0.0.1
	export XDG_RUNTIME_DIR=/tmp/runtime
	docker compose up --build

docker-down:
	docker compose down

