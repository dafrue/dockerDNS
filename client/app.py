from flask import Flask
from flask import request
import subprocess
import socket

app = Flask(__name__)

@app.route("/", methods=("GET", "POST"))
def hello():
    html = """<a href="http://172.20.20.10">&lt&lt zur&uuml;ck</a>
           <form method="post"><fieldset><legend>DNS Aufl&ouml;sung</legend>
           Adresse:<br>
           <input type="text" name="address" required><br>
           DNS Server:<br>
           <select name="server" required>"""
    with open("/app/config/servers.txt","r") as stxt:
        servers = stxt.readlines()
        servers = [(server.split(" ", 1)[0],server.split(" ", 1)[1]) for server in servers]
        for server in servers:
            if len(server) == 2:
                html += '<option value="{ip}">{name}</option>'.format(ip=server[0], name=server[1])           
    html += """</select><br><br>
            <input type="submit" value="Aufl&ouml;sen"></form>
            <fieldset><legend>Output</legend>{output}</fieldset>
            </fieldset><br>
            <b>Hostname:</b> {hostname}<br/>"""
    if request.method == "POST":
        name = request.form["address"]
        server = request.form["server"]
        try:
            dnsresp = subprocess.check_output(["host",name,server]) 
            return html.format(output=dnsresp, hostname=socket.gethostname())
        except subprocess.CalledProcessError as e:
            dnsresp = e.output
            return html.format(output=dnsresp, hostname=socket.gethostname())
    return html.format(output="", hostname=socket.gethostname())

if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0', port=80)
