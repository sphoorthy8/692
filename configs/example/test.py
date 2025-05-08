#!/usr/bin/env python3

import m5
from m5.objects import *
import m5.stats as stats


class L1ICache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20
    size = "32kB"


class L1DCache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20
    size = "32kB"


class L2Cache(Cache):
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12
    size = "256kB"


system = System()
system.clk_domain = SrcClockDomain(
    clock="1GHz", voltage_domain=VoltageDomain()
)
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("128MB")]

system.cpu = TimingSimpleCPU()

binary = "/home/sphoo/gem5/configs/example/hello"
system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()
system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.dcache.cpu_side = system.cpu.dcache_port

system.l2bus = L2XBar()
system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports

system.l2cache = L2Cache()
system.l2cache.cpu_side = system.l2bus.mem_side_ports

system.membus = SystemXBar()
system.l2cache.mem_side = system.membus.cpu_side_ports

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

root = Root(full_system=False, system=system)
m5.instantiate()
stats.reset()

print("Starting simulation!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")

stats.dump()
