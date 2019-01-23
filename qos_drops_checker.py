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

import re, time, cli
import sys

# Get show interface status output
show_int_status_op = cli.execute('show interface status')

# Find all interfaces that are in up/up state. Look for connected in show interface status output.
up_interfaces_list = re.findall(r"(Gi(\d)\/\d\/\d{1,2}|Te(\d)\/\d\/\d{1,2}).+?connected", show_int_status_op)
if not up_interfaces_list:
    cli.execute("send log" + " No interface is found to be up'")
    exit()

#Determine switch numbers
intf_drop_traffic = []
for up_interface, sw_num_1, sw_num_2 in up_interfaces_list:
    if sw_num_1:
        sw_num = int(sw_num_1)
    elif sw_num_2:
        sw_num = int(sw_num_2)

    # Get raw data - two snapshots	
    snapshot_1 = cli.execute('show platform hard fed sw %d qos queue stats interface %s ' % (sw_num, up_interface))
    time.sleep(2)
    snapshot_2 = cli.execute('show platform hard fed sw %d qos queue stats interface %s ' % (sw_num, up_interface))

    #Check if drops are happening in any queue-threshold by comparing 2 snapshots with 2 secs time interval for the up interfaces
    # Iterate through raw data to compare counters and throw logs as appropriate
    for queue in range(0, 8):
        match_2 = re.search(
            r"Drop Counters[^!]+?(%d)\s+?(\d+)\s+?(\d+)\s+?(\d+)\s+?(\d+)\s+?(\d+)\s+?(\d+)\n" % (queue), snapshot_2)
        match_1 = re.search(
            r"Drop Counters[^!]+?(%d)\s+?(\d+)\s+?(\d+)\s+?(\d+)\s+?(\d+)\s+?(\d+)\s+?(\d+)\n" % (queue), snapshot_1)
        for threshold in range(2, 8):
            if match_2:
                drop_count_2 = int(match_2.group(threshold))
            if match_1:
                drop_count_1 = int(match_1.group(threshold))
            if match_1 and match_2 and drop_count_2 > drop_count_1:
                intf_drop_traffic.append(up_interface)
                if threshold < 5:
                    cli.execute(
                    "send log" + " Drop-Th%d is dropping traffic in queue %d. Drop count is %d. Check 'show platform hard fed sw %d qos queue stats interface %s'" % (
                    threshold - 2, queue, drop_count_2, sw_num, up_interface))
                elif threshold == 5:
                    cli.execute(
                    "send log" + " SBufDrop is incrementing queue %d. Drop count is %d. Check 'show platform hard fed sw %d qos queue stats interface %s'." % (
                    queue, drop_count_2, sw_num, up_interface))
                elif threshold == 6:
                    cli.execute(
                    "send log" + " QebDrop is incrementing in queue %d. Drop count is %d. Check 'show platform hard fed sw %d qos queue stats interface %s'." % (
                    queue, drop_count_2, sw_num, up_interface))
                elif threshold == 7:
                    cli.execute(
                    "send log" + " Qpolicerdrops is incrementing in queue %d. Drop count is %d. Check 'show platform hard fed sw %d qos queue stats interface %s'." % (
                    queue, drop_count_2, sw_num, up_interface))

#if no interface found dropping traffic, throw log
if not intf_drop_traffic:
    cli.execute("send log" + " No drops found for up/up interfaces")
    exit()