from amaranth import *
import enum

class Path(Elaboratable):
	def __init__(self):
		self.i_direction = Signal(16)
		self.i_distance = Signal(16)
		self.i_aim = Signal(signed(16))

		self.o_depth = Signal(64)
		self.o_forward = Signal(64)

	def elaborate(self, platform):
		m = Module()

		with m.If((self.i_direction == Direction['UP'].value)):
			m.d.sync += self.i_aim.eq(self.i_aim - self.i_distance)

		with m.If((self.i_direction == Direction['DOWN'].value)):
			m.d.sync += self.i_aim.eq(self.i_aim + self.i_distance)

		with m.If((self.i_direction == Direction['FORWARD'].value)):
			m.d.sync += [
				self.o_forward.eq(self.o_forward + self.i_distance),
				self.o_depth.eq(self.o_depth + (self.i_aim * self.i_distance))
			]

		return m

class Direction(enum.Enum):
	UP  	= 1
	DOWN    = 2
	FORWARD = 3

from amaranth.sim import *

path = Path()
sim = Simulator(path)

def data():
	with open("input") as f:
		for line in f.read().splitlines():
			parts = line.split()
			direction = Direction[parts[0].upper()]
			distance = parts[1]

			yield path.i_direction.eq(direction.value)
			yield path.i_distance.eq(int(distance))
			yield
		yield
		depth = yield path.o_depth
		forward = yield path.o_forward
		print("{} - {}".format(depth, forward))
		print("{}".format(depth * forward))

sim.add_sync_process(data)
sim.add_clock(1e-9)
with sim.write_vcd("day02.vcd", "day02.gtkw"):
	sim.run()
