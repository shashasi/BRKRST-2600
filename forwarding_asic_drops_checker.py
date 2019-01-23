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
#show platform hard fed sw active fwd-asic drop exceptions

sh_drop_exceptions = cli.execute('show platform hard fed sw active fwd-asic drop exceptions')

#Checking for non zero value against any field in delta column.
#Ignoring rows NO_EXCEPTION PKT_DROP_COUNT BLOCK_FORWARD these rows as they are seen to increment without any issue too 

non_zero_values_delta = re.findall(r"\d+?\s+?\d+?\s+?(\S+?)\s+?\d+?\s+?\d+?\s+?([1-9]\d*?)\s", sh_drop_exceptions)
non_zero = 0
if non_zero_values_delta:
    for name, non_zero_delta in non_zero_values_delta:
        if str(name) != "NO_EXCEPTION" and str(name) != "PKT_DROP_COUNT" and str(name) != "BLOCK_FORWARD":
            non_zero =1
            cli.execute("send log" + " Non zero delta value %s found for %s. Check 'show platform hard fed sw active fwd-asic drop exceptions'" % (non_zero_delta, name))
            
#If not non zero  delta values found generating no problem found alert.   
if not non_zero:
    cli.execute("send log" + " No problem found")
   
       

				



    