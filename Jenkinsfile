pipeline {
    agent any

    environment {
        IMAGE_NAME = 'week12-app'
        DOCKERHUB_USER = 'khyathig'
        DEPLOYMENT_NAME = 'week12-deployment'
        DOCKER_PATH = 'C:\\Users\\khyat\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin'
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
                bat '''
                    start /B python app.py
                    ping 127.0.0.1 -n 6 > nul
                    python -m pytest -v test_app.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                    set "PATH=%DOCKER_PATH%;%PATH%"
                    docker --version
                    docker build -t %IMAGE_NAME%:latest .
                '''
                echo 'Docker image built successfully.'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-credentials',
                        usernameVariable: 'DOCKERHUB_USER_CREDENTIAL',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    bat '''
                        set "PATH=%DOCKER_PATH%;%PATH%"
                        echo %DOCKERHUB_TOKEN% | docker login -u "%DOCKERHUB_USER_CREDENTIAL%" --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-credentials',
                        usernameVariable: 'DOCKERHUB_USER_CREDENTIAL',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    bat '''
                        set "PATH=%DOCKER_PATH%;%PATH%"
                        docker tag %IMAGE_NAME%:latest "%DOCKERHUB_USER_CREDENTIAL%/%IMAGE_NAME%:latest"
                        docker push "%DOCKERHUB_USER_CREDENTIAL%/%IMAGE_NAME%:latest"
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                    kubectl apply -f deployment.yaml
                    kubectl apply -f service.yaml
                    kubectl rollout status deployment/%DEPLOYMENT_NAME% --timeout=120s
                '''
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
            echo 'Week 12 CI/CD pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the Jenkins Console Output for details.'
        }

        always {
            echo 'Week 12 pipeline execution finished.'
        }
    }
}
