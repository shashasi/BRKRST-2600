import re, time, cli
 
# check stack-ports summary
show_cmd = 'show switch stack-ports summary'            
re.search('\d+\/\d+\s+?\w+.*(\d{2,})', show_cmd)
summary_op = cli.execute(show_cmd)
pattern = '(\d+\/\d+)\s+?\w+.*(\d{2,})'
if summary_op:
    for line in summary_op.splitlines():
        link_ok = re.search(pattern, line)
        if link_ok:
            cli.execute("send log" + " Stack port '%s' has %s 'Changes to LinkOK'"%(link_ok.group(1), link_ok.group(2)))
 
# collect switch and its asic count 
show_switch_op = cli.execute('show switch')
stack_numbers = re.findall('[\*|\s](\d+)\s+?(?:Active|Standby|Member)', show_switch_op)
switch_asic_dict = {}
for stack in stack_numbers:
    show_cmd = 'show platform hardware fed switch %s fwd-asic drops exceptions  | count ASIC'%(stack)
    asic_op = cli.execute(show_cmd)
    if asic_op:
        count = re.search('Number of lines which match regexp \= (\d+)', asic_op)
        if count:
            switch_asic_dict.update({stack:count.group(1)})
 
# SDP counter check for non zero count against Tx Fail or Rx Fail
pattern = re.compile(r'(\w+.*)\s+?\d+\s+?(((\d{2,}|[1-9])\s+?\d+\s+(0))|((0)\s+?\d+\s+(\d{2,}|[1-9])))')
for stack in stack_numbers:
    show_cmd = 'show platform software stack-mgr switch %s r0 sdp-counters'%(stack)
    sdp_counter_op = cli.execute(show_cmd)
    if sdp_counter_op:
        for line in sdp_counter_op.splitlines():
            match = pattern.search(line)
            if match:
                message = match.group(1).strip()
                tx_fail = match.group(4)
                rx_fail = match.group(8)
                if not tx_fail:
                    tx_fail = '0'
                if not rx_fail:
                    rx_fail = '0'
                cli.execute("send log" + " '%s' has %s Tx_Fail and %s Rx_Fail counters"%(message, tx_fail, rx_fail))

# Register's snapshot
cmd_list = ['show platform hardware fed switch %s fwd-asic register read register-name SifRacDataCrcErrorCnt asic %s', 'show platform hardware fed switch %s fwd-asic register read register-name SifRacRwCrcErrorCnt asic %s', 'show platform hardware fed switch %s fwd-asic register read register-name SifRacPcsCodeWordErrorCnt asic %s', 'show platform hardware fed switch %s fwd-asic register read register-name SifRacInvalidRingWordCnt asic %s']
 
snapshot = {}
for stack in stack_numbers:
    for asic in range(int(switch_asic_dict[stack])):
        # Loop for 2 snapshot
        for x in range(2):
            snapshot.update({x:[]})
            # collect value for all 4 commands
            for cmd in cmd_list:
                sh_cmd = cmd%(stack, asic)
                output = cli.execute(sh_cmd)
                value = re.search('count\s+?:\s(\w+)',output)
                if value:
                    # check for hex 3+ digits
                    if int(value.group(1), 16) > int('0x99', 16):
                        cli.execute("send log" + " '%s' has '%s' count"%(sh_cmd, value.group(1)))
                    snapshot[x].append((sh_cmd, value.group(1)))
                else:
                    snapshot[x].append([sh_cmd, 'None'])
            # wait for 5 sec and collect again for above 4 commands
            time.sleep(5)
        # compare two snapshot values
        for index, cmd in enumerate(cmd_list):
            if snapshot[1][index][1] and snapshot[0][index][1]:
                if snapshot[1][index][1] > snapshot[0][index][1]:
                    cli.execute("send log" + " '%s' has increased from '%s' to '%s' within 5 seconds"%(snapshot[0][index][0], snapshot[0][index][1], snapshot[1][index][1]

