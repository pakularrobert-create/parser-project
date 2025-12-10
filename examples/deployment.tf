// Deployment Workflow
// Alkalmazás telepítési folyamat

task prepare_environment {
    priority: high
    
    log "Preparing deployment environment"
    run "mkdir -p /opt/app"
    run "mkdir -p /opt/app/logs"
    
    let ready = true
    if ready {
        log "Environment ready for deployment"
    }
}

task build_application {
    priority: high
    depends: [prepare_environment]
    
    log "Building application"
    
    run "npm install"
    run "npm run build"
    
    log "Build completed"
}

task run_tests {
    priority: high
    depends: [build_application]
    
    log "Running test suite"
    
    let test_count = 0
    repeat 3 times {
        run "npm test"
        test_count = test_count + 1
    }
    
    log "All tests passed"
}

task deploy_to_server {
    priority: medium
    depends: [run_tests]
    
    log "Deploying to production server"
    
    run "rsync -avz dist/ server:/opt/app/"
    run "systemctl restart app.service"
    
    log "Deployment successful"
}

task health_check {
    priority: medium
    depends: [deploy_to_server]
    
    log "Performing health check"
    
    let attempts = 0
    let max_attempts = 10
    let healthy = false
    
    while attempts < max_attempts and not healthy {
        run "curl -f http://localhost:8080/health"
        attempts = attempts + 1
    }
    
    if healthy {
        log "Application is healthy"
    } else {
        log "Health check failed!"
    }
}

task notify_team {
    priority: low
    depends: [health_check]
    
    log "Notifying team about deployment"
    run "echo 'Deployment completed' | mail -s 'Deploy Status' team@example.com"
}
