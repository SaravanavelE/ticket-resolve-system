# Runbook: Blue Screen of Death (BSOD)

## Overview
Initial troubleshooting for BSOD on company laptops.

## Steps
1. Ask user for the stop code (e.g., PAGE_FAULT_IN_NONPAGED_AREA).
2. Request user to reboot in Safe Mode.
3. Check for recent Windows Updates or Driver installations.
4. Run `sfc /scannow` and `dism /online /cleanup-image /restorehealth`.
5. If hardware failure is suspected, contact vendor (Dell/HP) for replacement.