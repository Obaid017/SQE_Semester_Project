# SQE_Semester_Project
# Advanced Multi-User Banking & Financial Management System (PKR)

## 🚀 Project Overview
This project fulfills the requirements of Lab Assignment 4, demonstrating a complete software quality lifecycle. It consists of a functional Python-based Command Line Interface (CLI) banking application built with intentional logic errors, code smells, and security vulnerabilities. These flaws are explicitly designed to be discovered, documented, and analyzed using manual testing, automated unit testing, SonarQube, and Snyk.

### Core System Features
* **Multi-User Authentication:** Separate login spaces for customers and administrators, complete with user session state handling and account locking rules.
* **PKR Financial Transaction Engine:** Built-in business validations for automated account deposits, cash withdrawals, and Peer-to-Peer (P2P) fund transfers.
* **Fixed Deposit Simulator:** A calculation matrix tool utilizing compounding loops to analyze investment trajectories over custom timelines.
* **Expense Tracker:** A tracking module that categorizes individual user outbound transactions and auto-calculates localized tax adjustments.

---

## 📂 Repository Architecture
The workspace contains the following core files:

* `banking_system.py`: The core application program containing all functional modules, menus, and intentional bugs.
* `test_banking.py`: The automated unit test suite containing 7 test cases designed to catch functional boundaries and logical software flaws.
* `sonar-project.properties`: Configuration mapping profile to route local source files through the SonarQube quality gateway.
* `requirements.txt`: Project dependency manifest file compiled to enable Snyk automated package scanning.

---

## ⚙️ Execution and Testing Instructions

### 1. Running the Banking Application
Launch the standalone terminal interface by running:
```bash
python banking_system.py
