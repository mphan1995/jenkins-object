pipeline {
  agent { label 'built-in' }

  environment {
    REGISTRY   = "localhost:5000"
    IMAGE_NAME = "jenkins-lab-app"
    IMAGE_TAG  = "${env.BUILD_NUMBER}"
    FULL_IMAGE = "${env.REGISTRY}/${env.IMAGE_NAME}:${env.IMAGE_TAG}"
    PYTHON     = "python3"
  }

  options {
    timestamps()
    //ansiColor('xterm')
    buildDiscarder(logRotator(numToKeepStr: '20'))
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Unit Tests') {
      steps {
        sh '''
          ${PYTHON} -m venv .venv
          . .venv/bin/activate
          pip install -r app/requirements.txt pytest
          pytest -q
        '''
      }
    }

    stage('Build Image') {
      steps {
        sh '''
          docker build -t ${IMAGE_NAME}:build -f app/Dockerfile .
          docker tag ${IMAGE_NAME}:build ${FULL_IMAGE}
        '''
      }
    }

    stage('Push Registry') {
      steps {
        sh '''
          docker push ${FULL_IMAGE}
          docker tag ${FULL_IMAGE} ${REGISTRY}/${IMAGE_NAME}:latest
          docker push ${REGISTRY}/${IMAGE_NAME}:latest
        '''
      }
    }

    stage('Ansible Deploy') {
      steps {
        sh '''
          python3 -m pip install --user ansible==9.5.1
          export PATH="$HOME/.local/bin:$PATH"
          cd ansible
          IMAGE_TAG=${IMAGE_TAG:-latest} ansible-playbook -i inventory.ini deploy.yml
        '''
      }
    }
  }
}
