from amaranth import *

class Sonar(Elaboratable):
	def __init__(self):
		self.i_incr = Signal()	
		self.i_signal = Signal(16)

		self.o_result = Signal(16)

	def elaborate(self, platform):
		m = Module()
		last = Signal(16)

		with m.If((self.i_signal > last) & self.i_incr):
			m.d.sync += self.o_result.eq(self.o_result + 1)

		m.d.sync += last.eq(self.i_signal)

		return m

from amaranth.sim import *

sonar = Sonar()
sim = Simulator(sonar)

def incr():
	yield sonar.i_incr.eq(0)
	yield
	yield sonar.i_incr.eq(1)
	yield

def data():
	with open("input") as f:
		for line in f.read().splitlines():
			yield sonar.i_signal.eq(int(line))
			yield
		yield
		result = yield sonar.o_result
		print("{}".format(result))

sim.add_sync_process(incr)
sim.add_sync_process(data)
sim.add_clock(1e-9)
sim.run()
