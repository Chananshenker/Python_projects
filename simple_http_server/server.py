# this is a simple http server that works with an SQLite3 database
# the SQLite3 datatbse needs to be set up before the server is run
# the html pages are included in this repository

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import sqlite3

con = sqlite3.connect("main.db", check_same_thread=False)
cur = con.cursor()

class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/feed.html':
            self.display_feed()
            return
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except FileNotFoundError:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    def display_feed(self):
        try:
            cur.execute("SELECT name, thoughts, time FROM thoughts ORDER BY id DESC LIMIT 10")
            rows = cur.fetchall()

            with open("feed.html", "r") as file:
                html = file.read()

            content = ""
            for row in rows:
                name, thoughts, timestamp = row
                content += f"""
                    <tr>
                        <td>{name}</td>
                        <td>{thoughts}</td>
                        <td>{timestamp}</td>
                    </tr>
                """

            html = html.replace("{{content}}", content)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(html, 'utf-8'))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(bytes(f"Error: {e}", 'utf-8'))

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('ascii')

        form_data = parse_qs(post_data)
        name_form = form_data["name"][0]
        thoughts_form = form_data["thoughts"][0]

        cur.execute("INSERT INTO thoughts (name, thoughts) VALUES (?, ?)", (name_form, thoughts_form))
        con.commit()

        self.send_response(302)
        self.send_header("Location", "http://localhost:8888/")
        self.end_headers()
        
httpd = HTTPServer(('localhost', 8888), Serv)
print("server running...")
httpd.serve_forever()
