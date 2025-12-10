// Complex workflow with multiple tasks
task setup {
    priority: high
    log "Setting up environment"
    run "mkdir -p /tmp/project"
}

task build {
    priority: medium
    depends: [setup]
    
    log "Building project"
    run "make build"
    
    let status = "success"
    if status == "success" {
        log "Build completed successfully"
    }
}

task test {
    priority: low
    depends: [build]
    
    log "Running tests"
    run "make test"
}
