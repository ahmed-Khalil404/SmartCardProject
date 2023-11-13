#!/bin/bash
sudo service pcscd start

javac -source 1.2 -target 1.1 -g -cp jc211_kit/bin/api.jar -d src/class src/FinalJavaCode.java

java -classpath ./jc211_kit/bin/converter.jar:. com.sun.javacard.converter.Converter -verbose -exportpath ./jc211_kit/api_export_files:source -classdir ./src/class -applet 0xa0:0x0:0x0:0x0:0x62:0x3:0x1:0xc:0x6:0x1:0x2 FinalJavaCode source 0x0a:0x0:0x0:0x0:0x62:0x3:0x1:0xc:0x6:0x1 1.0

gpshell ./gpshellscript/deletefromcard
gpshell ./gpshellscript/uploadtocard

python3 TerminalPython/terminal.py
