All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
## Unrealeased
- portscanner module, used to scan ports
- dumpster module, used to dump generic credentials
- local_email_extractor module, used to extract .pst, .ost files
- firecookies, used to extract cookies from Mozilla Firefox
- keylogging module, used to log keystrokes
- scrnshot module, used to get screenshot from victim via email or ftp
- ftp_bruteforce module, used to bruteforce ftp servers
- shellshock module, used to exploit shellshock in vulnerable servers
- username module, used to extract information based on username

## [0.2] - 2020-08-04
### Added
- links_extractor module, used to extract links from a website
- emailrep module, used to extract information by an e-mail address
- cve_2020_5902 module, used to exploit F5 BIG-IP devices
- Almost all modules updated
- Multiples bugs fixed

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

[0.2]: https://github.com/Sam-Marx/AmaterasuV2/compare/v0.1...v0.2
[0.1]: https://github.com/Sam-Marx/AmaterasuV2/releases/tag/v0.1