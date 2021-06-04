import sys
import gurobipy
import math
import numpy as np

# Lies die Lösungsdatei ein und gib eine Liste der Mittelpunkte zurück
# solutionFilePath = Pfad zur Lösungsdatei (string)
# n = Dimension der Kugel (int, >= 1)
def readSolution(solutionFilePath, n=3):
	solution = []
	try:
		# Öffne die Lösungsdatei und lies die Lösung ein
		with open(solutionFilePath) as solutionFile:
			# Lies die Lösungsdatei zeilenweise,
			# konvertiere jede Zeile zu einem Koordinatentupel
			# und speichere die Koordinatentupel in der Liste solution ab
			for line in solutionFile:
				entries = line.split(';')
				try:
					solution.append(tuple(entries[i] for i in range(n)))
				except:
					print(f'Ungültige Zeile: {line}')
	except:
		print(f'Konnte die Datei {solutionFilePath} nicht öffnen.')
		sys.exit(-1)
		
	return solution

# Überprüfe die übergebene Liste von Mittelpunkten,
# ob die dort zentrierten Kappen die Sphäre vollständig überdecken
# solution = Liste der Mittelpunkte der Kappen (List[tuple(n)])
# alpha = Öffnungswinkel der Kappen (float, >= 0, <= 360)
# n = Dimension der Kugel (int, >= 1)
def checkSolution(solution, alpha, n=3, printing=True):
	# Erzeuge ein Gurobi-Modell um zu überprüfen,
	# ob die Überdeckung vollständig ist
	# (Annahme: die Kappen sind "offen")
	model = gurobipy.Model()
	
	# Deaktiviere die Gurobi-Ausgabe
	model.setParam('OutputFlag', 0)
	
	# Aktiviere den nicht-konvexen Löser
	model.setParam('NonConvex', 2)
	
	# Erzeuge die Variablen und Nebenbedingungen
	
	# Die y-Variablen kodieren den gesuchten unüberdeckten Punkt
	y = {}
	for i in range(n):
		y[i] = model.addVar(lb=-gurobipy.GRB.INFINITY, ub=gurobipy.GRB.INFINITY, vtype=gurobipy.GRB.CONTINUOUS, name = f'y{i}')
	
	# Der Punkt muss auf der Sphäre liegen, also eine 2-Norm von Wert 1 haben.
	model.addQConstr(gurobipy.quicksum(y[i] * y[i] for i in range(n)) == 1, 'Norm')
	
	# Der Punkt darf von keiner Kappe in der übergebenen Lösung überdeckt werden
	for j in range(len(solution)):
		x = solution[j]
		model.addConstr(gurobipy.quicksum(x[i] * y[i] for i in range(n)) <= math.cos((0.5 * alpha) / 180 * math.pi), f'Angle{j}')
		
	# Schreibe zum Debuggen eine LP-Datei heraus
	#model.write("Lösung.lp")
	
	# Löse das Modell und entscheide an Hand des Zulässigkeitsstatus,
	# ob die Überdeckung vollständig
	model.optimize()
	if model.status == 2:
		if printing:
			print('Die Überdeckung ist nicht vollständig.\nDer folgende Punkt ist nicht überdeckt:')
		arr = np.array([0.0,0.0,0.0])
		
		for i in range(n):
			if printing:
				print(f'y{i} = ', y[i].X)
			arr[i] = y[i].X
		return arr

	else:
		print('Die Überdeckung ist vollständig.')
		
if __name__ == '__main__':
	try:
		# Lies den Pfad zur Lösungsdatei ein
		solutionFilePath = sys.argv[1]
		
		# Lies den Öffnungwinkel der Kappen ein
		alpha = float(sys.argv[2])
	# Falls keine korrekten Parameter übergeben wurden,
	# gib den Benutzungshinweis aus und schließe das Programm
	except:
		print('Verwendung: ./checker.py {Lösungsdatei} {Öffnungswinkel}')
		sys.exit(-1)
		
	# Lies die Lösung ein
	solution = readSolution(solutionFilePath)
	
	# Überprüfe die Lösung
	checkSolution(solution, alpha)

