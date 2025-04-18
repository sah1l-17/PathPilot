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
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                sh 'pip install -r requirements.txt'
                '''
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
