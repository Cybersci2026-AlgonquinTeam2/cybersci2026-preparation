"""mangui guides, batch 16: impacket (kept in its own file; written last).
Examples teach (command + explanation); nothing is captured. Written by scripts/mangui_write.py.
Option lists were written from knowledge, not checked against Kali's pages.
Use these tools only on systems you own or are explicitly authorised to test (a lab, a CTF, a signed engagement)."""

GUIDES = []

GUIDES.append(dict(
    name="impacket", section="1", one_line="Python tools that speak Windows network protocols (SMB, Kerberos, RPC, LDAP)",
    plain=["`impacket` is a collection of Python scripts for working with Windows and Active Directory protocols from Linux. On Kali they are installed as `impacket-NAME`, for example `impacket-smbclient` or `impacket-lookupsid`.",
           "Most scripts take the target as `DOMAIN/USER:PASSWORD@HOST`. Instead of a password you can give an NT hash with `-hashes :NTHASH`, or a Kerberos ticket with `-k`. Pass `-h` to any script for its own options.",
           "It is a defender's reference as much as an attacker's: seeing how each tool works shows what to detect. Run it only against machines you own or are allowed to test, such as a CTF or a home lab."],
    when=["Enumerate a Windows host or domain from Linux in a lab.", "Understand how a Windows protocol behaves by looking at the traffic it makes.", "Use a credential you were given in a CTF against another service.", "Practise Active Directory attack paths in your own lab, then write the detection."],
    examples=[("Browse a share", "impacket-smbclient CORP/alice:'Passw0rd'@10.10.10.5", "Opens an FTP-like prompt for SMB shares. Type `shares`, `use SHARE`, `ls`, `get FILE`."),
              ("Look up accounts by SID", "impacket-lookupsid CORP/alice:'Passw0rd'@10.10.10.5", "Counts up the numeric ids (RIDs) after the domain SID and prints the account names: a way to list users and groups."),
              ("Which services use which ports", "impacket-rpcdump 10.10.10.5", "Lists the RPC endpoints a host exposes, to see what is running."),
              ("Check a Kerberos setting", "impacket-GetNPUsers CORP/ -dc-ip 10.10.10.2 -usersfile users.txt -no-pass -format hashcat", "Asks the domain controller about accounts that do not require Kerberos pre-authentication (a misconfiguration). A lab exercise: the fix is to enable pre-auth, and the detection is repeated AS-REQ without pre-auth."),
              ("Accounts with service names", "impacket-GetUserSPNs CORP/alice:'Passw0rd' -dc-ip 10.10.10.2", "Lists accounts that have service principal names. Adding -request fetches service tickets that can be tested for weak passwords offline: practise only in your lab, and read about the defence (long random service-account passwords, gMSA)."),
              ("Run a command with credentials you hold", "impacket-wmiexec CORP/alice:'Passw0rd'@10.10.10.5 whoami", "Runs one command through WMI and prints the result. The same technique exists as impacket-psexec and impacket-smbexec; they differ in how noisy they are, which is what defenders look for."),
              ("Use a hash instead of a password", "impacket-wmiexec -hashes :31d6cfe0d16ae931b73c59d7e0c089c0 CORP/alice@10.10.10.5", "Windows accepts the NT hash in place of the password for these protocols. This is why hash theft matters and why defenders limit where privileged accounts log in."),
              ("A fake file share for a test", "impacket-smbserver share ./loot -smb2support", "Starts an SMB server that shares ./loot. In a lab it is a quick way to move a file between two machines."),
              ("Use a Kerberos ticket", "export KRB5CCNAME=alice.ccache\nimpacket-smbclient -k -no-pass CORP/alice@dc01.corp.local", "-k uses the ticket named in KRB5CCNAME. Kerberos needs working DNS names and a clock within five minutes of the domain.")],
    options=[
        ("TARGET", "DOMAIN/USER[:PASSWORD]@HOST (the form most scripts expect).", "Always."),
        ("-hashes LMHASH:NTHASH", "Authenticate with a hash (leave the LM part empty: :NTHASH).", "When you hold a hash, not a password."),
        ("-no-pass", "Do not ask for a password.", "With -k or a null session."),
        ("-k", "Use Kerberos authentication (reads KRB5CCNAME).", "Kerberos-only domains."),
        ("-aesKey KEY", "Kerberos AES key.", "Keys instead of passwords."),
        ("-dc-ip IP", "Address of the domain controller.", "When names do not resolve."),
        ("-target-ip IP", "Address of the target when the name does not resolve.", "Labs without DNS."),
        ("-port N", "Port to connect to.", "Non-standard services."),
        ("-debug / -ts", "Show debug output / timestamps.", "Troubleshooting."),
        ("-h", "Help for the script (always run it first).", "Every script has its own options."),
        ("impacket-smbclient", "Share browser.", "Moving files from a share."),
        ("impacket-lookupsid", "Enumerate accounts by SID.", "Listing users and groups."),
        ("impacket-rpcdump / impacket-samrdump", "List RPC endpoints / SAM information.", "Host enumeration."),
        ("impacket-GetNPUsers / impacket-GetUserSPNs", "Find accounts with Kerberos misconfigurations.", "AD practice and detection work."),
        ("impacket-wmiexec / -psexec / -smbexec / -atexec / -dcomexec", "Run commands remotely by different methods.", "Lab practice and comparing detections."),
        ("impacket-secretsdump", "Read stored credentials from a host you administer or a copy of its data.", "Lab work and recovery of your own systems."),
        ("impacket-smbserver", "A small SMB server.", "Moving files in a lab."),
        ("impacket-mssqlclient", "A SQL Server client.", "Databases in a lab."),
        ("impacket-ntlmrelayx", "Relays NTLM authentication to other services.", "Advanced lab exercises; read the defences first (SMB signing, LDAP signing)."),
        ("impacket-ticketer / impacket-getTGT / impacket-getST", "Request or build Kerberos tickets.", "Understanding Kerberos in a lab.")],
    mistakes=["Forgetting that Kerberos needs the right DNS names and a clock within five minutes.", "Mixing up the script names: on Kali they are `impacket-NAME`; the older `NAME.py` form is the same script.", "Trying a command on a host you are not authorised to test: this tool set is illegal outside a lab or an engagement.", "Passing a password with special characters unquoted: wrap it in single quotes.", "Running many guesses against accounts and locking them out: read the lockout policy first."],
    try_=["In a lab domain, list the users with impacket-lookupsid and compare with BloodHound.", "Read the `-h` output for three scripts and explain what each protocol is.", "Pick one technique and write the detection rule (an event ID or a log line) that would catch it.", "Fix a deliberately weak setting in your lab and rerun the tool to see it stop working."],
    see_also="smbclient(1), rpcclient(1), ldapsearch(1), bloodhound(1), nmap(1) (smb-*, ldap-* scripts), crackmapexec / netexec, evil-winrm, hashcat(1), john(1).", partial=True))
