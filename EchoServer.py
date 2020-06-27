#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 12345        # Port to listen on (non-privileged ports are > 1023)

print('Start server on %s:%s' % (HOST, PORT))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print('received "%s"' % data)
            conn.sendall(b'HTTP/1.1 200 OK\r\n Date: Mon, 27 Jul 2009 12:28:53 GMT\r\n Server: Apache/2.2.14 (Win32)\r\n Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT\r\n Content-Length: 88\r\n Content-Type: text/html\r\n Connection: Closed\r\n\r\n <html> <!-- Text between angle brackets is an HTML tag and is not displayed.; Most tags, such as the HTML and /HTML tags that surround the contents of; a page, come in pairs; some tags, like HR, for a horizontal rule, stand; alone. Comments, such as the text you"re reading, are not displayed when; the Web page is shown. The information between the HEAD and /HEAD tags is not displayed. The information between the BODY and /BODY tags is displayed.--> <head> <title>Enter a title, displayed at the top of the window.</title> </head> <!-- The information between the BODY and /BODY tags is displayed.--> <body> <h1>Enter the main heading, usually the same as the title.</h1> <p>Be <b>bold</b> in stating your key points. Put them in a list: </p> <ul> <li>The first item in your list</li> <li>The second item; <i>italicize</i> key words</li> </ul> <p>Improve your image by including an image. </p> <p><img src="http://www.mygifs.com/CoverImage.gif" ></p> <p>Add a link to your favorite <a href=>Web site</a>.Break up your page with a horizontal rule or two. </p> <hr> <p>Finally, link to <a href="page2.html">another page</a> in your own Web site.</p> <!-- And add a copyright notice.--> <p> Wiley Publishing, 2011</p> </body> </html>\r\n\r\n\r\n ')
            break
print('Finish server on %s:%s' % (HOST, PORT))