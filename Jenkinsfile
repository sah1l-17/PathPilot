pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'sahil069917/pathpilot:latest'
        // Will be populated from credentials
        DOCKERHUB_USERNAME = credentials('dockerhub-credentials').split(':')[0]
        DOCKERHUB_PASSWORD = credentials('dockerhub-credentials').split(':')[1]
    }

    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', 
                         branches: [[name: 'main']],
                         extensions: [[$class: 'CleanBeforeCheckout']],
                         userRemoteConfigs: [[
                             url: 'https://github.com/sah1l-17/PathPilot.git',
                             credentialsId: 'github-token'
                         ]]])
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''#!/bin/bash
                    # Install system dependencies
                    sudo apt-get update -y
                    sudo apt-get install -y python3-venv python3-pip docker.io
                    
                    # Add jenkins user to docker group
                    sudo usermod -aG docker jenkins
                    newgrp docker
                '''
            }
        }

        stage('Install Python Dependencies') {
            steps {
                sh '''#!/bin/bash
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''#!/bin/bash
                    source venv/bin/activate
                    pytest --maxfail=1 --disable-warnings --tb=short
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Login to Docker Hub first
                    sh "echo ${DOCKERHUB_PASSWORD} | docker login -u ${DOCKERHUB_USERNAME} --password-stdin"
                    
                    // Build with cache and metadata
                    dockerImage = docker.build("${DOCKERHUB_USERNAME}/pathpilot:latest", 
                        "--build-arg ENV=production .")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Deploy Locally') {
            environment {
                GROQ_API_KEY = credentials('groq-api-key')
            }
            steps {
                sh '''#!/bin/bash
                    # Stop and remove existing container if running
                    docker stop pathpilot_container || true
                    docker rm pathpilot_container || true
                    
                    # Run new container with proper resource limits
                    docker run -d \
                        --name pathpilot_container \
                        -p 5000:5000 \
                        -e GROQ_API_KEY=${GROQ_API_KEY} \
                        --memory="1g" \
                        --cpus="1.0" \
                        ${DOCKERHUB_USERNAME}/pathpilot:latest
                '''
            }
        }
    }

    post {
        always {
            sh 'docker logout'  // Clean up docker credentials
            cleanWs()  // Clean workspace
        }
        success {
            slackSend(color: 'good', message: "Build Successful: ${env.BUILD_URL}")
        }
        failure {
            slackSend(color: 'danger', message: "Build Failed: ${env.BUILD_URL}")
        }
    }
}
