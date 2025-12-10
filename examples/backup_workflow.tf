// Backup Workflow
// Automatizált mentési feladatok

task check_disk_space {
    priority: high
    
    log "Checking available disk space"
    run "df -h"
    
    let space_available = true
    if space_available {
        log "Sufficient disk space available"
    } else {
        log "Warning: Low disk space!"
    }
}

task backup_files {
    priority: high
    depends: [check_disk_space]
    
    log "Starting backup process"
    
    let backup_count = 0
    let max_backups = 5
    
    repeat max_backups times {
        run "tar -czf backup.tar.gz /data"
        backup_count = backup_count + 1
        log "Backup created"
    }
}

task verify_backup {
    priority: medium
    depends: [backup_files]
    
    log "Verifying backup integrity"
    run "tar -tzf backup.tar.gz"
    
    let verified = true
    if verified {
        log "Backup verification successful"
    } else {
        log "Backup verification failed!"
    }
}

task cleanup_old_backups {
    priority: low
    depends: [verify_backup]
    
    log "Cleaning up old backups"
    
    let days_to_keep = 7
    run "find /backups -mtime +7 -delete"
    
    log "Cleanup completed"
}
