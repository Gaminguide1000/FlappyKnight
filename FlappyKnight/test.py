import subprocess

#Check for Updates
update_file = "udpater.py"
result = subprocess.run(["python", update_file], capture_output=True, text=True)
print(result)