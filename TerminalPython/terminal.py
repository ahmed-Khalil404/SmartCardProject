from APDUKHALIL import KhalilAPDU
import time
import sys

class JavaCardCLI:
    def __init__(self, log=False):
        self.APDU = KhalilAPDU(log)
        self.coreCommands = {
            "login": self.login,
            "changepin": self.changePin,
            "logout": self.logout,
            "genkey": self.generateKey,
            "pubkey": self.showPublicKey,
            "sign": self.signData,
            "verify": self.verifyData,
            "back": self.exitLoop  # Command to exit the loop
        }
        self.PaymentMethods = {
            "history": self.fetch, 
            "pay": self.pay,
            "charge": self.charge,
            "info": self.fetchBalance,
            "back": self.exitLoop  # Command to exit the loop
        }
        self.welcomeMessage()
        self.ChoosepaymentFonc()
        self.currentCommandGroup = None

    def welcomeMessage(self, speed=0.03):
        self.animateText("Welcome to the Java Card project developed by Khalil, Yassin, and Jamal!", speed=0.06)
        self.animateText("📚 Type 'exit' at any time to say goodbye! 📚", speed)

    def ChoosepaymentFonc(self):
        while True:
            self.animateText("\n1: Core Functionalities\n2: Payment features\nEnter option (1 or 2): ", speed=0.05)
            choice = input()
            if choice == '1':
                self.animateText("Core Functionalities selected. Type 'help' for commands or 'back' to switch.", speed=0.05)
                self.myMainLoop(self.coreCommands)
            elif choice == '2':
                self.animateText("Payment Features selected. Type 'help' for commands or 'back' to switch.", speed=0.05)
                self.myMainLoop(self.PaymentMethods)
            elif choice.lower() == 'exit':
                self.animateText("Goodbye! 👋")
                break
            else:
                self.animateText("Invalid choice, please enter 1 or 2.")


    def myMainLoop(self, command_group):
        self.currentCommandGroup = command_group  # Set the current command group
        self.exit_loop = False  # Flag to control the loop
        self.help()  # Show help message at the beginning
        try:
            while not self.exit_loop:
                userinput = self.myInput()
                if userinput:
                    command = userinput[0].lower()
                    if command == 'exit':
                        return
                    elif command in command_group:
                        command_group[command](userinput)
                    elif command == 'help':
                        self.help()
                    elif command == 'back':
                        return  
                    else:
                        self.animateText("\nUnknown command. Try again.")
        except KeyboardInterrupt:
            self.animateText("\n\nExiting... Goodbye! 👋")
            time.sleep(1)

    def fetch(self, userinput):
        self.APDU.fetchTransactionHistory()

    def exitLoop(self, userinput):
        self.exit_loop = True  # Set the flag to exit the loop

    def login(self, userinput):
        self.validate(userinput, self.APDU.startPINSession, "Enter PIN: ")

    def changePin(self, userinput):
        self.validate(userinput, self.APDU.modifyPIN)

    def logout(self, userinput):
        self.APDU.terminatePINSession()

    def generateKey(self, userinput):
        self.APDU.generateRSAKeyPair()

    def signData(self, userinput):
        self.validate(userinput, self.APDU.signMessageWithRSA)

    def verifyData(self, userinput):
        self.validate(userinput, self.APDU.validateRSASignature)

    def pay(self, userinput):
        self.APDU.makePayment()

    def charge(self, userinput):
        self.APDU.chargeCard()

    def fetchBalance(self, userinput):
        self.APDU.fetchBalance()

    def showPublicKey(self, userinput):
        self.APDU.retrieveRSAPublicKey()
    
    def help(self):
        self.animateText("🌟 Command List: 🌟", speed=0.07)
        if self.currentCommandGroup:
            for command in self.currentCommandGroup:
                self.animateText(f"- {command}", speed=0.03)
        else:
            self.animateText("No command group selected. Please choose a functionality group first.", speed=0.05)

    def coreFunctionalityCommands(self, userinput):
        command = userinput[0].lower()
        if command == "login":
            self.validate(userinput, self.APDU.startPINSession, "Enter PIN: ")
        elif command == "changepin":
            self.validate(userinput, self.APDU.modifyPIN)
        elif command == "logout":
            self.APDU.terminatePINSession()
        elif command == "genkey":
            self.APDU.generateRSAKeyPair()
        elif command == "sign":
            self.validate(userinput, self.APDU.signMessageWithRSA)
        elif command == "verify":
            self.validate(userinput, self.APDU.validateRSASignature)

    def Paymentfeatures(self, userinput):
        command = userinput[0].lower()
        if command == "check":
            self.APDU.fetchTransactionHistory()
        elif command == "pay":
            self.APDU.makePayment()
        elif command == "charge":
            self.APDU.chargeCard()
        elif command == "info":
            self.APDU.fetchBalance()
        

    def myInput(self, prompt="\nCommand > "):
        return input(prompt).split()

    def validate(self, userinput, callback, input_msg=""):
        if len(userinput) != 2:
            user_input = self.myInput(input_msg)[0]
            callback(user_input)
        else:
            callback(userinput[1])

    def animateText(self, text, speed=0.05):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        print()

    # Add definitions for other methods like help, info, etc.

if __name__ == '__main__':
    apdu_interface = KhalilAPDU(log=False)
    if apdu_interface.initialized:
        JavaCardCLI()
    else:
        print("Once you connect your card, restart the program.")
