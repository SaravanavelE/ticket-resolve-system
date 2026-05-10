# Ticket: INC006 - Laptop is very slow

**Category:** Hardware/Performance
**Description:** User reports laptop takes 10 minutes to boot.
**Root Cause:** Antivirus full scan was running during startup.
**Resolution:** 
1. Checked Task Manager, saw high CPU from AV service.
2. Adjusted AV policy to run full scans on weekends only.
3. Rebooted machine, performance normalized.