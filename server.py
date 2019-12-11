from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from tickets_db import ticketsDB
import json
import random
from http import cookies


class MyRequestHandler (BaseHTTPRequestHandler):

    def ticketCreated(self):
        if "Oompa" in self.cookie:
            print("OOMPA DETECTED")
            return True
        else:
            print("OOMPA UNDETECTED")
            return False

    def end_headers(self):
        self.send_cookie()
        self.send_header("Access-Control-Allow-Origin", self.headers["origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)

    def load_cookie(self):
        if "Cookie" in self.headers:
            print("COOKIE LOADED")
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()
            print("cOOkie DID NOT lOaded")

    def send_cookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

    def do_GET(self):
        self.load_cookie()
        if self.path == "/entries":
            self.handleEntries()
        else:
            self.handleNotFound()

    def do_POST(self):
        self.load_cookie()
        if self.ticketCreated():
            self.send_response(403)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
        else:
            if self.path == "/entries":
                self.createEntry()

    def handleNotFound(self):
        self.send_error(404)
        self.end_headers()
        pass

    def handleEntries(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        db = ticketsDB()
        entries = db.getEntries()
        self.wfile.write(bytes(json.dumps(entries), "utf-8"))

    def createEntry(self):
        length = self.headers["Content-Length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        print("BODY:", body)
        parsed_body = parse_qs(body)
        print("PARSED BODY:", parsed_body)
        entrant_name = parsed_body["entrant_name"][0]
        entrant_age = parsed_body["entrant_age"][0]
        guest_name = parsed_body["guest_name"][0]
        random_token = random.randint(0, 6)
        db = ticketsDB()
        db.insertEntry(entrant_name, entrant_age,
                       guest_name, random_token)

        # SEND COOKIE
        #self.cookie["Oompa"] = "Loopa"
        #self.cookie["Oompa"] = ["Loopa"]
        #self.cookie['Oompa'] = 'Loopa'
        self.cookie['Oompa'] = "Loopa"
        print("COOKIE VALUE HAS BEEN SET")

        self.send_response(201)
        self.end_headers()
        pass


def run():
    listen = ("127.0.0.1", 8080)
    server = HTTPServer(listen, MyRequestHandler)
    print("Listening...")
    server.serve_forever()


run()
