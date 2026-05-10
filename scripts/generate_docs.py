import os

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rag", "documents")

DOCUMENTS = [
    {
        "filename": "runbook_password_reset.md",
        "content": "# Runbook: Active Directory Password Reset\n\n## Overview\nThis SOP details how to reset an AD password.\n\n## Steps\n1. Verify user identity via alternate email or manager.\n2. Open Active Directory Users and Computers.\n3. Locate user account.\n4. Right-click -> Reset Password.\n5. Ensure 'User must change password at next logon' is checked.\n6. Notify user of temporary password."
    },
    {
        "filename": "runbook_vpn_issues.md",
        "content": "# Runbook: VPN Connectivity Issues\n\n## Overview\nTroubleshooting Cisco AnyConnect VPN drops.\n\n## Steps\n1. Ask user to check home internet connection.\n2. Verify VPN service status on the internal dashboard.\n3. Check if user is on the latest AnyConnect version (v4.10+).\n4. Instruct user to clear VPN cache and restart client.\n5. If issue persists, check firewall logs for the user's IP.\n6. Escalate to Network Team if multiple users report drops."
    },
    {
        "filename": "faq_email_config.md",
        "content": "# FAQ: Outlook Email Configuration\n\n**Q: How do I configure Outlook on my mobile device?**\nA: Download Outlook from the App Store. Enter your company email. You will be redirected to the SSO page. Authenticate with MFA.\n\n**Q: Why are my emails stuck in the Outbox?**\nA: This usually happens when the mailbox quota is exceeded or the network is disconnected. Check mailbox size under File -> Info."
    },
    {
        "filename": "ticket_INC001_sap_gui.md",
        "content": "# Ticket: INC001 - SAP GUI Crashing\n\n**Category:** Application Error\n**Description:** SAP GUI crashes immediately upon opening.\n**Root Cause:** Corrupted SAP GUI cache files.\n**Resolution:** \n1. Navigated to `%appdata%\\SAP\\Common`.\n2. Deleted the cache folders.\n3. Restarted SAP GUI.\n4. Issue resolved."
    },
    {
        "filename": "ticket_INC002_printer.md",
        "content": "# Ticket: INC002 - Cannot map network printer\n\n**Category:** Hardware/Peripherals\n**Description:** User unable to map the 3rd floor marketing printer.\n**Root Cause:** Spooler service was hung on user's machine.\n**Resolution:** \n1. Opened Services.msc.\n2. Restarted Print Spooler service.\n3. Re-mapped printer using `\\\\printserver01\\MKT-3FL-PTR`.\n4. Printed test page successfully."
    },
    {
        "filename": "sop_software_install.md",
        "content": "# SOP: Approved Software Installation\n\n## Overview\nProcedure for installing standard software.\n\n## Steps\n1. Verify software is in the Approved Software List (ASL).\n2. If not, direct user to submit a Software Exception Request.\n3. If approved, use SCCM or Intune Company Portal to push the installation.\n4. If manual install is required, use CyberArk EPM or LAPS for temporary admin rights.\n5. Do NOT give users permanent local admin rights."
    },
    {
        "filename": "runbook_bsod.md",
        "content": "# Runbook: Blue Screen of Death (BSOD)\n\n## Overview\nInitial troubleshooting for BSOD on company laptops.\n\n## Steps\n1. Ask user for the stop code (e.g., PAGE_FAULT_IN_NONPAGED_AREA).\n2. Request user to reboot in Safe Mode.\n3. Check for recent Windows Updates or Driver installations.\n4. Run `sfc /scannow` and `dism /online /cleanup-image /restorehealth`.\n5. If hardware failure is suspected, contact vendor (Dell/HP) for replacement."
    },
    {
        "filename": "faq_hardware.md",
        "content": "# FAQ: Hardware Requests\n\n**Q: How do I request a new monitor?**\nA: Open a ticket in the IT portal. Manager approval is required for a second monitor.\n\n**Q: What do I do if I spilled liquid on my laptop?**\nA: Immediately power off the laptop. Do not try to turn it on. Bring it to the IT Helpdesk for assessment."
    },
    {
        "filename": "ticket_INC003_sharepoint.md",
        "content": "# Ticket: INC003 - SharePoint Access Denied\n\n**Category:** Access Rights\n**Description:** User gets access denied on the Finance SharePoint site.\n**Root Cause:** User was removed from the Finance AD group during an automated sync.\n**Resolution:** \n1. Verified user's department with HR.\n2. Re-added user to the `SEC-Finance-Users` AD group.\n3. Instructed user to wait 15 minutes for sync and try again."
    },
    {
        "filename": "ticket_INC004_teams.md",
        "content": "# Ticket: INC004 - Teams Audio Not Working\n\n**Category:** Application Error\n**Description:** Microphone not working in Teams meetings.\n**Root Cause:** Teams was using the incorrect audio input device.\n**Resolution:** \n1. Opened Teams Settings -> Devices.\n2. Changed microphone from 'System Default' to 'Plantronics Headset'.\n3. Made a test call to verify."
    },
    {
        "filename": "runbook_onboarding.md",
        "content": "# Runbook: IT Onboarding\n\n## Overview\nIT tasks for new hires.\n\n## Steps\n1. Ensure AD account is created by the automated HR system.\n2. Assign O365 E3 License.\n3. Add to department-specific distribution lists.\n4. Image laptop with standard Windows 11 Enterprise build.\n5. Send welcome email to manager with login credentials."
    },
    {
        "filename": "sop_guest_wifi.md",
        "content": "# SOP: Guest Wi-Fi Access\n\n## Overview\nGranting temporary Wi-Fi to visitors.\n\n## Steps\n1. Connect to 'Company-Guest' SSID.\n2. A captive portal will open.\n3. Sponsor (employee) must approve the request via email.\n4. Access is granted for 24 hours.\n5. Max bandwidth per guest is limited to 10Mbps."
    },
    {
        "filename": "ticket_INC005_locked_file.md",
        "content": "# Ticket: INC005 - Excel File Locked\n\n**Category:** File Share\n**Description:** Cannot edit Finance.xlsx, says it is locked by another user.\n**Root Cause:** A user left the file open and their session disconnected.\n**Resolution:** \n1. Connected to File Server `FS01`.\n2. Opened Computer Management -> Shared Folders -> Open Files.\n3. Closed the open session for Finance.xlsx.\n4. User can now edit."
    },
    {
        "filename": "faq_mfa.md",
        "content": "# FAQ: Multi-Factor Authentication (MFA)\n\n**Q: I lost my phone, how do I log in?**\nA: Call the Helpdesk. After verbal verification, we can issue a Temporary Access Pass (TAP) valid for 8 hours.\n\n**Q: Can I use SMS for MFA?**\nA: No. SMS MFA is disabled globally due to security policies. Use the Microsoft Authenticator app."
    },
    {
        "filename": "ticket_INC006_slow_pc.md",
        "content": "# Ticket: INC006 - Laptop is very slow\n\n**Category:** Hardware/Performance\n**Description:** User reports laptop takes 10 minutes to boot.\n**Root Cause:** Antivirus full scan was running during startup.\n**Resolution:** \n1. Checked Task Manager, saw high CPU from AV service.\n2. Adjusted AV policy to run full scans on weekends only.\n3. Rebooted machine, performance normalized."
    }
]

def main():
    os.makedirs(DOCS_DIR, exist_ok=True)
    for doc in DOCUMENTS:
        path = os.path.join(DOCS_DIR, doc["filename"])
        with open(path, "w", encoding="utf-8") as f:
            f.write(doc["content"])
    print(f"Generated {len(DOCUMENTS)} knowledge base documents in {DOCS_DIR}")

if __name__ == "__main__":
    main()
