from subprocess import call
call(["adb", "shell", "screencap", "-p", ">", "screen.png"])