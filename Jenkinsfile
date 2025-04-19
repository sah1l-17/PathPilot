pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'sahil069917/pathpilot:latest'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/sah1l-17/PathPilot.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    python test_app.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_HUB_USR', passwordVariable: 'DOCKER_HUB_PSW')]) {
                        sh "echo ${DOCKER_HUB_PSW} | docker login -u ${DOCKER_HUB_USR} --password-stdin"
                        sh "docker build -t ${DOCKER_IMAGE} ."
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_HUB_USR', passwordVariable: 'DOCKER_HUB_PSW')]) {
                        sh "echo ${DOCKER_HUB_PSW} | docker login -u ${DOCKER_HUB_USR} --password-stdin"
                        sh "docker push ${DOCKER_IMAGE}"
                    }
                }
            }
        }

        stage('Run Docker Container') {
            environment {
                GROQ_API_KEY = credentials('groq-api-key')
            }
            steps {
                script {
                    sh "docker stop pathpilot_container || true"
                    sh "docker rm pathpilot_container || true"

                    sh """
                        docker run -d --name pathpilot_container \
                        -p 5000:5000 \
                        -e GROQ_API_KEY=${GROQ_API_KEY} \
                        --memory='1g' \
                        --cpus='1.0' \
                        ${DOCKER_IMAGE}
                    """
                }
            }
        }

        stage('Cleanup') {
            steps {
                sh '''
                    docker logout
                    deactivate || true
                    rm -rf venv
                '''
                cleanWs()
            }
        }
    }
}
