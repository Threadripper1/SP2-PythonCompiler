import sys

def run_program():
    i = "\ninclude D:\masm32\include\windows.inc\ninclude D:\masm32\include\kernel32.inc\ninclude D:\masm32\include\masm32.inc\n\n" \
    "includelib D:\masm32\lib\kernel32.lib\nincludelib D:\masm32\lib\masm32.lib\n\n"
    k = ".386\n.model flat, stdcall\noption casemap:none\n"+ i +".data\n\n.code\nstart:\n\tmain proc"
    s = k + "main endp"+"\nend start"
    if not s:
        print("Error. The file was saved unsuccessfully")
    else:
        a = open("RGR-12-Python-IO-83-Kolomiets.asm", "w")
        a.write(s)
        a.close()
        print("The file was saved successfully!" + "\nSaved in: RGR-12-Python-IO-83-Kolomiets.asm")
        print(input())
run_program()
