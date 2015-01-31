from measurement.utils import guess

def convert_weight_to_oz(weight, unit):
	weight = guess(weight, unit)

	return weight.oz