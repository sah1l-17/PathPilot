pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'sahil069917/pathpilot:latest'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url:'https://github.com/sah1l-17/PathPilot.git'
            }
        }docker run -d \
  -p 8888:8080 \               # Jenkins UI on localhost:8888
  -p 50001:50000 \             # Agent communication port
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name jenkins-pathpilot \
  jenkins/jenkins:lts


        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest --maxfail=1 --disable-warnings --tb=short'
            }
        }


        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKERHUB_USERNAME}/pathpilot:latest")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', 'dockerhub-credentials') {
                        dockerImage.push()
                    }
                }
            }
        }

        stage('Deploy Locally') {
            environment {
                GROQ_API_KEY = credentials('groq-api-key')
            }
            steps {
                sh """
                docker run -d -p 5000:5000 \\
                    -e GROQ_API_KEY=$GROQ_API_KEY \\
                    --name pathpilot_container \\
                    ${DOCKERHUB_USERNAME}/pathpilot:latest
                """
            }
        }

    }
}
