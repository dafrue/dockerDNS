# DockerDNS
DockerDNS ist ein virtuelles Docker-basiertes Netzwerk zu Veranschaulichung von DNS-Anfrage.

## Voraussetzungen
* Docker Engine 1.13.0+
* Docker Compose 1.13.0+

Details zur Installation von Docker können [hier](https://docs.docker.com/install/#supported-platforms) gefunden werden.

Details zur Installation von Docker Compose können [hier](https://docs.docker.com/compose/install/) gefunden werden.
### Installation überprüfen:
```bash
$ docker --version
$ docker-compose --version
```

## Verwendung
### Starten des Netzwerks
Um das Netzwerk zu starten, öffnen Sie ein Terminal und navigieren zu der Datei `docker-compose.yml` im Hauptordner des Projekts. Führen sie dort den Befehl `docker-compose up` aus und warten, bis die Client- und DNS-Container gestartet sind.

Beim ersten Start kann dies etwas länger dauern, da Docker die benötigten Images erst erstellen muss.

### Absenden einer DNS-Anfrage
Sobald das Netzwerk vollständig erstellt ist können sie das Command & Control Interface in ihrem Browser unter der Adresse `localhost` finden.

Dort befindet sich unter anderem eine Liste der Clients im Netzwerk. Klicken Sie nun auf den Client, von dem aus Sie eine Anfrage schicken wollen.

Auf dem Interface des Clients können sie nun die aufzulösende Adresse eingeben und den DNS-Server auswählen, der sie bearbeiten soll. Der Button `Auflösen` schickt die DNS-Anfrage ab.

### Logging
Mit dem Knopf `Merge` im C&C Interface (`localhost`) können Sie nun die Netzwerklogs ihrer Anfragen zusammenfassen.

Der Ordner `logs` enthält die Netzwerklogs aus Sicht der einzelnen Nameserver sowie die Datei `merged_logs`, die den gesamten Netzwerkverkehr enthält.

Zur Auswertung der Logs können Sie Programme wie **Wireshark** oder **tcpdump** verwenden.

### Herunterfahren des Netzwerks
Um das Netzwerk herunterzufahren, öffnen Sie erneut ein Terminal und navigieren zu der Datei `docker-compose.yml` im Hauptordner des Projekts. Führen Sie dort den Befehl `docker-compose down` aus und warten, bis alle Container erfolgreich beendet wurden.

## Das Beispiel-Netzwerk
Das Projekt ist standardmäßig mit dem folgenden Beispiel-Netzwerk konfiguriert:


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