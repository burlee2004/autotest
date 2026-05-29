pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            } 
        }
 
        stage('Install Python') {
            steps {
                sh 'python3 -m venv venv'
                sh 'venv/bin/pip install --upgrade pip'
                sh 'venv/bin/pip install -r requirements.txt'
                sh 'venv/bin/pip install pytest pytest-html selenium allure-pytest requests'
            }
        }

        stage('Run Automation Tests') {
            steps {
                // =========================================================================
                // 🟢 KỊCH BẢN 1: CHỈ TEST ĐỒ ÁN KHÁCH SẠN (UI & API)
                // =========================================================================
                sh 'venv/bin/pytest tests/ui/ tests/api/ 
                    --alluredir=reports/allure-results 
                    --clean-alluredir'
  
                // =========================================================================
                // 🔵 KỊCH BẢN 2: CHỈ TEST GOOGLE SEARCH
                // =========================================================================
                // sh 'venv/bin/pytest tests/google/ 
                // --alluredir=reports/allure-results 
                // --clean-alluredir'

                // =========================================================================
                // 🟠 KỊCH BẢN 3: CHỈ TEST SAUCEDEMO
                // =========================================================================
                // sh 'venv/bin/pytest tests/saucedemo/ 
                // --alluredir=reports/allure-results 
                // --clean-alluredir'
            }
        }
    }
    
    post {
        always {
            script {
                allure commandline: 'Allure', includeProperties: false, jdk: '', results: [[path: 'reports/allure-results']]
            }
        }
    }
}