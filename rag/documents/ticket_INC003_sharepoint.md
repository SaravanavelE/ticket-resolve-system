# Ticket: INC003 - SharePoint Access Denied

**Category:** Access Rights
**Description:** User gets access denied on the Finance SharePoint site.
**Root Cause:** User was removed from the Finance AD group during an automated sync.
**Resolution:** 
1. Verified user's department with HR.
2. Re-added user to the `SEC-Finance-Users` AD group.
3. Instructed user to wait 15 minutes for sync and try again.