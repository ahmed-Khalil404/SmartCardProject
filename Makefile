all: compile convert delete_applet upload_applet run_terminal

compile:
	@sudo service pcscd start
	@echo "Compiling Java source..."
	@javac -source 1.2 -target 1.1 -g -cp ./jc211_kit/bin/api.jar -d ./src/class ./src/FinalJavaCode.java
	@echo "Compilation complete or with warnings..."

convert:
	@echo "Converting to JavaCard format..."
	@java -classpath ./jc211_kit/bin/converter.jar:. com.sun.javacard.converter.Converter -verbose -exportpath ./jc211_kit/api_export_files:source -classdir ./src/class -applet 0xa0:0x0:0x0:0x0:0x62:0x3:0x1:0xc:0x6:0x1:0x2 FinalJavaCode source 0x0a:0x0:0x0:0x0:0x62:0x3:0x1:0xc:0x6:0x1 1.0

delete_applet:
	@echo "Deleting applet from card..."
	@gpshell ./gpshellscript/deletefromcard

upload_applet:
	@echo "Uploading applet to card..."
	@gpshell ./gpshellscript/uploadtocard

run_terminal:
	@echo "Running Terminal Python script..."
	@python3 ./TerminalPython/terminal.py

.PHONY: compile convert delete_applet upload_applet run_terminal all

