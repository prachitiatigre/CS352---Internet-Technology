import socket
import signal
import sys
import random
import datetime

# Read a command line argument for the port where the server
# must run.
port = 8080
if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    print("Using default port 8080")

# Start a listening server socket on the port
sock = socket.socket()
sock.bind(('', port))
sock.listen(2)

### Contents of pages we will serve.
# Login form
login_form = """
   <form action = "http://localhost:%d" method = "post">
   Name: <input type = "text" name = "username">  <br/>
   Password: <input type = "text" name = "password" /> <br/>
   <input type = "submit" value = "Submit" />
   </form>
""" % port
# Default: Login page.
login_page = "<h1>Please login</h1>" + login_form
# Error page for bad credentials
bad_creds_page = "<h1>Bad user/pass! Try again</h1>" + login_form
# Successful logout
logout_page = "<h1>Logged out successfully</h1>" + login_form
# A part of the page that will be displayed after successful
# login or the presentation of a valid cookie
success_page = """
   <h1>Welcome!</h1>
   <form action="http://localhost:%d" method = "post">
   <input type = "hidden" name = "action" value = "logout" />
   <input type = "submit" value = "Click here to logout" />
   </form>
   <br/><br/>
   <h1>Your secret data is here:</h1>
""" % port

#### Helper functions
# Printing.
def print_value(tag, value):
    print "Here is the", tag
    print "\"\"\""
    print value
    print "\"\"\""
    print

# Signal handler for graceful exit
def sigint_handler(sig, frame):
    print('Finishing up by closing listening socket...')
    sock.close()
    sys.exit(0)
# Register the signal handler
signal.signal(signal.SIGINT, sigint_handler)


# TODO: put your application logic here!

login_credentials = {}
login_file = open("passwords.txt")
for line in login_file: 
    key,value = line.split()
    login_credentials[key] = value
print "Login Credentials=", login_credentials

secret_data = {}
secret_file = open("secrets.txt")
for line in secret_file: 
    key, value = line.split()
    secret_data[key] = value
print "Secret Data=", secret_data

print(" ------------------ Here ------------------ ")
cookie_val = {}
cookie_file = open("cookies.txt", "a+")
for line in cookie_file: 
    # if line.read(1):
    key, value = line.split()
    cookie_val[key] = value
print "Secret Data=", cookie_val

### Loop to accept incoming HTTP connections and respond.
while True:

    # cookie_val = {}
    # cookie_val = open("cookies.txt", "w") 

    client, addr = sock.accept()
    req = client.recv(1024)

    # Let's pick the headers and entity body apart
    header_body = req.split('\r\n\r\n')
    headers = header_body[0]
    body = '' if len(header_body) == 1 else header_body[1]
    print_value('headers', headers)
    print_value('entity body', body)
    html_content_to_send = login_page
    headers_to_send = ''

    sub = "&"
    ####
    if body != "" and (sub in body):
        
        user_pass = body.split("&")
        username_split = ((body.split("&"))[0])[9:]
        password_split = ((body.split("&"))[1])[9:]
        print('Username = ' + str(username_split))
        print('Password = ' + str(password_split))

        # You need to set the variables:
        # (1) `html_content_to_send` => add the HTML content you'd
        # like to send to the client.
        # Right now, we just send the default login page.
        
        # Get cookie from header
        cookie = ''
        cookieToken = ''
        for line in headers.split('\r\n'):
            hv = line.split(':')
            if(len(hv) == 2):
                h, v = hv
                if h == 'Cookie':
                    cookie = v.strip()
                    cookieToken = cookie[6:]

        # Correct username
        if username_split in login_credentials:
            print('Correct Username')
            
            # Correct username AND password
            if (username_split, password_split) in login_credentials.items():
                print('Correct username and password')
                
                # Username exists in cookie val
                # Check if token from header matches token in cookie val
                # If it does, then it should also match the username
                if username_split in cookie_val.values() and cookie_val.has_key(str(cookieToken)):
                    print('Cookie Val has header token')
                    print('Header Token = ' +str(cookieToken))
                        
                    # Both username and cookie token from header are in cookie val
                    # Check if they both match
                    if ((cookie_val.has_key(str(cookieToken))) and (cookie_val.get(cookieToken) == username_split)):
                        print("Correct username, correct password - cookie exists & DOES matche")
                        html_content_to_send = success_page + str(secret_data.get(cookie_val.get(cookieToken)))
                        
                    else:
                        print("Correct username, correct password - cookie exists & DOES NOT match")
                        html_content_to_send = bad_creds_page
                    # else:
                    #     print('Here')
                
                # Correct username AND password. Username does not exist in cookie val. New login
                else:
                        
                    print("Correct username, correct password - cookie does not exist, set cookie")
                    rand_val = random.getrandbits(64)
                    headers_to_send = 'Set-Cookie: token='+ str(rand_val) + '\r\n'
                            
                    cookie_val[str(rand_val)] = username_split
                    cookie_file.write(str(rand_val) + " " + str(username_split) + "\n")
                    
                    html_content_to_send = success_page + str(secret_data.get(username_split))
            
            # Correct username, incorrect password
            else:
                
                print(cookie_val)
                print(cookieToken)
                print(cookie_val.get(cookieToken))
                print(username_split)
                if ((cookie_val.has_key(str(cookieToken))) and (cookie_val.get(cookieToken) == username_split)):
                    print("Correct username, incorrect password, check for cookie - cookie exists")                            
                    html_content_to_send = success_page + str(secret_data.get(cookie_val.get(cookieToken)))

                else:
                    print("Correct username, incorrect password, check for cookie - cookie does not exist")
                    html_content_to_send = bad_creds_page 

        # Either incorrect username or 
        # Blank username
        else:
            print("Nothing Header Token = " +str(cookieToken))

            # if username_split == '' and password_split == '' and cookie_val.has_key(str(cookieToken)):
            if cookie_val.has_key(str(cookieToken)):
                print("Username and Password blank or incorrect username")
                html_content_to_send = success_page + str(secret_data.get(cookie_val.get(cookieToken)))

            else:

                if username_split != '' or password_split != '':
                    html_content_to_send = bad_creds_page

                else:
                #if username_split == '' and password_split == '':
                    html_content_to_send = login_page        
    else:
        print("Not Logging out")
    
    if body == "action=logout":
        cookie = ''
        for line in headers.split('\r\n'):
            hv = line.split(':')
            if(len(hv) == 2):
                h, v = hv
                if h == 'Cookie':
                    cookie = v.strip()
                    cookieToken = cookie[6:]
                    # expires = datetime.datetime.utcnow() + datetime.timedelta(days=30)
                    # headers_to_send = 'Set-Cookie: token='+ str(cookieToken) + '; expires=' +str(expires.strftime("%a, %d %b %Y %H:%M:%S GMT")) 
                    headers_to_send = 'Set-Cookie: token='+ str(cookieToken) + '; expires=Thu, 01 Jan 1970 00:00:00 GMT\r\n' 
                    cookie_val = {}
        

    # html_content_to_send = login_page
    # But other possibilities exist, including
    # html_content_to_send = success_page + <secret>
    # html_content_to_send = bad_creds_page
    # html_content_to_send = logout_page
    
    # (2) `headers_to_send` => add any additional headers
    # you'd like to send the client?
    # Right now, we don't send any extra headers.
    # headers_to_send = ''

    # Construct and send the final response
    response  = 'HTTP/1.1 200 OK\r\n'
    response += headers_to_send
    response += 'Content-Type: text/html\r\n\r\n'
    response += html_content_to_send
    print_value('response', response)    
    client.send(response)
    client.close()
    
    print "Served one request/connection!"
    print

# We will never actually get here.
# Close the listening socket
sock.close()
