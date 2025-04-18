pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'sahil069917/pathpilot:latest'
        DOCKER_UBERNAME = credentials('dockerhub-credentials')
    }

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm  // 👈 Simplified checkout
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Login to Docker Hub
                    sh "echo ${env.DOCKERHUB_PASSWORD} | docker login -u ${env.DOCKERHUB_USERNAME} --password-stdin"
                    
                    // Build with simplified syntax
                    docker.build("${env.DOCKER_IMAGE}").inside("--network host") {
                        // Optional: Run tests inside the container
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
                        docker.image("${env.DOCKER_IMAGE}").push()
                        docker.image("${env.DOCKER_IMAGE}").push('latest')
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
                    docker.image("${env.DOCKER_IMAGE}").run(
                        "-d --name pathpilot_container " +
                        "-p 5000:5000 " +
                        "-e GROQ_API_KEY=${GROQ_API_KEY} " +
                        "--memory='1g' " +
                        "--cpus='1.0'"
                    )
                }
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