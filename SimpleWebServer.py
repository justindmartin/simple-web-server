import os.path
import socket

class SimpleWebServer:
    def __init__(self, port):
        print("You initialized a SimpleWebServer instance at localhost on port " + str(port) + " (:")
        self.startServer("localhost", port)

    def processFile(self, filename):
        #long list of file types, mapped to their extension
        fileTypes = {
            "bmp": "image/bmp",
            "css": "text/css",
            "htm": "text/html",
            "html": "text/html",
            "ico": "image/x-icon",
            "jpe": "image/jpeg",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "mp2": "audio/mpeg",
            "mp3": "audio/mpeg",
            "mp4": "audio/mp4",
            "mpe": "video/mpeg",
            "mpeg": "video/mpeg",
            "ogg": "application/ogg",
            "pdf": "application/pdf",
            "png": "image/png",
            "ppt": "application/vnd.ms-powerpoint",
            "ps": "application/postscript",
            "qt": "video/quicktime",
            "qti": "image/x-quicktime",
            "qtif": "image/x-quicktime",
            "rtf": "text/rtf",
            "rtx": "text/richtext",
            "svg": "image/svg+xml",
            "swf": "application/x-shockwave-flash",
            "tif": "image/tiff",
            "tiff": "image/tiff",
            "txt": "text/plain",
            "wav": "audio/x-wav",
            "xhtml": "application/xhtml+xml",
            "xls": "application/vnd.ms-excel",
            "xsl": "application/xml",
            "zip": "application/zip"

        }

        #remove transversal characters
        filename = filename[1:]
        while filename.find("..") != -1:
            filename = filename.replace("..", "")

        try:
            fileType = fileTypes[filename.split(".")[-1].lower()]
        except:
            fileType = "text/plain"

        try:
            fh = open(filename, "rb")
            fileContents = fh.read()
            fh.close()
            fileSize = len(fileContents)
            statusCode = "200 OK"
        except:
            fileContents = "<!DOCTYPE HTML><html><head><title>404 - Page Not Found</title></head><body><h1>404 - That page was not found :(</h1></body></html>"
            fileType = "text/html"
            fileSize = len(fileContents)
            statusCode = "404 Not Found"
            
        return [statusCode, fileSize, fileType, fileContents]

    def startServer(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        while True:
            serverSocket, hostAddr = sock.accept()
            request = serverSocket.recv(2048).decode("UTF-8").split("\r\n")
            filename = request[0][request[0].find(" ")+1:request[0].rfind(" ")]
            statusCode, fileSize, fileType, fileContents = self.processFile(filename)
            response = "HTTP/1.1 " + statusCode;
            if fileType != "" and fileSize != "" and fileContents != "":
                response += "\r\nContent-Type: " + fileType
                response += "\r\nContent-Length: " + str(fileSize)
                response += "\r\n\r\n" + fileContents
            serverSocket.sendall(response)
            #hostAddr[0] is client address
            serverSocket.close()