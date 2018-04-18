import subprocess

class ResourceManager:
    def __init__(self):
        pass

    def executeLambda(self):
        copy = subprocess.check_output(
            "scp -o LogLevel=quiet -o StrictHostKeyChecking=no /tmp/function1.py " + "ec2-user@ec2-52-23-174-4.compute-1.amazonaws.com" + ":~", shell=True)
        perm = subprocess.check_output("ssh -o LogLevel=quiet -o StrictHostKeyChecking=no " + "ec2-user@ec2-52-23-174-4.compute-1.amazonaws.com" + " 'chmod 711 ~/function1.py'", shell=True)
        run = subprocess.check_output("ssh -o LogLevel=quiet -o StrictHostKeyChecking=no " + "ec2-user@ec2-52-23-174-4.compute-1.amazonaws.com" + " '" + "DISPLAY=:0 python function1.py >function1.log" + "'", shell=True)
        "deployed and executed"

resourceManager = ResourceManager()
resourceManager.executeLambda()