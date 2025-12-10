// TaskFlow példa program

task setup {
    priority: high
    log "Környezet előkészítése"
    run "mkdir -p /tmp/project"
}

task build {
    priority: medium
    depends: [setup]
    
    let attempts = 3
    
    repeat attempts times {
        run "make build"
    }
    
    if attempts > 0 {
        log "Build kész"
    }
}

task test {
    priority: low
    depends: [build]
    
    let i = 0
    while i < 5 {
        run "pytest"
        i = i + 1
    }
    
    log "Tesztek befejezve"
}
