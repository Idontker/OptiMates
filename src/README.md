# Gliederung / Table of Contents
1. Auflistung der Module und Pakete (Deutsche Version)
    * Module
    * Pakete
3. Listing of modules and packages (English Version)
    * Moduls
    * Packages

# Auflistung der Module und Pakete (Deutsche Version)
## Module
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
## Pakete
* *checker/*: In diesem Paket befindet sich das Modul, welches mit einem Ungleichungssystem fehlende Punkte einsammelt und eine gegebene Lösung verifiziert.
* *geometrics/*: In diesem Paket befindet sich alle Module, die eine geometrische Komponente besitzten. Dazu gehören die unterschiedlichen Diskretisierungsverfahren für eine Kugel oder auch das Modul zur Bestimmung der Schnittpunkte dreier Sphären.

# Listing of modules and packages (English Version)
## Moduls
* *main.py*  
    This is the main module. It can be called with the following parameters: 
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
       
    Example call for 6000 nodes, spherical cap radius 70.6° and step size 1 of adaptive solving, with the solution file to be saved in the *sols* folder:
    ```
        python .\src\main.py 5000 70.6 1 -p .\sols\
    ```
* *setupLogger.py*  
  This module sets the logger appropriately. The logs are saved in the folder .\logs\. A new log file is created for each new day in the format dd-mm-yyyy.
* *solver.py*  
  This is the solve module. It only has the function *solve* and offers an interface that makes it possible to solve the sphere-covering problem of a three-dimensional sphere. For this, certain parameters have to be chosen appropriately:
     * *r_deg* - float between 0 and 360, describes the radius of a sphere cap in degrees.
     *N* - int, describes the number of nodes to be used in the discretisation.
     * *intersection_weight* - float greater than or equal to 0, describes the weight with which the intersection points between two solution caps are evaluated.
     * *seperation_step* - float between 0 and 1, describes the step size of the apdaptive solution procedure
     * *solutionFilePath* - string, path including file name, of the solution file (will be created automatically)
     * *solution_log_FilePath* - string, path including filename, of the solution log file. Here the history of a run is saved in a csv (is created automatically). 
## Packages
* *checker/*: This package contains the module that collects missing points with a system of inequalities and verifies a given solution.
* *geometrics/*: This package contains all modules that have a geometric component. These include the different discretisation methods for a sphere or the module for determining the intersection points of three spheres.

