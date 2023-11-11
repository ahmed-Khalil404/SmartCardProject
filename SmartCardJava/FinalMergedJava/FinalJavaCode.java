package SmartCardJava.FinalMergedJava;
import javacard.framework.*;
import javacard.security.*;

public class FinalJavaCode extends Applet {
    
    private byte balance = 50;
    private static final byte PAYMENT_AMOUNT = 10;
    private static final byte CHARGE_AMOUNT = 10;
    private static KeyPair keyPair;
    private static byte[] signature = new byte[64];
    private final static byte[] PIN = { 0x6B, 0x68, 0x61, 0x6C, 0x69, 0x6C };
    private final static byte[] PIN_ANSWER = new byte[6];

    //All the methods *********************************************************************All the methods we used

    private void makePayment() {
        if (balance < PAYMENT_AMOUNT) {
            ISOException.throwIt(ISO7816.SW_CONDITIONS_NOT_SATISFIED);
        }
        balance -= PAYMENT_AMOUNT;
    }
    private void chargeCard() {
        balance += CHARGE_AMOUNT;
    }


    public static void OnPinConnect() {
        if (Util.arrayCompare(PIN, (byte) 0, PIN_ANSWER, (byte) 0, (short) PIN_ANSWER.length) != 0x00) {
            ISOException.throwIt(ISO7816.SW_SECURITY_STATUS_NOT_SATISFIED);
        }
    }

    public static void PINISCONNECTED(APDU apdu, byte[] buf) {
        short bytesRead = apdu.setIncomingAndReceive();
        short answerOffset = (short) 0;

        while (bytesRead > 0) {
            Util.arrayCopy(buf, ISO7816.OFFSET_CDATA, PIN_ANSWER, answerOffset, bytesRead);
            answerOffset += bytesRead;
            bytesRead = apdu.receiveBytes(ISO7816.OFFSET_CDATA);
        }

        OnPinConnect();
    }

    public static void DisconnectConnectedPin() {
        PINReset();
        OnPinConnect();
    }

    public static void ChangeCurrentPin(APDU apdu, byte[] buf) {
        short bytesRead = apdu.setIncomingAndReceive();
        short answerOffset = (short) 0;

        while (bytesRead > 0) {
            Util.arrayCopy(buf, ISO7816.OFFSET_CDATA, PIN, answerOffset, bytesRead);
            answerOffset += bytesRead;
            bytesRead = apdu.receiveBytes(ISO7816.OFFSET_CDATA);
        }

        PINReset();
        ISOException.throwIt((short) 0x6983);
    }

    public static void PINReset() {
        for (short i = 0; i < PIN_ANSWER.length; i++) {
            PIN_ANSWER[i] = 0x00;
        }
    }


    public static void KeyPairGeneration() {
        keyPair = new KeyPair(KeyPair.ALG_RSA, KeyBuilder.LENGTH_RSA_512);
        keyPair.genKeyPair();
    }

    public static void SendThePublicKey(APDU apdu, byte[] buf) {
        RSAPublicKey publicKey = (RSAPublicKey) keyPair.getPublic();

        short offset = ISO7816.OFFSET_CDATA;

        short expLen = publicKey.getExponent(buf, (short) (offset + 2));
        offset = Util.setShort(buf, offset, expLen);
        offset += expLen;

        short modLen = publicKey.getModulus(buf, (short) (offset + 2));
        offset = Util.setShort(buf, (short) offset, modLen);
        offset += modLen;

        apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (short) (offset - ISO7816.OFFSET_CDATA));
    }

    public static void DoSignTheMessage(APDU apdu, byte[] buf) {
        short bytesRead = apdu.setIncomingAndReceive();
        short answerOffset = (short) 0;
        byte[] message = new byte[127];

        while (bytesRead > 0) {
            Util.arrayCopy(buf, ISO7816.OFFSET_CDATA, message, answerOffset, bytesRead);
            answerOffset += bytesRead;
            bytesRead = apdu.receiveBytes(ISO7816.OFFSET_CDATA);
        }

        Signature privSign = Signature.getInstance(Signature.ALG_RSA_SHA_PKCS1, false);
        privSign.init(keyPair.getPrivate(), Signature.MODE_SIGN);
        short len = privSign.sign(message, (short) 0, (short) message.length, signature, (short) 0);

        apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (byte) len);
    }
    public static void SendSignatureTotheCard(APDU apdu, byte[] buf) {
        Util.arrayCopy(signature, (byte) 0, buf, ISO7816.OFFSET_CDATA, (byte) signature.length);
        apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (byte) signature.length);
    }



    public static void install(byte[] buffer, short offset, byte length) {
        new FinalJavaCode().register();
    }

        //End of the methods we used *********************************************************************End of the methods we used


    public void process(APDU apdu) {
        if (selectingApplet()) {
            return;
        }
        byte[] buf = apdu.getBuffer();
        switch (buf[ISO7816.OFFSET_INS]) {
            case (byte) 0x00:
                OnPinConnect();
                buf[0] = balance;
                apdu.setOutgoingAndSend((short) 0, (short) 1);
                break;
            case (byte) 0xC1:
                OnPinConnect();
                makePayment();
                buf[0] = balance;
                apdu.setOutgoingAndSend((short) 0, (short) 1);
                break;

            case (byte) 0xD1:
                OnPinConnect();
                chargeCard();
                buf[0] = balance;
                apdu.setOutgoingAndSend((short) 0, (short) 1);
                break;

            case (byte) 0xA0:
                PINISCONNECTED(apdu, buf);
                break;

            case (byte) 0xA1:
                DisconnectConnectedPin();
                break;

            case (byte) 0xA2:
                OnPinConnect();
                ChangeCurrentPin(apdu, buf);
                break;

            case (byte) 0xB0:
                OnPinConnect();
                KeyPairGeneration();
                break;

            case (byte) 0xB1:
                OnPinConnect();
                SendThePublicKey(apdu, buf);
                break;

            case (byte) 0xB2:
                OnPinConnect();
                DoSignTheMessage(apdu, buf);
                break;

            case (byte) 0xB3:
                OnPinConnect();
                SendSignatureTotheCard(apdu, buf);
                break;

            default:
                ISOException.throwIt(ISO7816.SW_INS_NOT_SUPPORTED);
        }
    }

}
