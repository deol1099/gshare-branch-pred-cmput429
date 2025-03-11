# Copyright (c) 1990-2010, Ayrton Chilibeck.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# Neither the name of the Ayrton Chilibeck nor the names of its contributors may be
# used to endorse or promote products derived from this software without specific
# prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# Invoke using `gem5 P550SystemSingleSim.py`
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource,BinaryResource
from gem5.resources.downloader import list_resources
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires

from m5.objects import *

#####
# Needed for local imports since gem5 takes our file
#  and executes it in the context of the multisim module
import sys
import os

thispath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(thispath)
######

# Parse command-line arguments for predictor type and workload.
if len(sys.argv) < 3:
    print("Usage: {} <predictor_type: gshare or perceptron> <workload: mcf, gcc1, gcc2>".format(sys.argv[0]))
    sys.exit(1)

predictor_type = sys.argv[1]
workload_type = sys.argv[2]

if predictor_type not in ["gshare", "perceptron"]:
    print("Invalid predictor type. Choose either 'gshare' or 'perceptron'.")
    sys.exit(1)

if workload_type == "mcf":
    workload_resource = "riscv-spec-mcf-run-se"
elif workload_type == "gcc1":
    workload_resource = "riscv-spec-gcc-mcf-run-se"
elif workload_type == "gcc2":
    workload_resource = "riscv-spec-gcc-lbm-run-se"
else:
    print("Invalid workload. Choose one of: mcf, gcc1, gcc2.")
    sys.exit(1)

from P550Caches import *
from P550Processor import *

# This check ensures the gem5 binary is compiled to the RISCV ISA target. If not,
# an exception will be thrown.
requires(isa_required=ISA.RISCV)

# We can run multiple simulations at once
# Be careful of running out of memory!
# NOTE: this only sets the max number
#  of processes to run at once, not
#  the maximum number of sims you can run

# We use the P550 processor with one core.
#  see the P550Processor.py file
#  TODO Create your processor and add it to this list
processor = P550Processor(num_cores=1, predictor=predictor_type)  # perceptron, gshare

# We use the P550 Cache system
#  see P550Caches.py
cache_hierarchy = P550CacheHierarchy()

# We use a single channel DDR3_1600 memory system
memory = SingleChannelDDR3_1600(size="8GiB")

# The gem5 library simble board which can be used to run simple SE-mode
# simulations.
board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# Set the board workload to our workload
# board.set_workload(obtain_resource("riscv-spec-mcf-run-se"))
# board.set_workload(obtain_resource("riscv-spec-gcc-mcf-run-se"))
board.set_workload(obtain_resource(workload_resource))

simulator = Simulator(board=board)

simulator.run()

