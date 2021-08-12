# Gliederung / Table of Contents
1. Deutsche Version
    1. Usage
    2. Auflistung der Module und Pakete 
2. Englische Version

# German Version
## Auflistung der Module und Pakete
### Module
* *main.py*  
  Dies ist das Main Modul. Es kann mit folgenden Paramtern aufgerufen werden: 
    ```
        usage: main.py [-h] [-w WEIGHT] [-e EXPLORATION] [-p PATH] [-l LOGPATH] N radian stepsize

        positional arguments:
          N                     integer - number of nodes to be used
          radian                float within 0 and 360° - radian of a spherical segment in degree
          stepsize              float within 0 and 1 - step size of the adaptive solution generation in percent

        optional arguments:
          -h, --help            show this help message and exit
          -w WEIGHT, --weight WEIGHT
                                float greater or equal to zero - intersection weight in percent of the pointdensity of a spherical segment
          -e EXPLORATION, --exploration EXPLORATION
                                float greater or equal to zero - exploration factor that is mutiplied with the radius to determine how large the distance of the surrounding nodes under      
                                consideration is
          -p PATH, --path PATH  path to the save location (excluding filename)
          -l LOGPATH, --logpath LOGPATH
                                path to the save location of the log file (excluding filename)
    ```
    Beispielaufruf für 6000 Knoten, den Kugelkappenradius 70.6° und die Schrittweite 1 des adaptiven Lösens, wobei die Lösungsdatei im Ordner *sols* gespeichert werden soll:
    ```
        python .\src\main.py 5000 70.6 1 -p .\sols\
    ```
* *setupLogger.py*  
  Dieses Modul stellt den Logger passend ein. Die Logs werden im Ordner .\logs\ gespeichert. Dabei wird für jeden neuen Tag ein neues Logfile nach dem Format dd-mm-jjjj erstellt.
* *solver.py*  
  Dies ist das solve-Modul. Es besitzt lediglich die Funktion *solve* und bietet eine Schnittstelle an, die es ermöglicht, eine Lösung für das Sphere-Covering Problem einer dreidimensionalen Sphäre zu lösen. Hierzu müssen gewisse Parameter passend gewählt werden:
     * *r_deg* - float zwischen 0 und 360, beschreibt den Radius einer Kugelkappe in Grad
     * *N* - int, beschreibt die Anzahl an Knoten, die bei der Diskretisierung genutzt werden sollen.
     * *intersection_weight* - float größer oder gleich 0, beschreibt das Gewicht, mit welchem die Schnittpunkte zwischen zwei Lösungskappen bewertet werden
     * *seperation_step* - float zwischen 0 und 1, beschreibt die Schrittweite des apdaptiven Lösungsverfahrens
     * *solutionFilePath* - string, Pfad inklusive Dateinname, der Lösungsdatei (wird automatisch erstellt)
     * *solution_log_FilePath* - string, Pfad inklusive Dateinname, der Logdatei zur Lösung. Hier wird der Verlauf eines Durchlaufes in einer csv gespeichert (wird automatisch erstellt)
### Pakete

# English Version
