import rsa
from smartcard import *
from smartcard.util import toHexString
from smartcard.System import readers

class CardAPDU:
    def __init__(self):
        self.initialized = False
        card_reader = readers()
        if not card_reader:
            print("Card reader not found.")
            return

        self.card_connection = card_reader[0].createConnection()
        try:
            self.card_connection.connect()
            self.initialized = True
        except Exception as err:
            print("Connection error: ", err)

    def transmitAPDU(self, command, enable_log=False):
        command_hex = toHexString(command).replace(" ", "")
        log_message = f"APDU command: {command_hex}"
        line = "-" * min(len(log_message), 100)

        response_data, status_word1, status_word2 = self.card_connection.transmit(command)

        if enable_log:
            print(f"{line}\n{log_message}\nResponse: {status_word1} {status_word2}\nData: {response_data}\n{line}")
        return (response_data, status_word1, status_word2)

    def activateAID(self, aid=[0xA0, 0x00, 0x00, 0x00, 0x62, 0x03, 0x01, 0x0C, 0x06, 0x01, 0x02]):
        command = [0x00, 0xA4, 0x04, 0x00] + [len(aid)] + aid
        _, word1, word2 = self.transmitAPDU(command)
        if self.verifyResponse(word1, word2) != 0:
            print("AID activation failed")

    def verifyResponse(self, word1, word2):
        # Interpretation of response status words
        if word1 == 0x90 and word2 == 0x00: 
            return 0
        if word1 == 0x61: 
            return word2
        if word1 == 0x69 and word2 == 0x82: 
            return -1
        if word1 == 0x69 and word2 == 0x83:  
            return -2
        if word1 == 0x6f and word2 == 0x00:  
            return -3

    def pushData(self, instruction, payload, log_enabled=False):
        # Send data to the card
        hex_payload = [ord(char) for char in payload]
        apdu_command = [0x80, instruction, 0x00, 0x00] + [len(hex_payload)] + hex_payload
        return self.transmitAPDU(apdu_command, log_enabled)

    def pushEmptyCommand(self, instruction, log_enabled=False):
        # Send a command without data
        return self.pushData(instruction, "", log_enabled)

    def pullData(self, instruction, length, log_enabled=False):
        # Receive data from the card
        apdu_command = [0x80, instruction, 0x00, 0x00, length]
        return self.transmitAPDU(apdu_command, log_enabled)

    def convertDataToString(self, data):
        return "".join([chr(byte) for byte in data])

class KhalilAPDU(CardAPDU):
    def __init__(self, log=False):
        super().__init__()
        self.logging_enabled = log
        if not self.initialized:
            return

        self.log = log
        self.activateAID()
        self.terminatePINSession()

    def makePayment(self):
        response, resp_word1, resp_word2 = self.pullData(0xC1, 1, self.logging_enabled)  # Ensure length is correct
        if self.verifyResponse(resp_word1, resp_word2) == 0:
            print("Payment of 10 euros successful")
            self.fetchBalance()
        else:
            print("Payment failed")

            

    def chargeCard(self):
        response, resp_word1, resp_word2 = self.pullData(0xD1, self.logging_enabled)
        if self.verifyResponse(resp_word1, resp_word2) == 0:
            print("Charging failed")
        else:
            print("Card successfully charged with 10 euros")
            self.fetchBalance()

    def fetchTransactionHistory(self):
         response, sw1, sw2 = self.pullData(0x01, 1, self.logging_enabled)  
         if self.verifyResponse(sw1, sw2) == 0:
            paymentCount = response[0]  # Get the count of payment transactions
            print("Total Payment Transactions: %d" % paymentCount)
         else:
            print("Failed to fetch transaction history. Please enter your PIN first!")

    def fetchBalance(self):
        response, sw1, sw2 = self.pullData(0x00, 1, self.logging_enabled)
        if self.verifyResponse(sw1, sw2) == 0:
            print("Balance: %d" % response[0])
        else:
            print("Please enter your PIN first !")

    

    def startPINSession(self, pin_code):
        _, resp_word1, resp_word2 = self.pushData(0xC2, pin_code, self.logging_enabled)
        if self.verifyResponse(resp_word1, resp_word2) == 0:
            print("PIN session started successfully")
        elif self.verifyResponse(resp_word1, resp_word2) == -1:
            print("Incorrect PIN")
        else:
            print("PIN must be 6 characters")

    def terminatePINSession(self):
        _, resp_word1, resp_word2 = self.pushEmptyCommand(0xC3, self.logging_enabled)
        if self.verifyResponse(resp_word1, resp_word2) != -1:
            print("Error terminating PIN session")

    def modifyPIN(self, new_pin):
        if len(new_pin) != 6:
            print("PIN must be 6 characters")
        else:
            _, resp_word1, resp_word2 = self.pushData(0xC4, new_pin, self.logging_enabled)
            if self.verifyResponse(resp_word1, resp_word2) == -1:
                print("PIN session not active")
            elif self.verifyResponse(resp_word1, resp_word2) == -2:
                print("PIN changed and session terminated")
            else:
                print("Error changing PIN")

    def generateRSAKeyPair(self):
        _, resp_word1, resp_word2 = self.pushEmptyCommand(0xD3, self.logging_enabled)
        if self.verifyResponse(resp_word1, resp_word2) == 0:
            print("RSA KeyPair generation successful")
        elif self.verifyResponse(resp_word1, resp_word2) == -1:
            print("PIN session not active")
        else:
            print("Error during RSA KeyPair generation")

    def retrieveRSAPublicKey(self):
        key_data, resp_word1, resp_word2 = self.pullData(0xD4, 0x47, self.logging_enabled)
        if self.verifyResponse(resp_word1, resp_word2) == 0:
            exp_len = int.from_bytes(key_data[:2], "big")
            offset = 2
            exponent = int.from_bytes(key_data[offset:offset + exp_len], "big")
            offset += exp_len
            mod_len = int.from_bytes(key_data[offset:offset + 2], "big")
            offset += 2
            modulus = int.from_bytes(key_data[offset:offset + mod_len], "big")

            self.rsa_public_key = rsa.PublicKey(modulus, exponent)

            print("%s" % (self.rsa_public_key.save_pkcs1().decode("utf-8")))
        elif self.verifyResponse(resp_word1, resp_word2) == -1:
            print("PIN session not active")
        else:
            print("Error retrieving RSA Public Key")

    def signMessageWithRSA(self, message):
        _, resp_word1, resp_word2 = self.pushData(0xD5, message, self.logging_enabled)
        if self.verifyResponse(resp_word1, resp_word2) == -1:
            print("PIN session not active")
        elif self.verifyResponse(resp_word1, resp_word2) == -3:
            print("Message must be under 127 characters")
        else:
            signature_data, resp_word1_2, resp_word2_2 = self.pullData(0xD6, resp_word2, self.logging_enabled)
            if self.verifyResponse(resp_word1_2, resp_word2_2) != 0:
                print("Error receiving RSA Signature")
                return
            self.rsa_signature = signature_data
            print("Signature received: \n%s" % (self.convertDataToString(self.rsa_signature)))

    def validateRSASignature(self, message):
        try:
            rsa.verify(bytes(message, "utf-8").ljust(127, b'\x00'), self.rsa_signature, self.rsa_public_key)
            print("Signature is valid")
        except:
            print("Signature is invalid.")
