run-app:
	docker build -t jenkins-lab-app:dev -f app/Dockerfile .
	docker run --rm -p 8000:8000 jenkins-lab-app:dev
