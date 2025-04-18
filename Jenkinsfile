pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'sahil069917/pathpilot:latest'
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_HUB_USR', passwordVariable: 'DOCKER_HUB_PSW')]) {
                        // Login to Docker Hub using credentials
                        sh "echo ${DOCKER_HUB_PSW} | docker login -u ${DOCKER_HUB_USR} --password-stdin"

                        // Build the Docker image
                        sh "docker build -t ${DOCKER_IMAGE} ."
                    }
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    // Reuse credentials for push if necessary
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
                sh 'docker logout'
                cleanWs()
            }
        }
    }
}
