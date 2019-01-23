# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
#THIS SCRIPT IS DESIGNED TO BE RUN FROM AN EXTERNAL MACHINE HAVING TELNET ACCESS TO NETWORK DEVICES.

#=============== 
#READ-ME
#=============== 
#Write and save IP Addresses of network devices in IP_Address.txt in same dir as this script, one in each line
#Write and save new config that needs to be pushed to network devices defined above in startup-config.txt in same dir as this script
#=============== 

import sys
import telnetlib,time

#Pass username and password as variables while running the script
user = sys.argv[1]
password = sys.argv[2]
#Privilege level 15 set for this user so enable pwd is not needed

#Load IP addresses of devices
with open("IP_Address.txt", "r") as object_1:
    IP = []
    for object in object_1:
        IP.append(object.rstrip())
        
#Load startup-config
with open("startup-config.txt", "r") as object_2:
    START_UP = []
    for object in object_2:
        START_UP.append(object.rstrip())    

#Copy configuration            	
def copy_start(tn):
	tn.write("conf t\r")
	time.sleep(0.1)
	print ("In config mode. Writing config now..")
	time.sleep(2)
	for line in START_UP:
		tn.write(line + "\r")
		print line
		time.sleep(0.05)
		
#iterate through IPs, telnet and call copy_start()
for ip in IP:
	tn = telnetlib.Telnet(ip)
	tn.read_until("Username:")
	tn.write(user + "\n")
	tn.read_until("Password:")
	tn.write(password + "\n")
	tn.read_until("#")
	copy_start(tn)
	tn.write("wr\n")
	tn.close()