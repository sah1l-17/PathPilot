pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'sahil069917/pathpilot:latest'
        // Will be populated from credentials
        DOCKER_UBERNAME = credentials('dockerhub-credentials')
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
                script {
                    // Split credentials in script block
                    env.DOCKERHUB_USERNAME = env.DOCKER_UBERNAME.split(':')[0]
                    env.DOCKERHUB_PASSWORD = env.DOCKER_UBERNAME.split(':')[1]
                }
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
                    // Login to Docker Hub
                    sh "echo ${env.DOCKERHUB_PASSWORD} | docker login -u ${env.DOCKERHUB_USERNAME} --password-stdin"
                    
                    // Build with cache and metadata
                    dockerImage = docker.build("${env.DOCKERHUB_USERNAME}/pathpilot:latest", 
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
                    
                    # Run new container
                    docker run -d \
                        --name pathpilot_container \
                        -p 5000:5000 \
                        -e GROQ_API_KEY=${GROQ_API_KEY} \
                        --memory="1g" \
                        --cpus="1.0" \
                        ${env.DOCKERHUB_USERNAME}/pathpilot:latest
                '''
            }
        }
    }

    post {
        always {
            sh 'docker logout'  // Clean up docker credentials
            cleanWs()  // Clean workspace
        }
    }
}
