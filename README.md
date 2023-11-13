# Smart Card Project

## Overview
This project, developed by Ahmed Khalil Ben Sassi, Yassin Anakar, and Jamal El Alouani, focuses on creating a secure communication system between a terminal (CLI) coded in Python and a smart card-Applet application programmed in Java. The primary goal is to enable the generation of an RSA private and public key pair within the smart card, thereby enhancing the security of data transmission.

## Introduction
The project facilitates secure interactions between a CLI terminal and a smart card. Key features include PIN protection, RSA key pair generation, data signing, and public key transmission. These functionalities enhance the security and reliability of data exchanged between the terminal and the smart card.

## Features

### Basic Functionalities
- **PIN Protection:** Integrates a PIN code for user authentication and card protection.
- **Key Pair Generation:** Enables the smart card to generate a secure RSA 512-bit key pair.
- **Data Signing:** Implements the smart card's capability to sign data.
- **Public Key Transmission:** Allows for the transmission of the smart card's public key to the terminal application.

### Payment Functionalities
- **Account Credit:** Check the current credit on the card.
- **History:** Review transaction history.
- **Payment:** Process static payments of 10 euros.
- **Recharge:** Recharge the card with a fixed amount of 10 euros.

### Terminal-Side Interaction
- A user-friendly CLI with robust exception handling.
- Functionalities include user login/logout, PIN changes, key generation, and more.

## Architecture
- Detailed command descriptions and return values for various operations like balance inquiry, payment, charging the card, etc.

## Libraries Used
- Python's `smartcard` library for interfacing with the card reader and managing APDU communications.
- The `rsa` library for cryptographic operations.
- Java's `javacard.framework` and `javacard.security` for smart card applet development.

## Setup and Execution
- Instructions for using shell scripts and Makefiles for compiling and managing the smart card application lifecycle.

## Conclusion
The Smart Card Project successfully demonstrates a secure communication system, fulfilling the specified requirements and providing a secure framework for data transmission between the terminal and the smart card.

---

### Note
This README is a template based on the project report and should be modified to accurately reflect the specific details and functionalities of your project.
