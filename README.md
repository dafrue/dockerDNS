# DockerDNS
DockerDNS ist ein virtuelles, Docker-basiertes Netzwerk zur Veranschaulichung von DNS-Anfragen.

## Voraussetzungen
* Docker Engine 1.13.0+
* Docker Compose 1.13.0+

Details zur Installation von Docker können Sie [hier](https://docs.docker.com/install/#supported-platforms) einsehen.

Details zur Installation von Docker Compose können Sie [hier](https://docs.docker.com/compose/install/) einsehen.
### Installation überprüfen:
```bash
$ docker --version
$ docker-compose --version
```

## Verwendung
### Starten des Netzwerks
Um das Netzwerk zu starten, öffnen Sie ein Terminal und navigieren zur  `docker-compose.yml`-Datei im Hauptordner des Projekts. Führen Sie dort den Befehl `docker-compose up` aus und warten Sie darauf, dass die Client- und DNS-Container vollständig gestartet sind.

Dies kann bei der ersten Ausführung ein paar Minuten dauern, da die benötigten Images erst von Docker erstellt werden müssen.

### Absenden einer DNS-Anfrage
Sobald das Netzwerk vollständig erstellt worden ist, können sie das Command & Control Interface in ihrem Browser unter der Adresse `localhost` finden.

Dort befindet sich unter anderem eine Liste aller im Netzwerk befindlichen Clients. Klicken Sie nun auf einen Client, von dem aus die gewünschte Anfrage gesendet werden soll.

Auf der Oberfläche des Clients können Sie nun die aufzulösende Adresse eingeben und den DNS-Server auswählen, der die Anfrage bearbeiten soll. Der Button `Auflösen` schickt die gewünschte DNS-Anfrage ab.

### Logging
Mit dem `Merge`-Button im Interface (`localhost`) können Sie nun die Netzwerklogs ihrer Anfragen zusammenfassen.

Der Ordner `logs` enthält die Netzwerklogs aus Sicht der einzelnen Nameserver sowie die Datei `merged_logs`, welche die zusammengefassten Netzwerklogs enthält.

Zur Auswertung der Logs können Sie Programme wie beispielsweise **Wireshark** oder **tcpdump** verwenden.

### Herunterfahren des Netzwerks
Zum Herunterfahren des Netzwerks, öffnen Sie erneut ein Terminal und navigieren zur `docker-compose.yml`-Datei im Hauptordner des Projekts. Führen Sie dort den Befehl `docker-compose down` aus und warten Sie darauf, dass alle Container erfolgreich beendet wurden.

## Das Beispielnetzwerk
Das Projekt ist standardmäßig mit dem folgenden Beispielnetzwerk konfiguriert:


```
                    | IP (172.20.x.x)   | Type
--------------------+-------------------+-----------
. (root)            | 10.1              | Nameserver
  belag             | 10.2              | Nameserver
    kaese           | 10.10             | Nameserver
      gouda         | 0.2               | Client
      edamer        | 0.3               | Client
      fleisch       | 0.4               | Client
    wurst           | 10.11             | Nameserver
      salami        | 0.5               | Client
      fleisch       | 0.6               | Client
      chorizo       | 0.7               | Client
    aufstrich       | 10.12             | Nameserver
      wurst         | 10.20             | Nameserver
        leber       | 0.8               | Client
      kaese         | 10.21             | Nameserver
        frisch      | 0.9               | Client
      mett          | 0.10              | Client
```



## Konfiguration eigener Netzwerke
Im folgenden Kapitel wird darauf eingegangen, wie DockerDNS mit benutzerdefinierten Netzwerken konfiguriert werden kann.

Im folgenden Kapitel wird dazu der Inhalt der `docker-compose.yml` und des `config`-Ordners behandelt.

### `docker-compose.yml`
Die `docker-compose.yml` enthält die Einstellungen und Start-Parameter für alle Container im Netzwerk.

Das Image für die *Command & Control*-Instanz wird aus den Dateien im `cnc`-Ordner generiert. Das Netzwerk enthält nur eine Instanz des CnC Images. Die CnC-Instanz hat eine feste IP im Netzwerk und ist der einzige Container, der von außen über den Localhost Port 80 zugänglich ist. Sie mountet die `clients.txt` und den `logs`-Ordner, um die Clients im Web-Interface anzuzeigen und Logs auf der Hostmaschine ablegen zu können.

Die *Client*-Instanzen werden aus dem `client`-Ordner generiert. Den Clients werden keine festen IPs zugewiesen, stattdessen füllen sie den weiter unten in der Datei definierten IP-Bereich im internen Netzwerk. Sie mounten die `servers.txt`, um die Nameserver im Webinterface anzuzeigen. Das `scale`-Parameter bestimmt die Anzahl der generierten Client-Instanzen.

Die DNS-Server werden einzeln beschrieben, da sie eine feste IP benötigen. Ihr Image wird aus dem `dns`-Ordner generiert. Den *Nameserver*-Instanzen wird die Umagebungsvariable `NSLOGNAME` zugewiesen. Diese bestimmt den Namen der vom Nameserver generierten Logdatei. Die individuelle Konfiguration der Server erfolgt über Konfigurationsdateien, die von den Serverinstanzen gemountet werden. Im Beispielnetzwerk liegen diese im `config`-Ordner. Die Dateien `named.conf.options` und `named.conf.local` sind dabei Einstellungen für den Server. Der `zones`-Ordner enthält die Zonefiles und damit die DNS-Zone Definitionen. Die Datei `db.root` enthält die DNS-Informationen des internen Rootservers. Des Weiteren wird noch der `logs`-Ordner gemountet, damit der DNS-Server dort Logdateien auf dem Host-System ablegen kann.

Im letzten Abschnitt wird das Netzwerk definiert. Es handelt sich hier um ein internes Bridge-Netzwerk. Der `subnet`-Parameter bestimmt den IP-Bereich für die Container im Netzwerk und somit auch die dynamisch vergebenen IPs der Client-Instanzen.

Eine detaillierte Referenz zur Compose Datei kann [hier]("https://docs.docker.com/compose/compose-file/compose-file-v2/") gefunden werden.

### Der `config`-Ordner
Der `config`-Ordner enthält die von den *CnC*, *Client* und *Nameserver* Instanzen eingebundenen Konfigurationsdateien.

#### `clients.txt`

Diese Datei enthält die Adressen und Namen der Clients im Netzwerk, die von der CnC-Instanz gelesen werden, um sie im Web-Interface anzuzeigen.

Jeder Client steht in einer eigenen Zeile, angegeben durch seine IP-Adresse und seinen Namen im Web-Interface, getrennt mit einem Leerzeichen. Der Name selbst kann beliebig viele Leerzeichen enthalten, da nur das erste Leerzeichen in einer Zeile als Trennzeichen geparst wird.

Die Zeile `172.20.0.2 Gouda (172.20.0.2 | gouda.kaese.belag)` beschreibt einen Client mit der Adresse `172.20.0.2` und dem Anzeigenamen `Gouda (172.20.0.2 | gouda.kaese.belag)`. Der Anzeigename muss dabei die Adresse nicht noch einmal enthalten.

#### `servers.txt`
Diese Datei enthält die Adressen und Namen der Nameserver im Netzwerk. Sie wird von den Client-Instanzen gelesen, sodass diese sie im Web-Interface zur Verfügung stellen können.

Genau wie die Clients in `clients.txt`, steht jeder Server in einer eigenen Zeile und ist mit seiner Adresse und seinem Anzeigenamen, getrennt durch ein Leerzeichen, angegeben. Die Servernamen können ebenfalls beliebig viele Leerzeichen enthalten, da nur das erste Leerzeichen als Trennzeichen geparst wird.

Die Zeile `172.20.10.10 ns.kaese.belag (172.20.10.10)` beschreibt einen Nameserver mit der Adresse `172.20.10.10` und dem Anzeigenamen `ns.kaese.belag (172.20.10.10)`. Auch hier ist es nicht notwendig, dass der Anzeigename die Adresse des Servers enthält.

#### Der `dns` Ordner
In diesem Ordner liegen die Konfigurationsdateien der einzelnen Nameserver. Die Ordnerstruktur beeinflusst dabei nicht die Struktur des Netzwerks, sondern dient ausschließlich der Übersichtlichkeit.

## Beispiel: Hinzufügen eines neuen Servers und Clients
Im folgenden werden wir das Subnetz `marmelade.auftsrich.belag` sowie den Client `erbeer.marmelade.aufstrich.belag` zum Netzwerk hinzufügen. Zuerst sollten wir dazu die IP des neuen Servers festlegen. Der Einfachheit halber setzen wir das Muster des Beispielnetzwerks fort und geben unserem neuen Nameserver die Adresse `172.20.10.22`. Unser neuer Client erhält dynamische eine Adresse im in der `docker-compose.yml` definierten IP-Bereich. Da die Adressen bei `172.20.0.2` starten und es insgesamt unser zehnter Client ist, ist die Adresse `172.20.0.11`.

```
                    | IP (172.20.x.x)   | Type
--------------------+-------------------+-----------
. (root)            | 10.1              | Nameserver
  belag             | 10.2              | Nameserver
    kaese           | 10.10             | Nameserver
      gouda         | 0.2               | Client
      edamer        | 0.3               | Client
      fleisch       | 0.4               | Client
    wurst           | 10.11             | Nameserver
      salami        | 0.5               | Client
      fleisch       | 0.6               | Client
      chorizo       | 0.7               | Client
    aufstrich       | 10.12             | Nameserver
      wurst         | 10.20             | Nameserver
        leber       | 0.8               | Client
      kaese         | 10.21             | Nameserver
        frisch      | 0.9               | Client
      mett          | 0.10              | Client
                    |                   |
+     marmelade     | 10.22             | Nameserver
+       erdbeer     | 0.11              | Client
```

Als nächstes legen wir die Zonefile für den neuen Nameserver an.

```
$TTL  604800
@ IN  SOA ns.marmelade.aufstrich.belag. admin.marmelade.aufstrich.belag. (
            5   ; Serial
       604800   ; Refresh
        86400   ; Retry
      2419200   ; Expire
       604800 ) ; Negative Cache TTL
;
; name servers - NS records
            IN  NS  ns.marmelade.aufstrich.belag.

; name servers - A records
ns          IN  A 172.20.10.22

; A records
erdbeer     IN  A 172.20.0.11
```

Dieses Zonefile enthält ein *Start of Authority (SOA)* Statement für die Zone, einen *Nameserver (NS) Record* für unseren neuen Nameserver `ns.marmelade.aufstrich.belag` und dessen *A Record* sowie den *A Record* des neuen Clients `erdbeer.marmelade.aufstrich.belag`.

Nun müssen wir den neuen Nameserver noch zum Zonefile der übergeordneten Domain, in diesem Fall `aufstrich.belag`, hinzufügen. Hierzu öffnen wir das Zonefile des Nameservers `ns.auftrich.belag` und fügen einen neuen *NS* und *A* Record für `ns.marmelade.aufstrich.belag` ein.

```
$TTL  604800
@ IN  SOA ns.aufstrich.belag. admin.aufstrich.belag. (
            5   ; Serial
       604800   ; Refresh
        86400   ; Retry
      2419200   ; Expire
       604800 ) ; Negative Cache TTL
;
; name servers - NS records
            IN  NS  ns.aufstrich.belag.
wurst       IN  NS  ns.wurst.aufstrich.belag.
kaese       IN  NS  ns.kaese.aufstrich.belag.

; +++ NEU +++
marmelade   IN  NS ns.marmelade.auftsrich.belag.

; name servers - A records
ns            IN  A 172.20.10.12
ns.wurst      IN  A 172.20.10.20
ns.kaese      IN  A 172.20.10.21

; +++ NEU +++
ns.marmelade  IN  A 172.20.10.22

; A records
mett        IN  A 172.20.0.10
```

Nachdem wir die neuen Zonefiles erstellt haben, legen wir die restlichen Konfigurationsdateien für unseren neuen Server an. In `named.conf.local` verweisen wir den Server auf unser soeben erstelltes Zonefile:

```
zone "marmelade.aufstrich.belag" {
  type master;
  file "/etc/bind/zones/db.marmelade.aufstrich.belag";
};
```

Die Datei `named.conf.options` enthält weitere Optionen für den Server:

```
options {
  directory "/var/cache/bind";

  recursion yes;
  listen-on { 172.20.10.22; };  # NS IP anpassen!
  allow-transfer { none; };

  dnssec-validation no;
  max-cache-ttl 0;              # kein Caching
  max-ncache-ttl 0;

  auth-nxdomain no;
};
```

Nun da wir die Konfigurationsdateien des Servers angelegt haben, fügen wir ihn zur `docker-compose.yml` hinzu. Hier ist es wichtig, dass wir die korrekten Konfigurationsdateien mounten.

```
#=======================================
#DNS Server
#=======================================
[...]

ns.marmelade.aufstrich.belag:
    build: ./dns
    image: dockerdns-ns:1.0
    networks:
      dnsbridge:
        ipv4_address: 172.20.10.22
    environment:
      - NSLOGNAME=ns.marmelade.aufstrich.belag
    volumes:
      - ./config/dns/ns.marmelade.aufstrich.belag/named.conf.options:/etc/bind/named.conf.options
      - ./config/dns/ns.marmelade.aufstrich.belag/named.conf.local:/etc/bind/named.conf.local
      - ./config/dns/ns.marmelade.aufstrich.belag/zones:/etc/bind/zones
      - ./config/dns/db.root:/etc/bind/db.root
      - ./logs:/logs

[...]
```

Unseren neuen Client fügen wir hinzu, indem wir einfach das `scale` Parameter im Client Abschnitt erhöhen (in unserem Fall von 9 auf 10), damit eine weitere Clientinstanz generiert wird:

```
#======================================
#Clients
#======================================  
  client:
    build: ./client
    image: dockerdns-client:1.0
    dns_search: .
    networks:
      - dnsbridge
    volumes:
      - ./config/servers.txt:/app/config/servers.txt:ro
    scale: 10
```

Alternativ könnten wir auch einen neuen Client erstellen, etwa wenn wir einen Client mit einer spezifischen IP generieren wollen.

Zuletzt müssen wir den neuen Server noch zur `servers.txt` und den neuen Client noch zur `clients.txt` hinzufügen, damit sie im Web-Interface verfügbar sind.

`servers.txt`: `172.20.10.22 ns.marmelade.aufstrich.belag (172.20.10.22)`

`clients.txt`: `172.20.0.11 Erdbeer (172.20.0.11 | erdbeer.marmelade.aufstrich.belag)`
