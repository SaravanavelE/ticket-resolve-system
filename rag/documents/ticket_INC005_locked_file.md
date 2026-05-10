# Ticket: INC005 - Excel File Locked

**Category:** File Share
**Description:** Cannot edit Finance.xlsx, says it is locked by another user.
**Root Cause:** A user left the file open and their session disconnected.
**Resolution:** 
1. Connected to File Server `FS01`.
2. Opened Computer Management -> Shared Folders -> Open Files.
3. Closed the open session for Finance.xlsx.
4. User can now edit.