def getObs(idx):
		curr = 0
		with open("log.txt") as log:
			for action in log:
				if curr == idx:
					return [action.split(" ")[i] for i in range(8)]
				curr += 1
                