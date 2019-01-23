
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

import cli,time

cli.execute("en")
cli.execute("del flash:gs_script/*")
cli.execute("monitor capture tac_cpu interface G1/0/1 both match any file location flash:/gs_script/tac-cpu.pcap")
cli.execute("monitor capture tac_cpu start")
time.sleep(5)
cli.execute("monitor capture tac_cpu stop")
cli.execute("show proc cpu sort | append flash:/gs_script/tac-cpu.txt")
cli.execute("show proc cpu hist | append flash:/gs_script/tac-cpu.txt")
cli.execute("show proc cpu platform sorted | append flash:/gs_script/tac-cpu.txt")
cli.execute("show interface | append flash:/gs_script/tac-cpu.txt")
cli.execute("show interface stats | append flash:/gs_script/tac-cpu.txt")
cli.execute("show log | append flash:/gs_script/tac-cpu.txt")
cli.execute("show ip traffic | append flash:/gs_script/tac-cpu.txt")
cli.execute("show users | append flash:/gs_script/tac-cpu.txt")
cli.execute("show platform software fed switch active punt cause summary | append flash:/gs_script/tac-cpu.txt")
cli.execute("show platform software fed switch active cpu-interface | append flash:/gs_script/tac-cpu.txt")
cli.execute("show platform software fed switch active punt cpuq all | append flash:/gs_script/tac-cpu.txt")



