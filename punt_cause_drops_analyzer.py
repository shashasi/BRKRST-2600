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
import re,time,cli
import sys

#Get output for following commands
#(a)sh platform software fed sw active punt cause summary
#(b)sh platform hardware fed switch active qos queue stats internal cpu policer 
#(c)sh platform software fed sw active punt cpuq all 

sh_sw_punt_cause = cli.execute('show platform software fed switch active punt cause summary')
sh_sw_cpu_policer = cli.execute('show platform hardware fed switch active qos queue stats internal cpu policer')
sh_sw_punt_cpuq = cli.execute('show platform software fed switch active punt cpuq all')

#Look for any non zero Dropped count. If found generate alert along with the Cause Info and corresponding non zero field.
non_zero_values_punt_cause = re.findall(r"\n\d+?\s+?(\S+?.*?)\s+?\d+?\s+?([1-9][0-9]*?)\s+?\n", sh_sw_punt_cause)
if non_zero_values_punt_cause:
    for cause, non_zero in non_zero_values_punt_cause:
        cli.execute("send log" + " Drop found %s, cause info %s. Check 'show platform software fed switch active punt cause summary'" % (non_zero, cause))
       
#Look for any cpu policer queue dropping packets. If found generate alert along with the queue and corresponding non zero field.
cpu_int_queue = re.findall(r"\d+?\s+?\d+?\s+(.+?)\s+Yes.+?(\d+?)\s+?\n", sh_sw_cpu_policer)
if cpu_int_queue:
    for queue, dropped in cpu_int_queue:
        if int(dropped) > 0:
        	cli.execute("send log" + " Non zero value %s found for %s. Check 'show platform hardware fed switch active qos queue stats internal cpu policer'" % (dropped, queue))
else:
    cli.execute("send log" + " No queue found dropping any packets")
            
#looking for any non zero count following fields - 
#Send to IOSd failed count      
#RX suspend count
#RX unsuspend send failed count 
#RX dropped count               
#RX non-active dropped count    
#RX conversion failure dropped  
#RX spurious interrupt
      
punt_cpuq = 0
non_zero_values_punt_cpuq = re.findall(r"(CPU Q Id\s+?\: (\d{1,})(?:(?!(?:CPU Q Id))[\s\S])*)", sh_sw_punt_cpuq)
if non_zero_values_punt_cpuq:
   for cpq_entry, cpu_q_id in non_zero_values_punt_cpuq:
       match = re.findall(r"(Send to IOSd failed count|RX suspend count|RX unsuspend send failed count|RX dropped count|RX non-active dropped count|RX conversion failure dropped|RX spurious interrupt)\s+?\: ([1-9][0-9]{0,})", cpq_entry)
       if match:
          punt_cpuq = 1
          for field, non_zero_value in match:
                cli.execute("send log" + " Non zero value %s found for %s - CPU Q ID %s. Check 'show platform software fed switch active punt cpuq all'" % (non_zero_value, field, cpu_q_id))

        
#If no drops are found, generating no problem found alert.   
if not non_zero_values_punt_cause and not punt_cpuq:
   cli.execute("send log" + " No problem found")
    