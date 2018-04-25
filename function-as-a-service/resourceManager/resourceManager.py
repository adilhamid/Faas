import subprocess
import sys
sys.path.append("..")
from util.config import Config

class ResourceManager:
    def __init__(self):
        self.configObj = Config()

    def create_directory(self, host, path):
        creatDir = "ssh " + host +" 'mkdir -p " + path+"'"
        try:
            print creatDir
            copy = subprocess.check_output(creatDir, shell=True)
        except:
            e = sys.exc_info()[0]
            print "Exception occured ",
            print e


    def executeLambda(self, path, functionName):

        # Since we have one instance only, running the command on the single instance
        functionPath = path + functionName + ".py"
        instancePath  = "/home/ec2-user/functionDir/"

        # Check if the file path exists in the instance machine
        self.create_directory(self.configObj.INSTANCE, instancePath )

        copyCommand = "scp -o LogLevel=quiet -o StrictHostKeyChecking=no " + functionPath + " " + self.configObj.INSTANCE + ":" + instancePath

        permissionCommand = "ssh -o LogLevel=quiet -o StrictHostKeyChecking=no " + self.configObj.INSTANCE + " 'chmod 711 " + instancePath+functionName + ".py'"

        runCommand = "ssh -o LogLevel=quiet -o StrictHostKeyChecking=no " + self.configObj.INSTANCE + " 'DISPLAY=:0 python "+ instancePath + functionName + ".py > "+ instancePath + functionName + ".log'"

        copyLogBack = "scp -o LogLevel=quiet -o StrictHostKeyChecking=no " + self.configObj.INSTANCE + ":" + instancePath+ functionName + ".log " + path + functionName + ".log"

        try:
            print copyCommand
            copy = subprocess.check_output(copyCommand, shell=True)

            print permissionCommand
            perm = subprocess.check_output(permissionCommand, shell=True)

            print runCommand
            run = subprocess.check_output(runCommand, shell=True)

            print copyLogBack
            copyBack = subprocess.check_output(copyLogBack, shell = True)

            resultData = open(path+functionName+".log", 'r').read()

            print "\nThe result obtained by running function is : "+ resultData

            print "Deployed an Executed Successfully"

            return resultData

        except:
            e = sys.exc_info()[0]
            print "Exception occured ",
            print e


if __name__ == "__main__":
    obj = ResourceManager()
    obj.create_directory(obj.configObj.INSTANCE ,"/home/ec2-user/functionDir/")