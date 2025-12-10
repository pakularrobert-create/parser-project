// Data Processing Workflow
// Adatfeldolgozási pipeline

task load_data {
    priority: high
    
    log "Loading data from sources"
    
    let sources = ["db1", "db2", "db3"]
    let loaded = 0
    
    repeat 3 times {
        run "python load_data.py"
        loaded = loaded + 1
    }
    
    log "Data loading completed"
}

task validate_data {
    priority: high
    depends: [load_data]
    
    log "Validating data quality"
    
    let valid_records = 0
    let total_records = 1000
    
    while valid_records < total_records {
        valid_records = valid_records + 100
    }
    
    if valid_records == total_records {
        log "All records validated successfully"
    }
}

task transform_data {
    priority: medium
    depends: [validate_data]
    
    log "Transforming data"
    
    let transformations = ["normalize", "aggregate", "filter"]
    let step = 0
    
    repeat 3 times {
        run "python transform.py"
        step = step + 1
        log "Transformation step completed"
    }
}

task analyze_data {
    priority: medium
    depends: [transform_data]
    
    log "Analyzing processed data"
    
    run "python analyze.py"
    
    let insights = 42
    if insights > 0 {
        log "Analysis completed with insights"
    } else {
        log "No significant insights found"
    }
}

task generate_report {
    priority: low
    depends: [analyze_data]
    
    log "Generating final report"
    
    run "python report.py"
    run "python export_pdf.py"
    
    log "Report generated successfully"
}

task archive_results {
    priority: low
    depends: [generate_report]
    
    log "Archiving results"
    
    let archive_path = "/archive/data"
    run "tar -czf results.tar.gz /output"
    run "mv results.tar.gz /archive/"
    
    log "Results archived"
}
