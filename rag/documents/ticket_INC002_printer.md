# Ticket: INC002 - Cannot map network printer

**Category:** Hardware/Peripherals
**Description:** User unable to map the 3rd floor marketing printer.
**Root Cause:** Spooler service was hung on user's machine.
**Resolution:** 
1. Opened Services.msc.
2. Restarted Print Spooler service.
3. Re-mapped printer using `\\printserver01\MKT-3FL-PTR`.
4. Printed test page successfully.