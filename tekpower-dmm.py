from serial import Serial

BAUD = 2400
DATA_BITS = 8
PARITY = False
STOP_BITS = 1
FLOW_CONTROL = False


class TekReader:
	def __init__(self,port):
		self.serial = Serial(port,BAUD,DATA_BITS,PARITY,STOP_BITS)
		self.data = bytes([0,0,0,0,0,0,0,0,0,0,0,0,0,0]) # fourteen 0's
	
	@staticmethod
	def seven_seg_to_float(digits):
		def convert_digit(d):
			extra = False
			out = 0
			if d > 128:
				d -= 128
				extra = True

			if d == 0b0000101:
				out = 1
			elif d == 0b1011011:
				out = 2
			elif d == 0b0011111:
				out = 3
			elif d == 0b0100111:
				out = 4
			elif d == 0b0111110:
				out = 5
			elif d == 0b1111110:
				out = 6
			elif d == 0b0010101:
				out = 7
			elif d == 0b1111111:
				out = 8
			elif d == 0b0111111:
				out = 9

			return (extra,out)

		neg = 1
		n = 0.0

		extras,digits = zip(*map(convert_digit, digits))
		if extras[0]:
			neg = -1

		for digit in digits:
			n *= 10
			n += digit

		dps = 0
		for i,dp in enumerate(extras[1:].reverse):
			if dp:
				dps = i+1
				break
		n *= 10 ** ( -1 * dps )
		return n*neg

	@staticmethod
	def parse_byte(b):
		i = (b >> 4)-1
		v = b & 7
		return i,v

	def _read_row(self):
		first, = self.serial.read(1)
		i,v = self.parse_byte(first)
		if i == 0:
			return [v] + [self.parse_byte(b)[1] for b in self.serial.read(13)]
		else:
			self.serial.read(13 - i)
			return [self.parse_byte(b)[1] for b in self.serial.read(14)]
	
	
				
				

		

if __name__ == "__main__":
	print("derp")
