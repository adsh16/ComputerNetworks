import xml.etree.ElementTree as ET



# Load the XML file

tree = ET.parse("flow-monitor-output.xml")

root = tree.getroot()



# Extract metrics

flows = root.findall(".//FlowStats/Flow")



print(f"{'Flow ID':<10} {'TxPackets':<10} {'RxPackets':<10} {'LostPackets':<12} {'DelaySum (ns)':<15} {'AvgDelay (ns)':<15} {'DropRate (%)':<12}")

print("-" * 80)



for flow in flows:

    flow_id = flow.get("flowId")

    tx_packets = int(flow.get("txPackets"))

    rx_packets = int(flow.get("rxPackets"))

    lost_packets = int(flow.get("lostPackets"))

    delay_sum_str = flow.get("delaySum")

    delay_sum = float(delay_sum_str.rstrip("ns"))  # Remove 'ns' and convert to float

    avg_delay = delay_sum / rx_packets if rx_packets > 0 else 0

    drop_rate = (lost_packets / tx_packets) * 100 if tx_packets > 0 else 0



    # Print flow-level metrics

    print(f"{flow_id:<10} {tx_packets:<10} {rx_packets:<10} {lost_packets:<12} {delay_sum:<15.2f} {avg_delay:<15.2f} {drop_rate:<12.2f}")



    # Extract dropped packets and delays

    dropped_packets = flow.findall(".//packetsDropped")

    delays = flow.findall(".//delayHistogram/bin")

    jitter = flow.findall(".//jitterHistogram/bin")



    # Print details about dropped packets

    if dropped_packets:

        print(f"  Dropped Packets Details:")

        for drop in dropped_packets:

            reason_code = drop.get("reasonCode")

            number = int(drop.get("number"))

            print(f"    Reason Code {reason_code}: {number} packets dropped")



    # Print delay histogram details for packets

    if delays:

        print(f"  Delay Histogram Details:")

        for delay in delays:

            start = delay.get("start")

            count = int(delay.get("count"))

            print(f"    Delay: {start}ns, Count: {count} packets")



    # Print jitter histogram details

    if jitter:

        print(f"  Jitter Histogram Details:")

        for j in jitter:

            start = j.get("start")

            count = int(j.get("count"))

            print(f"    Jitter: {start}ns, Count: {count} packets")

    

    print("-" * 80)

