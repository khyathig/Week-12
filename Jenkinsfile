pipeline {
    agent any

    environment {
        IMAGE_NAME = 'week12-app'
        DEPLOYMENT_NAME = 'week12-deployment'
    }

    stages {

        stage('Checkout SCM') {
            steps {
                checkout scm
                echo 'Source code checked out successfully.'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Selenium Tests with Pytest') {
            steps {
                bat 'start /B python app.py'
                bat 'ping 127.0.0.1 -n 6 > nul'
                bat 'python -m pytest -v test_app.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:latest .'
                echo 'Docker image built successfully.'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-credentials',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    bat '''
                        @echo off
                        echo %DOCKERHUB_TOKEN% | docker login -u "%DOCKERHUB_USER%" --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-credentials',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    bat '''
                        docker tag %IMAGE_NAME%:latest "%DOCKERHUB_USER%/%IMAGE_NAME%:latest"
                        docker push "%DOCKERHUB_USER%/%IMAGE_NAME%:latest"
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-credentials',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    bat '''
                        powershell -NoProfile -Command "(Get-Content deployment.yaml) -replace 'YOUR_DOCKERHUB_USERNAME', $env:DOCKERHUB_USER | Set-Content deployment.yaml"

                        kubectl apply -f deployment.yaml
                        kubectl apply -f service.yaml

                        kubectl rollout status deployment/%DEPLOYMENT_NAME% --timeout=120s
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                bat 'kubectl get deployments'
                bat 'kubectl get pods'
                bat 'kubectl get services'
            }
        }
    }

    post {
        success {
            echo 'Week 12 pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the Jenkins console output.'
        }
    }
}