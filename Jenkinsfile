pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'sahil069917/pathpilot:latest'
        DOCKERHUB = credentials('dockerhub-credentials')
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
                    // Login to Docker Hub using the credentials
                    sh "echo ${DOCKERHUB_PSW} | docker login -u ${DOCKERHUB_USR} --password-stdin"
                    
                    // Build the Docker image
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    // Push the image to Docker Hub
                    sh "docker push ${DOCKER_IMAGE}"
                }
            }
        }
        
        stage('Run Docker Container') {
            environment {
                GROQ_API_KEY = credentials('groq-api-key')
            }
            steps {
                script {
                    // Stop and remove any existing container
                    sh "docker stop pathpilot_container || true"
                    sh "docker rm pathpilot_container || true"
                    
                    // Run the container with proper environment variables
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
        
        // Add a cleanup stage instead of using post
        stage('Cleanup') {
            steps {
                sh 'docker logout'
                cleanWs()
            }
        }
    }
}
