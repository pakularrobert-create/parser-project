// Full example with all language features
task full_example {
    priority: high
    depends: []
    
    // Variables
    let count = 0
    let max = 10
    let items = [1, 2, 3, 4, 5]
    let message = "Processing"
    
    // Conditional
    if count < max {
        log "Starting processing"
    } else {
        log "Already at max"
    }
    
    // Repeat loop
    repeat 3 times {
        log message
        run "echo Step"
        count = count + 1
    }
    
    // While loop
    while count < max {
        count = count + 1
        
        if count == 5 {
            log "Halfway there"
        }
    }
    
    // Complex expressions
    let result = (count + 10) * 2 - 5
    let flag = true and not false or (result > 20)
    
    if flag {
        log "All conditions met"
    }
}
