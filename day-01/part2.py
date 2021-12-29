from amaranth import *

class Sonar(Elaboratable):
	def __init__(self):
		self.i_incr = Signal()

		self.i_signal = Signal(16)
		self.o_result = Signal(16)

	def elaborate(self, platform):
		m = Module()

		last1 = Signal(16)
		last2 = Signal(16)
		last3 = Signal(16)
		test = Signal()

		with m.If(((self.i_signal + last1 + last2) > (last1 + last2 + last3)) & self.i_incr):
			m.d.sync += [
				self.o_result.eq(self.o_result + 1),
				test.eq(1)
			]

		m.d.sync += [
			last3.eq(last2),
			last2.eq(last1),
			last1.eq(self.i_signal)
		]

		return m

from amaranth.sim import *

sonar = Sonar()
sim = Simulator(sonar)

def incr():
	yield sonar.i_incr.eq(0)
	yield
	yield
	yield
	yield sonar.i_incr.eq(1)
	yield

def data():
	with open("input") as f:
		for line in f.read().splitlines():
			yield sonar.i_signal.eq(int(line))
			yield
		yield sonar.i_incr.eq(0)
		yield
		result = yield sonar.o_result
		print("{}".format(result))

sim.add_sync_process(incr)
sim.add_sync_process(data)
sim.add_clock(1e-9)
with sim.write_vcd("test.vcd", "test.gtkw"):
	sim.run()
