# Client version 3.0

import socketserver, socket, time, os, sys, subprocess, logging
from threading import Thread

logging.disable(999)

try:
    import winsound, ctypes

except:
    class winsound:
        MB_ICONEXCLAMATION = None
        def MessageBeep(type):
            return "This is a faked module because you are not on Windows"

try:
    from win10toast import ToastNotifier # Enable basic notification support
    NOTIFICATIONS_INITIALIZED = True
    toaster = ToastNotifier()
except ModuleNotFoundError:
    continst = input("\u001b[31;1mShoutout was unable to initialize notification support because it requires additional python modules. Do you want to install notification support? [Y/N] > \u001b[0m").capitalize()

    if (continst == "Y"):
        subprocess.run("pip install win10toast")
        os.startfile(__file__)
        print("Reloading Shoutout")
        os.abort()
    else:
        NOTIFICATIONS_INITIALIZED = False
        print("\u001b[34;1mContinuing without notification support...\u001b[0m")
        time.sleep(2)
except:
    NOTIFICATIONS_INITIALIZED = False
    print("\u001b[34;1mContinuing without notification support...\u001b[0m")
    

VERSION = "3.0"
if socket.gethostbyname(socket.gethostname()) == "127.0.0.1":
    MODE_PREFIX = " (Offline)"
else:
    MODE_PREFIX = ""

DRIVELETTER = str(os.environ['WINDIR'].split(":\\")[0])
DATAPATH = "%s:/ProgramData/shoutout"%DRIVELETTER

class encryption():
    """
    Encode and decode messages using a tri-base encryption scheme
    """
    def encrypt(text):
        """
        Encrypts a message to be sent over the network. 
        The exact process of how the message is encrypted is not exposed to the standard user to help keep messages secure
        """

        #dictionary_letters contains the key for scrambling the message. Ex: the letter a will turn to t

        dictionary_letters = {'a':'t', 'b':'u', 'c':'d', 'd':'e', 'e':'v', 'f':'q', 'g':'l', 'h':'m', 'i':'c', 'j':'k', 'k':'w', 'l':'n', 'm':'b', 'n':'h', 'o':'g', 'p':'p', 'q':'o', 'r':'f', 's':'a', 't':'i', 'u':'r', 'v':'j', 'w':'s', 'x':'x', 'y':'z', 'z':'y', 'A':'T', 'B':'U', 'C':'D', 'D':'E', 'E':'V', 'F':'Q', 'G':'L', 'H':'M', 'I':'C', 'J':'K', 'K':'W', 'L':'N', 
    'M':'B', 'N':'H', 'O':'G', 'P':'P', 'Q':'O', 'R':'F', 'S':'A', 'T':'I', 'U':'R', 'V':'J', 'W':'S', 'X':'X', 'Y':'Z', 'Z':'Y'}
        
        #partial encode contains the message after scrambling letter. The for loop goes through every character in the message and replaces it with the value shown in dictionary_letters. However, if that value doesn't exist, that character remains unchanged.
        partialEncode=''
        for c in text:
            partialEncode=partialEncode+dictionary_letters.get(c, c)

        #Second stage of encoding turns the scrambled letters into their ascii codes.To make it more secure, we're adding 10 to the ascii code. For example, 97 for the letter a turns to 107.
        ascii_values = ''
        for character in partialEncode: # loop through every letter
            ascii_values = ascii_values + str(ord(character) + 10) + "." # convert each letter into an ascii representation (shifted by 10), then add the seperator string (".")

        return ascii_values # sends the encoded message back to the calling function


    def decrypt(ascii_values):
        """Decrypts a message to be printed in the terminal"""


        character = '' # a variable to hold the currently-selected character
        string = "" # a variable to hold the entire decrypted message

        try:
            for i in ascii_values: # for every interger in the passed-in encoded message
                if i != '.': #period determines the end of a character value
                    character = character + str(i) # adds each new character to the string
                else: #when it comes across period, it's time to decode that value
                    letter = chr(int(character)-10) # unshifts the character by 10, then decodes it back into a character
                    string = string + letter # appends the letter to the string
                    character='' # resets character to blank

            #this is the key for the scrambled letters for decoding. when the scrambled letter is t, it decoded to a.
            decode_dictionary_letters = {'t':'a', 'u':'b', 'd':'c', 'e':'d', 'v':'e', 'q':'f', 'l':'g', 'm':'h', 'c':'i', 'k':'j', 'w':'k', 'n':'l', 'b':'m', 'h':'n', 'g':'o', 'p':'p', 'o':'q', 'f':'r', 'a':'s', 'i':'t', 'r':'u', 'j':'v', 's':'w', 'x':'x', 'z':'y', 'y':'z', 'T':'A', 'U':'B', 'D':'C', 'E':'D', 'V':'E', 'Q':'F', 'L':'G', 'M':'H', 'C':'I', 'K':'J', 'W':'K', 'N':'L', 
        'B':'M', 'H':'N', 'G':'O', 'P':'P', 'O':'Q', 'F':'R', 'A':'S', 'I':'T', 'R':'U', 'J':'V', 'S':'W', 'X':'X', 'Z':'Y', 'Y':'Z'}
            
            #Each character is seached for in the dictionary, if it's there, it decodes the character.
            decoded=''
            for c in string:
                decoded=decoded+decode_dictionary_letters.get(c, c)

            return decoded # returns the decoded message to be printed on-screen
        except:
            return (ascii_values + RED + "    (Message sent without encryption)" + NORMAL)

def sendNotification(username, message, secure):
    if NOTIFICATIONS_INITIALIZED:
        icon = "chat-bubble-color.ico" if secure else "chat-bubble-insecure-color.ico"
        toast_sent = False
        # toaster.show_toast("%s (via Shoutout)"%username, "%s"%message, DATAPATH + "/" + icon, threaded=True)
        Thread(target=actuallySendNotificationViaThread, args=(username, message, icon)).start()

def actuallySendNotificationViaThread(username, message, icon):
    toast_sent = False
    while toast_sent == False:
        toast_sent = toaster.show_toast("%s (via Shoutout)"%username, "%s"%message, DATAPATH + "/" + icon, threaded=True)
        time.sleep(1)

os.system('cls')
os.system("title Shoutout v%s %s" % (VERSION, MODE_PREFIX))

if (os.name == "nt"):
    programID = u'pds.shoutout.beta-%s' % VERSION
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(programID)

INCHOST, PORT = str(socket.gethostbyname(socket.gethostname())), 1500 # Sets the host to the current IP and the port to 1500

BLUE = "\u001b[34;1m" # The color blue
YELLOW = "\u001b[33;1m" # The color yellow
RED = "\u001b[31;1m" # The color red
GREEN = "\u001b[32;1m"
NORMAL = "\u001b[0m" # Reset to default color
 
os.system("")

# print(GREEN + "Shoutout Client v%s" % VERSION + NORMAL)
 
# Variables used by both
receiver_running = False
serverIP = "NA"

# if (socket.gethostbyname(socket.gethostname()) == "127.0.0.1"):
#     print(YELLOW + "Warning: No network connection detected" + NORMAL)
 
# print("")
# Client variables
if not (os.path.isfile(DATAPATH + "/name")):
    print(YELLOW + "Reminder: your name cannot be changed later, so please make sure you set it to what you really want!" + RESET)
    name = input(BLUE + "Please enter your name > " + NORMAL) # User's name
    file = open(DATAPATH + "/name", "x")
    file.write(name)
    file.close()
    # print("")
else:
    name = open(DATAPATH + "/name", "r").read()
    print(YELLOW + "Welcome back, %s\n"%name + NORMAL)
 
# Receiver server class
class ReceiverSocket(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(4096).strip() # Grab the data that was sent to the server
        
        playsound(winsound.MB_ICONEXCLAMATION) # Notification sound

        try:
            decodedMessage = encryption.decrypt(str(self.data.decode()))
            message = decodedMessage
            secure = True

            sys.stdout.write("\u001b[1F\u001b[999C\n" + decodedMessage + "\n") # Print the message on-screen

        except:
            sys.stdout.write("\u001b[1F\u001b[999C\n" + str(self.data.decode()) + "\n") # Print the message on-screen
            message = str(self.data.decode())
            secure = False

        # secure = False

        try:sendNotification(message.split(":", 1)[0], message.split(":", 1)[1], secure)
        except:
            try:sendNotification("System", message, secure)
            except:
                try:sendNotification("System", "New notification has arrived", secure)
                except:NotImplemented
 

# Functions used by both parts of the file
 
def playsound(type):
    winsound.MessageBeep(type)


if __name__ == "__main__":
    def incoming():
        global receiver_running, serverIP

        # Create the server, binding to localhost on port 1500
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer((INCHOST, PORT), ReceiverSocket) as server:
            
            print(GREEN + "Your IP (give this to the other person): " + server.server_address[0] + NORMAL) # Print the current device's IP address, used ONLY for same-network connections
            print(BLUE + "Your Hostname (you can also give this to them): " + socket.gethostname() + NORMAL)
            
            if (socket.gethostbyname(socket.gethostname()) == "127.0.0.1"):
                print(YELLOW + "You aren't connected to a network. This info  will only work on THIS device!" + NORMAL)

            print("")
 
            receiver_running == True
            serverIP = server.server_address[0]
            server.serve_forever() # Makes sure the server stays running as long as the server terminal is open
 


    # Start the incoming messages thread
    Thread(target=incoming, name="receiver").start()
    time.sleep(0.5)
 
 
    HOST = input(BLUE + "Enter other person's IP > " + NORMAL)

    print(BLUE + "Attempting to connect..." + NORMAL)

    # Try to connect to the server
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # Sets a temporary socket connection
            sock.connect((HOST, PORT))
            sock.sendall(bytes(encryption.encrypt(name + " has established a connection"), "utf-8")) # the server looks for these words to print the login message on the server terminal
            sock.close()

    except Exception as err: # Something went wrong while trying to send the message
        if not (str(err) == "[Errno 11001] getaddrinfo failed"):
            print(RED + "[!] - Failed to announce presence to endpoint -- " + str(err) + NORMAL)
            time.sleep(30)
            os.abort()
        else:
            print(RED + "Unable to resolve destination '" + BLUE + HOST + RED + "'" + NORMAL)
 

    class client(): # The class that all of the client (outgoing messages) functions are stored within
        # Create a message to send to the remote computer
        def createMessage():
            time.sleep(0.25)

            try:
                message = input()
                sys.stdout.write(u"\x1b[1A" + u"\x1b[2K" + "\r")
                client.sendMessage(message)
            
            except KeyboardInterrupt:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # Sets a temporary socket connection
                    # Connect to server and send data
                    sock.connect((HOST, PORT))
                    sock.sendall(bytes(encryption.encrypt(name + " disconnected"), "utf-8"))
                    sock.close()
                os.system("title Shoutout v%s (Disconnecting...)" % (VERSION))
                os.abort()

            except EOFError:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # Sets a temporary socket connection
                    # Connect to server and send data
                    sock.connect((HOST, PORT))
                    sock.sendall(bytes(encryption.encrypt(name + " disconnected"), "utf-8"))
                    sock.close()
                os.system("title Shoutout v%s (Disconnecting...)" % (VERSION))
                os.abort()
 
        # Send the message the user just created
        def sendMessage(data):
            try:
 
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # Sets a temporary socket connection
                    message = encryption.encrypt(name + ": " + data)
                    # Connect to server and send data
                    sock.connect((HOST, PORT))
                    sock.sendall(bytes(message, "utf-8"))
                    sock.close()

            except Exception as err: # Something went wrong trying to send the message to the server
                if (str(err) != "[Errno 11001] getaddrinfo failed"):
                    print(RED + "\n[!] - Failed to send message -- " + str(err) + "\n" + NORMAL)
                else:
                    print(RED + "Unable to resolve destination '" + BLUE + HOST + RED + "'" + NORMAL )

    # Main process that lets the user enter messages
    def mainLoop():
        try:
            print("\n")
            while True:
                    client.createMessage()
        except KeyboardInterrupt:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # Sets a temporary socket connection
                # Connect to server and send data
                sock.connect((HOST, PORT))
                sock.sendall(bytes(encryption.encrypt(name + " disconnected"), "utf-8"))
                sock.close()
            os.system("title Shoutout v%s (Disconnecting...)" % (VERSION))
            os.abort()
 
 
    # Start up the outgoing message thread
    mainThread = Thread(target=mainLoop, name="sender")
    mainThread.start()