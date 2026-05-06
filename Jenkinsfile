pipeline {
    agent any

    environment {

        SONAR_PROJECT_KEY  = 'sonarqube'
        SONAR_SCANNER_HOME = tool 'sonarqube'

        AWS_REGION = 'us-east-1'
        ECR_REPO   = 'my-repo'
        IMAGE_TAG  = 'latest'

        ECS_CLUSTER = 'sonarqube'
        ECS_SERVICE = 'sonarqube-service-n8cv0yog'

        DOCKER_CLIENT_TIMEOUT = '300'
        COMPOSE_HTTP_TIMEOUT  = '300'
    }

    stages {

        stage('Cloning Github repo to Jenkins') {

            steps {

                script {

                    echo 'Cloning Github repo to Jenkins............'

                    checkout scmGit(
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'github-token',
                            url: 'https://github.com/kumar7ashutosh/multi-ai.git'
                        ]]
                    )
                }
            }
        }

        stage('Verify Docker Environment') {

            steps {

                sh '''
                docker version
                docker info
                '''
            }
        }

        stage('SonarQube Analysis') {

            steps {

                withCredentials([
                    string(
                        credentialsId: 'sonarqube',
                        variable: 'SONAR_TOKEN'
                    )
                ]) {

                    withSonarQubeEnv('sonarqube') {

                        sh '''
                        ${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                        -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://sonarqube-dind:9000 \
                        -Dsonar.token=${SONAR_TOKEN}
                        '''
                    }
                }
            }
        }

        stage('Build and Push Docker Image to ECR') {

            steps {

                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-token'
                ]]) {

                    script {

                        def accountId = sh(
                            script: "aws sts get-caller-identity --query Account --output text",
                            returnStdout: true
                        ).trim()

                        def ecrUrl = "${accountId}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"

                        sh """
                        export DOCKER_CLIENT_TIMEOUT=300
                        export COMPOSE_HTTP_TIMEOUT=300

                        echo "Logging into AWS ECR..."

                        aws ecr get-login-password --region ${AWS_REGION} | \
                        docker login --username AWS --password-stdin \
                        ${accountId}.dkr.ecr.${AWS_REGION}.amazonaws.com

                        echo "Building Docker image..."

                        docker build -t ${ECR_REPO}:${IMAGE_TAG} .

                        echo "Tagging Docker image..."

                        docker tag ${ECR_REPO}:${IMAGE_TAG} ${ecrUrl}:${IMAGE_TAG}
                        """
                        
                        retry(3) {

                            sh """
                            echo "Pushing Docker image to ECR..."

                            docker push ${ecrUrl}:${IMAGE_TAG}
                            """
                        }
                    }
                }
            }
        }

        stage('Deploy to ECS Fargate') {

            steps {

                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-token'
                ]]) {

                    sh """
                    echo "Deploying application to ECS Fargate..."

                    aws ecs update-service \
                      --cluster ${ECS_CLUSTER} \
                      --service ${ECS_SERVICE} \
                      --force-new-deployment \
                      --region ${AWS_REGION}
                    """
                }
            }
        }
    }

    post {

        success {

            echo 'Pipeline executed successfully!'
        }

        failure {

            echo 'Pipeline failed!'
        }

        always {

            sh '''
            docker system prune -f || true
            '''
        }
    }
}