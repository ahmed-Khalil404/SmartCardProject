from APDUKHALIL import KhalilAPDU
import time
import sys


class JavaCardCLI:
    def __init__(self, log=False):
        self.APDU = KhalilAPDU(log)
        self.welcomeMessage()
        self.myMainLoop()

    def welcomeMessage(self,speed=0.03):
        self.animateText("Welcome to the Java Card project developed by Khalil, Yassin, and Jamal!", speed=0.06)
        self.animateText("There's so much to do from :", speed)        
        self.animateText("Check money on your account 💸", speed)
        self.animateText("🔐 Securely manage your smart card operations! 🔐", speed)
        self.animateText("📚 Type 'help' for a list of commands or 'exit' to say goodbye! 📚", speed)
        self.animateText("💻 Ready to start? Enter your command below! 💻", speed=0.06)



    def myInput(self, prompt="\nCommand > "):
        return (input(prompt).split())

    def myMainLoop(self):
        try:
            while True:
                userinput = self.myInput()
                if userinput == []:
                    pass
                elif userinput[0] == "ConnectWithPin":
                    self.validate(userinput, self.APDU.startPINSession, "Enter PIN: ")
                elif userinput[0] == "changepin":
                    self.validate(userinput, self.APDU.modifyPIN)
                elif userinput[0] == "ChargeCard":
                    self.APDU.chargeCard()
                elif userinput[0] == "Pay":
                    self.APDU.makePayment()
                elif userinput[0] == "Generatekey":
                    self.APDU.generateRSAKeyPair()
                elif userinput[0] == "ShowPublicKey":
                    self.APDU.retrieveRSAPublicKey()
                elif userinput[0] == "SignData":
                    self.validate(userinput, self.APDU.SignDataMessageWithRSA)
                elif userinput[0] == "VerifyData":
                    self.validate(userinput, self.APDU.validateRSASignDataature)
                elif userinput[0] == "info":
                    self.APDU.fetchBalance()
                elif userinput[0] == "help":
                    self.help()
                elif userinput[0] == "logout":
                    self.APDU.terminatePINSession()
                elif userinput[0] == "exit":
                    self.animateText("Goodbye! 👋")
                    time.sleep(1)
                    return
                else:
                    self.animateText("\nUnknown command. Try again.")
        except KeyboardInterrupt:
            self.animateText("\n\nExiting... Goodbye! 👋")   
            time.sleep(1)
            return

    def validate(self, userinput, callback, input_msg=""):
        if len(userinput) != 2:
            user_input = self.myInput(input_msg)[0]
            callback(user_input)
        else:
            callback(userinput[1])

    def animateText(self, text,speed=0.05):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        print()

    def info(self):
        self.APDU.getInfos()

    def help(self):
        self.animateText("🌟 Command List: 🌟", speed=0.07)
        self.animateText("- ConnectWithPin \"PIN\": 🔒 Connect with a PIN to the card", speed=0.03)
        self.animateText("- logout: 🚪 Disconnect the card", speed=0.03)
        self.animateText("- info: ℹ️ Get card balance", speed=0.03)
        self.animateText("- changepin \"new PIN\": 🔑 Change the PIN", speed=0.03)
        self.animateText("- ChargeCard: 💳 Add 10 units to your card balance", speed=0.03)
        self.animateText("- Pay: 💸 Make a payment of 10 units from your card", speed=0.03)
        self.animateText("- Generatekey: 🗝️ Generate an RSA key pair", speed=0.03)
        self.animateText("- ShowPublicKey: 🔐 Get the public key from the card", speed=0.03)
        self.animateText("- SignData \"message\": ✍️ Sign a message with RSA", speed=0.03)
        self.animateText("- VerifyData \"message\": ✔️ Verify a message with the RSA signature", speed=0.03)


if __name__ == '__main__':
    apdu_interface = KhalilAPDU(log=False)
    if apdu_interface.initialized:
        JavaCardCLI()
    else:
        print("Once you connect your card restart the program.")

