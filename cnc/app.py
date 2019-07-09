from flask import Flask
from flask import request
import subprocess
import socket

app = Flask(__name__)

@app.route("/", methods=("GET", "POST"))
def hello():
    clients = []
    html = "<fieldset><legend>Clients</legend>"
    with open("/app/config/clients.txt","r") as ctxt:
        clients = ctxt.readlines()
        clients = [(client.split(" ", 1)[0],client.split(" ", 1)[1]) for client in clients]
        for client in clients:
            if len(client) == 2:
                html += '<a href="http://{ip}">{name}</a><br>'.format(ip=client[0], name=client[1])
    html += """</fieldset><br><fieldset><legend>Logs</legend>
            <form method="post"><input type="submit" name="merge" value="Merge">{merge_status}</form></fieldset>"""
    html += "<br><b>Hostname:</b> {hostname}"
    if request.method == "POST":
        if "merge" in request.form:
            try:
                console_output = subprocess.check_output(["sh","-c","mergecap -w /logs/merged_logs /logs/*"]) 
                return html.format(merge_status=" - Done", hostname=socket.gethostname())
            except subprocess.CalledProcessError as e:
                console_output = e.output
                return html.format(merge_status=" - "+console_output, hostname=socket.gethostname())
    return html.format(merge_status="", hostname=socket.gethostname())

if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0', port=80)
