pipeline {
  agent any
  stages {
    stage('test') {
      steps {
        sh '''virtualenv venv --distribute
./venv/bin/activate
pip install -r requirements.txt'''
      }
    }

  }
}