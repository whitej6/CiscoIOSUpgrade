import netmiko
from datetime import datetime
from getpass import getpass
from pprint import pprint
import time

def define_password():
    password = None
    while not password:
        password = getpass('Enter TACACS+ Password: ')
        passwordverify = getpass('Re-enter TACACS+ Password to Verify: ')
        if not password == passwordverify:
            print('Passwords Did Not Match Please Try Again')
            password = None
    return password

def reformat_devices(devices):
    devices = devices.read()
    devices = devices.strip().splitlines()
    return devices

def reformat_code(code):
    code = code.read()
    code = code.strip().splitlines()
    codedict = {}
    for line in code:
        words = line.split()
        codedict.update({words[0]:words[1]})
    code = codedict
    return code

def reformat_md5(md5):
    md5 = md5.read()
    md5 = md5.strip().splitlines()
    md5dict = {}
    for line in md5:
        words = line.split()
        md5dict.update({words[0]:words[1]})
    md5 = md5dict
    return md5

def reformat_boot_loc(bootloc):
    bootloc = bootloc.read()
    bootloc = bootloc.strip().splitlines()
    bootdict = {}
    for line in bootloc:
        words = line.split()
        if len(words) == 3:
            directory = words[1]+' '+ words[2]
        else:
            directory = words[1]
        bootdict.update({words[0]:directory})
    bootloc = bootdict
    return bootloc

def get_upgrade_code(output):
    if 'Ambiguous' in output:
        output = connection.send_command('sh bootvar | in BOOT ')
    output = output.split()
    if len(output) == 3:
        upgradecode = output[2]
    else:
        upgradecode = output[3]
    upgradecode = upgradecode.split(':',1)[1]
    return upgradecode

def uploading_update(models,loc):
    devicemodel.update({device:models})
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'- Device identified as',models)
    logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Device identified as '+models+'\n')
    if models in code:
        output = connection.send_command('sh boot | in BOOT ')
        upgradecode = get_upgrade_code(output)
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Device running - '+upgradecode)
        logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Device running - '+upgradecode+'\n')
        if upgradecode == code[models]:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'- Device already running correct code:')
            logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Device already running correct code:'+'\n')
            output = 'Upgraded Previously'
            connection.disconnect()
        else:
            connection.send_command_timing('copy tftp: '+loc+'\n', max_loops=1)
            connection.send_command_timing(tftp, max_loops=1)
            connection.send_command_timing(code[models], max_loops=1)
            connection.send_command_timing('\n', max_loops=1)
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'- Starting TFTP upload:')
            logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Starting TFTP upload:'+'\n')
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'- 180 Second delay to allow file to upload:')
            logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - 180 Second delay to allow file to upload:'+'\n')
            time.sleep(180)
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'- 180 Second delay complete:')
            logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - 180 Second delay complete:'+'\n')
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'- Starting checksum:')
            logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Starting checksum:'+'\n')
            if not code[models] in md5:
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - MD5 hash not declared in md5hash.txt file:')
                logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - MD5 hash not declared in md5hash.txt file:'+'\n')
                output = 'NoMD5'
            else:
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Expected MD5 Hash: '+md5[code[models]])
                logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Expected MD5 Hash: '+md5[code[models]]+'\n')
                md5str = None
                md5str = ('verify /md5 flash:' + code[models]+' '+md5[code[models]])
                output = None
                connection.send_command_timing('\n')
                connection.send_command_timing('\n')
                output = connection.send_command(md5str)
    else:
        output = 'null'
        logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Model Not Specified For Upgrade:'+'\n')
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'- Model Not Specified For Upgrade:')
    return output            

def apply_boot_change(models,loc):
    device_ver.append(device)
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'- Passed Checksum:')
    logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Passed Checksum:'+'\n')
    if apply == 'y' or apply =='yes':
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'- Applying boot file change:')
        logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Applying boot file change:'+'\n')
        connection.send_command_timing('config t', max_loops=1)
        boot = ('boot system '+loc+code[models])
        connection.send_command_timing(boot, max_loops=1)
        connection.send_command_timing('end', max_loops=1)
        connection.send_command('write memory')
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'- Issueing reload command:')
        logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Issueing reload command:'+'\n')
        connection.send_command_timing('reload\n\n\n\n\n')
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'- Device rebooting:')
        logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Device rebooting:'+'\n')
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'- Timed-out reading channel is expected for next prompt:')
        logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Timed-out reading channel is expected for next prompt:'+'\n')
        connection.disconnect()
    else:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'- Please change boot system to apply update:')
        logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Please change boot system to apply update:'+'\n')
        connection.disconnect()
    output = None
    return output

print('~'*79)
print('~'*27+' Cisco IOS Upgrade Script '+'~'*26)
print('~'*79)
''' Get Variables '''
username = input('Enter TACACS+ Username: ')
password = define_password()
tftp = input('Enter TFTP Server IP: ')
apply = input('Would you like to apply the upgrade after passing checksum? (y/n):')
devices = open('.\devices\devices.txt','r')
devices = reformat_devices(devices)
code = open('.\code versions\codeversions.txt','r')
code = reformat_code(code)
bootloc = open('.\code versions\\bootloc.txt','r')
bootloc = reformat_boot_loc(bootloc)
md5 = open('.\code versions\\md5hash.txt','r')
md5 = reformat_md5(md5)
devicemodel = {}
device_type = 'cisco_ios'
logfilename = datetime.now().strftime('%m%d%Y-%H.%M.%S-')+username+'.log'
logfileloc = '.\\log\\'+logfilename
logfile = open(logfileloc,'w')
device_ver = []
print('~'*79)
logfile.write('~'*79+'\n')
print('~'*25+' Starting Cisco IOS Upgrades '+'~'*25)
logfile.write('~'*25+' Starting Cisco IOS Upgrades '+'~'*25+'\n')
print('~'*29+datetime.now().strftime(' %Y-%m-%d %H:%M:%S ')+'~'*29)
logfile.write('~'*29+datetime.now().strftime(' %Y-%m-%d %H:%M:%S ')+'~'*29+'\n')
print('~'*79)
logfile.write('~'*79+'\n')
''' Common exceptions that could cause issues '''
exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
              netmiko.ssh_exception.NetMikoAuthenticationException)

''' Loop for initial upload '''
for device in devices:
    try:
        ''' Connection Break '''
        print('*'*79)
        logfile.write('*'*79+'\n')
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'- Connecting to',device)
        logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Connecting to '+device+'\n')
        connection = netmiko.ConnectHandler(ip=device, device_type=device_type, username=username, password=password)
        output = connection.send_command('sh version')
        for models,loc in bootloc.items():
            if models in output:
                output = uploading_update(models,loc)
                if 'Verified' in output:
                    output = apply_boot_change(models,loc)
                elif 'Upgraded Previously' in output:
                    pass
                elif 'null' in output:
                    pass
                elif 'NoMD5' in output:
                    pass
                else:
                    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'- Failed Checksum')
                    logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Failed Checksum'+'\n')
                    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Please delete uploaded file and re-run application:')
                    logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Please delete uploaded file and re-run application:'+'\n')
                    print(output)
                    logfile.write(output+'\n')
                    connection.disconnect()
                    device_ver.append(device)

    except exceptions as exception_type:
        exception_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - '+str(exception_type)
        print(exception_str[:79])
        logfile.write(exception_str+'\n')

print('*'*79)
logfile.write('*'*79+'\n')
print('~'*79)
logfile.write('~'*79+'\n')
print('~'*17+' Starting verification of software upgrades '+'~'*18)
logfile.write('~'*17+' Starting verification of software upgrades '+'~'*18+'\n')
print('~'*29+datetime.now().strftime(' %Y-%m-%d %H:%M:%S ')+'~'*29)
logfile.write('~'*29+datetime.now().strftime(' %Y-%m-%d %H:%M:%S ')+'~'*29+'\n')
print('~'*79)
logfile.write('~'*79+'\n')
time.sleep(180)
for device_verify in device_ver:
    try:
        print('*'*79)
        logfile.write('*'*79+'\n')
        connection = netmiko.ConnectHandler(ip=device_verify, device_type=device_type, username=username, password=password)
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'- Connecting to',device_verify)
        logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Connecting to '+device_verify+'\n')
        output = connection.send_command('sh boot | in BOOT ')
        upgradecode = get_upgrade_code(output)
        if devicemodel[device_verify] in code:
            if upgradecode == code[devicemodel[device_verify]]:
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ ' - Sucessfully upgraded '+device_verify)
                logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ ' - Sucessfully upgraded '+ device_verify+'\n')
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Running code - '+upgradecode)
                logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Running code - '+upgradecode+'\n')
                connection.disconnect()
            else:
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ ' - Upgraded unable to be completed on '+ device_verify)
                logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ ' - Upgraded unable to be completed on '+ device_verify+'\n')
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Running code - '+upgradecode)
                logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Running code - '+upgradecode+'\n')
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ ' - Review log before rerunning application:')
                logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ ' - Review log before rerunning application:'+'\n')
                connection.disconnect()
        else:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ ' - '+device_verify+' was not specified for upgrade:')
            logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ ' - ' +device_verify+' was not specified for upgrade:'+'\n')
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Running code - '+upgradecode)
            logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Running code - '+upgradecode+'\n')
            connection.disconnect()
    except exceptions as exception_type:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Failed to connect to '+ device_verify+ ' to verify:')
        logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - Failed to connect to '+ device_verify+ ' to verify:'+'\n')
print('*'*79)
logfile.write('*'*79+'\n')
if device_ver == []:
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - No devices met requirements for code upgrade to run')
    logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - No devices met requirements for code upgrade to run'+'\n')
    print('*'*79)
    logfile.write('*'*79+'\n')
print('~'*79)
logfile.write('~'*79+'\n')
print('~'*17,'Script has completed all specified functions','~'*16)
logfile.write('~'*17+' Script has completed all specified functions '+'~'*16+'\n')
print('~'*29,datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'~'*29)
logfile.write('~'*29+datetime.now().strftime(' %Y-%m-%d %H:%M:%S ')+'~'*29+'\n')
print('~'*79)
logfile.write('~'*79+'\n')
logfile.close()
