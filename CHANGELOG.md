All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
## Unrealeased
- portscanner module, used to scan ports
- dumpster module, used to dump generic credentials
- local_email_extractor module, used to extract .pst, .ost files
- firecookies, used to extract cookies from Mozilla Firefox
- keylogging module, used to log keystrokes
- scrnshot module, used to get screenshot from victim via email or ftp
- links_extractor module, used to extract all links from websites


## [0.1] - 2020-07-04
### Added
- Modules.db file, a SQLite3 database to store modules names, their descriptions and their authors
- Sqlconnection.py file, used as a bridge to the modules.db
- Amaterasu.py, the main project file
- This CHANGELOG file to log the changes
- Requirements.txt, used to install required libraries
- README file to introduce the Amaterasu project
- email_extractor module, used to extract e-mails from websites
- atg_worm module, used to exploit atgs
- honeypot_detector, used to detect honeypots using Shodan
