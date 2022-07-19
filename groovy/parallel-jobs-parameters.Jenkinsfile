// assuming job-test-01 as payg
// job-test-02 as scheds
// job-test-03 as notification

pipeline {

    parameters {
      choice(name: 'MultipleJobs', choices: ['all', 'job-01-02', 'job-01-03', 'job-02-03'], description: '')
    }

    agent any
    stages {
        stage('All Jobs') {
            parallel {
                stage('Parallel All') {

                    when {
                        expression {
                            env.MultipleJobs == "all"
                        }
                    }

                    steps {
                        script {
                            def group1 = [:]
                            group1["Job01"] = {
                                echo "Job01"
                                sh(script: "date -u")
                                build(job: 'job-test-01')
                            }
                            group1["Job02"] = {
                                echo "Job02"
                                sh(script: "date -u")
                                build(job: 'job-test-02')
                            }
                            group1["Job03"] = {
                                echo "Job03"
                                sh(script: "date -u")
                                build(job: 'job-test-03')
                            }
                            parallel group1
                        }
                    }
                }
                stage('Parallel Job01 & Job02') {

                    when {
                        expression {
                            env.MultipleJobs == "job-01-02"
                        }
                    }

                    steps {
                        script {
                            def group1 = [:]
                            group1["Job01"] = {
                                echo "Job01"
                                sh(script: "date -u")
                                build(job: 'job-test-01')
                            }
                            group1["Job02"] = {
                                echo "Job02"
                                sh(script: "date -u")
                                build(job: 'job-test-02')
                            }
                            parallel group1
                        }
                    }
                }
                stage('Parallel Job01 & Job03') {

                    when {
                        expression {
                            env.MultipleJobs == "job-01-03"
                        }
                    }

                    steps {
                        script {
                            def group1 = [:]
                            group1["Job01"] = {
                                echo "Job01"
                                sh(script: "date -u")
                                build(job: 'job-test-01')
                            }
                            group1["Job02"] = {
                                echo "Job02"
                                sh(script: "date -u")
                                build(job: 'job-test-03')
                            }
                            parallel group1
                        }
                    }
                }
                stage('Parallel Job02 & Job03') {

                    when {
                        expression {
                            env.MultipleJobs == "job-02-03"
                        }
                    }

                    steps {
                        script {
                            def group1 = [:]
                            group1["Job01"] = {
                                echo "Job01"
                                sh(script: "date -u")
                                build(job: 'job-test-02')
                            }
                            group1["Job02"] = {
                                echo "Job02"
                                sh(script: "date -u")
                                build(job: 'job-test-03')
                            }
                            parallel group1
                        }
                    }
                }
            }
        }
    }
}