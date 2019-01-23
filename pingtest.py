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

import re,cli

#Get a copy of the ARP table in Mgmt-vrf
arp_table = cli.execute('show ip arp vrf Mgmt-vrf')
cli.executep('show ip arp vrf Mgmt-vrf')

#Find all IP addresses in the ARP table
hosts = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", arp_table)
if hosts:
    for host in hosts:
    	#ping each IP address
        ping_result = cli.execute("ping vrf Mgmt-vrf %s timeout 1" % host)
        #See if ping was successful
        success = re.findall(r"Success rate is 100 percent", ping_result)
        if success:
        	cli.execute("send log %s is reachable" % host)
        else:
        	cli.execute("send log %s is NOT reachable" % host)
        