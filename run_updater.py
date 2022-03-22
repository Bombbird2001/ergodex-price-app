import subprocess
import time
import os
from datetime import datetime, timezone

updatePeriod = 300 # Updates once every ~5 minutes (excluding time it takes to get data from PSQL server, pushing to Github)
repo_branch = "main" # The branch to push the data changes to

while True:
	data_get = False
	lu_changed = False
	lu_set = False
	added = False
	committed = False
	timeNow = datetime.now(timezone.utc).strftime("%d %B %Y, %H:%M:%S UTC") # Gets the time of update
	try:
		branch = subprocess.check_output(["git", "branch", "--show-current"]).decode("utf-8").strip()
		if branch != repo_branch.strip():
			print("Current branch \"" + branch + "\" does not match output branch \"" + repo_branch + "\" in this file")
			print("Program will now terminate")\
			break
		subprocess.run("get-price-csv_windows.cmd") if os.name == 'nt' else subprocess.run("get-price-csv.sh")
		print("Price data retrieved")
		data_get = True
		with open("last_updated.txt", "w+") as lu:
			lu.write(timeNow)
			lu_changed = True
		subprocess.run(["git", "add", "last_updated.txt"])
		print("Last updated time staged")
		lu_set = True
		subprocess.run(["git", "add", "price-data.csv"])
		print("Price data staged")
		added = True
		subprocess.run(["git", "commit", "-m", "Auto-updated price data at " + timeNow])
		print("Changes committed")
		committed = True
		subprocess.run(["git", "push", "origin", repo_branch])
		print("Commit pushed to origin:" + repo_branch)
		data_get = lu_changed = lu_set = added = committed = False
		print("------------------------------------------------------------------------------")
		time.sleep(updatePeriod)
	except KeyboardInterrupt:
		print("Shutting down...")
		if not data_get:
			break
		# Finish uncompleted steps if in the middle of an update
		if not lu_changed:
			with open("last_updated.txt", "w+") as lu:
				lu.write(timeNow)
		if not lu_set:
			subprocess.run(["git", "add", "last_updated.txt"])
			print("Cleanup: Last updated time staged")
		if not added:
			subprocess.run(["git", "add", "price-data.csv"])
			print("Cleanup: Price data staged")
		if not committed:
			subprocess.run(["git", "commit", "-m", "Auto-updated price data at " + timeNow])
			print("Cleanup: Changes committed")
		subprocess.run(["git", "push", "origin", repo_branch])
		print("Cleanup: Commit pushed to origin:" + repo_branch)
		break