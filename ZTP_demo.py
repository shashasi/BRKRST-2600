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
# Importing cli module
import cli,re

print "\n\n *** ZTP Python Script *** \n\n"

#Define credentials for ZTP switch
user = "cisco"
password = "cisco"
enable = "cisco"

#Configure hostname on ZTP switch
print "\n\n *** Configuring hostname *** \n\n"
cli.configurep(["hostname ZTP-Switch", "end"])

#Configure credentials on ZTP switch
print "\n\n *** Configuring credentials *** \n\n"
cli.configurep(['username {} privilege 15 password {}'.format(user, password)]) 
cli.configurep(['enable secret {}'.format(enable)])

#Configure telnet and ssh on ZTP switch
print "\n\n *** Configuring telnet & ssh *** \n\n"
cli.configurep(['line vty 0 4', 'login local', 'transport input telnet ssh'])

#get show interface status output from ZTP switch
list = cli.execute('show interface status')

#Find all 1G ports
gig_ports = re.findall(r"(Gi\d\/\d\/\d{1,2}).+?connect", list)
#Configure all gig ports as access ports in vlan 10
for gig_port in gig_ports:
        print '\n\n Configuring interface {} as access port in vlan 10'.format(gig_port)
        cli.configurep(['int {}'.format(gig_port), 'switchport mode access', 'switchport access vlan 10', 'description configured by python'])

#Find all 10G ports        
TenG_ports = re.findall(r"(Te\d\/\d\/\d{1,2}).+?connect", list)
#Configure all 10G ports as trunk ports
for TenG_port in TenG_ports:
    print '\n\n Configuring interface {} as trunk port'.format(TenG_port)
    cli.configurep(['int {}'.format(TenG_port), 'switchport mode trunk', 'description configured by python'])
                        
print "\n\n *** ZTP Python Script Execution Complete *** \n\n"