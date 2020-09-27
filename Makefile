build:
	sudo docker build -t "timescale/tester" -f "./setup-files/timescale.Dockerfile" setup-files
run-server:
	sudo docker stop timescaledb && sudo docker rm timescaledb && sudo docker run -d --name timescaledb -p 5432:5432 timescale/tester
bash:
	sudo docker exec -ti timescaledb bash
logs:
	sudo docker logs timescaledb