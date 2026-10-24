pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 15, unit: 'MINUTES')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install \
                      -r requirements.txt \
                      -r requirements-dev.txt
                '''
            }
        }

        stage('Lint - Ruff') {
            steps {
                sh '.venv/bin/python -m ruff check .'
            }
        }

        stage('Tests - Pytest') {
            steps {
                sh '''
                    mkdir -p reports
                    .venv/bin/python -m pytest -v \
                      --junitxml=reports/pytest.xml
                '''
            }
        }

        stage('Packaging') {
            steps {
                sh '''
                    mkdir -p dist
                    tar -czf dist/incidentflow-source.tar.gz \
                      app Dockerfile \
                      requirements.txt
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true,
                  testResults: 'reports/pytest.xml'

            archiveArtifacts(
                artifacts: 'dist/*.tar.gz',
                allowEmptyArchive: true,
                fingerprint: true
            )

            deleteDir()
        }
    }
}