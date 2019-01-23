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
import cli,time,sys

#Format current time to obtain a unique string for filename & develop a path name using that
timestamp = time.strftime('%b-%d-%Y_%H%M%S', time.localtime())
PATH_NAME = ("flash:/gs_script/" + timestamp + ".pcap")

#Pass interface name as runtime variable 
INTERFACE_NAME = str(sys.argv[1])

#Start and stop capture
cli.execute("enable")
cli.execute("no monitor capture pack_cap")
cli.execute("monitor capture pack_cap interface %s in file location %s size 10 match any" % (INTERFACE_NAME, PATH_NAME))
cli.execute("monitor capture pack_cap start")
cli.execute("send log Capture running on %s for 10 sec" %INTERFACE_NAME)
cli.executep("show monitor capture pack_cap")
time.sleep(10)
cli.execute("monitor capture pack_cap stop")
cli.execute("send log Capture saved in %s" %PATH_NAME)
