// Loop statements
task loops {
    let counter = 0
    
    repeat 5 times {
        log "Repeat iteration"
        counter = counter + 1
    }
    
    while counter < 10 {
        log "While iteration"
        counter = counter + 1
    }
}
