#!/usr/bin/env python3

import m5
from m5.objects import (
    System,
    SrcClockDomain,
    VoltageDomain,
    AddrRange,
    Cache,
    L2XBar,
    SystemXBar,
    MemCtrl,
    DDR3_1600_8x8,
    TimingSimpleCPU,
    DerivO3CPU,
    MinorCPU,
    SEWorkload,
    Process,
    Root,
    StridePrefetcher,
)
import m5.stats as stats
import argparse

# -----------------------------
# Argument parsing
# -----------------------------
parser = argparse.ArgumentParser(description="gem5 cache exploration ")
parser.add_argument(
    "--cpu-type",
    choices=["TimingSimpleCPU", "DerivO3CPU", "MinorCPU"],
    default="TimingSimpleCPU",
    help="Type of CPU model to simulate",
)
parser.add_argument(
    "--num-cpus", type=int, default=1, help="Number of CPU cores (shares L2)"
)
parser.add_argument(
    "--l1-size", type=str, default="32kB", help="Size of each private L1 cache"
)
parser.add_argument(
    "--l1-assoc", type=int, default=2, help="Associativity of L1 caches"
)
parser.add_argument(
    "--block-size",
    type=int,
    default=64,
    help="Cache line size in bytes (global)",
)
parser.add_argument(
    "--l2-size", type=str, default="256kB", help="Size of the shared L2 cache"
)
parser.add_argument(
    "--l2-assoc", type=int, default=8, help="Associativity of the L2 cache"
)
parser.add_argument(
    "--prefetcher",
    choices=["None", "StridePrefetcher"],
    default="None",
    help="Type of L1 prefetcher (if any)",
)
parser.add_argument(
    "--cmd",
    type=str,
    default="/home/sphoo/gem5/configs/example/add",
    help="Path to the workload binary to execute",
)
args = parser.parse_args()

# -----------------------------
# System configuration
# -----------------------------
system = System()
system.clk_domain = SrcClockDomain(
    clock="1GHz", voltage_domain=VoltageDomain()
)
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("1GB")]
# Global cache line size
system.cache_line_size = args.block_size

# SE-mode workload setup
process = Process()
process.cmd = [args.cmd]
system.workload = SEWorkload.init_compatible(args.cmd)

# Create CPU cores
cpu_cls = {
    "TimingSimpleCPU": TimingSimpleCPU,
    "DerivO3CPU": DerivO3CPU,
    "MinorCPU": MinorCPU,
}[args.cpu_type]
cpus = [cpu_cls() for _ in range(args.num_cpus)]
system.cpu = cpus

# Assign Process workload to each CPU and threads
for cpu in cpus:
    # Attach same workload
    cpu.workload = process
    cpu.createThreads()

# Cache creation helper
def make_cache(size, assoc, prefetch):
    c = Cache()
    c.size = size
    c.assoc = assoc
    c.tag_latency = 2
    c.data_latency = 2
    c.response_latency = 2
    c.mshrs = 4
    c.tgts_per_mshr = 20
    if prefetch == "StridePrefetcher":
        c.prefetcher = StridePrefetcher()
    return c


# Instantiate L1 I/D per CPU
for cpu in cpus:
    ic = make_cache(args.l1_size, args.l1_assoc, args.prefetcher)
    dc = make_cache(args.l1_size, args.l1_assoc, args.prefetcher)
    cpu.icache = ic
    cpu.dcache = dc
    cpu.icache.cpu_side = cpu.icache_port
    cpu.dcache.cpu_side = cpu.dcache_port

# Shared L2 bus and cache
system.l2bus = L2XBar()
system.l2cache = make_cache(args.l2_size, args.l2_assoc, "None")
for cpu in cpus:
    cpu.icache.mem_side = system.l2bus.cpu_side_ports
    cpu.dcache.mem_side = system.l2bus.cpu_side_ports
system.l2cache.cpu_side = system.l2bus.mem_side_ports

# Memory bus & DRAM
system.membus = SystemXBar()
system.l2cache.mem_side = system.membus.cpu_side_ports
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Interrupt controller setup for X86
for cpu in cpus:
    cpu.createInterruptController()
    intr = cpu.interrupts[0]
    intr.pio = system.membus.mem_side_ports
    intr.int_requestor = system.membus.cpu_side_ports
    intr.int_responder = system.membus.mem_side_ports

# System port
system.system_port = system.membus.cpu_side_ports

# Instantiate & launch
root = Root(full_system=False, system=system)
m5.instantiate()
stats.reset()
print(
    f"Running {args.cpu_type} x {args.num_cpus}, L1={args.l1_size}/{args.l1_assoc}, "
    f"L2={args.l2_size}/{args.l2_assoc}, line={args.block_size}B, pf={args.prefetcher}"
)
event = m5.simulate()
print(f"Exited @ tick {m5.curTick()} because {event.getCause()}")
stats.dump()
