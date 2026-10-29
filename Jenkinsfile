pipeline {
    agent any

    environment {
        PATH = "C:\\Users\\khyat\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Selenium Tests') {
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
                echo 'Build Docker Image'
                bat 'docker build -t week12-app:latest .'
            }
        }

        stage('Docker Login') {
            steps {
                bat 'docker login -u khyathig -p Docker@123'
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                echo 'Push Docker Image to Docker Hub'
                bat 'docker tag week12-app:latest khyathig/week12-app:latest'
                bat 'docker push khyathig/week12-app:latest'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f deployment.yaml'
                bat 'kubectl apply -f service.yaml'
                bat 'kubectl rollout status deployment/week12-deployment --timeout=120s'
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
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
