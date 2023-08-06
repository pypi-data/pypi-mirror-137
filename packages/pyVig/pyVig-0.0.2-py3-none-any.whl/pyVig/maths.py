import numpy as np



def df_with_slops_and_angles(df, x1_col, x2_col, y1_col, y2_col):
	"""add the dataframe with slop and angle for the given co-ordinates on plane.

	Args:
		df (DataFrame): Input DataFrame
		x1_col (str): column name for point 1 - x axis
		x2_col (str): column name for point 2 - x axis
		y1_col (str): column name for point 1 - y axis
		y2_col (str): column name for point 2 - y axis

	Returns:
		DataFrame: Updated Output DataFrame
	"""	
	df['slop'] = (df[y2_col] - df[y1_col])/(df[x2_col] - df[x1_col])
	df = df.fillna("")
	df['angle_angled_connector'] = df.slop.apply(slop_to_angled_connector)
	df['angle_straight_connector'] = df.slop.apply(slop_to_straight_connector)
	return df.fillna("")


def slop_to_straight_connector(m):
	"""calculate angle from given slop(m) of a straight line.

	Args:
		m (float): slop of a straight line

	Returns:
		int: degree/slop of line
	"""		
	if not m: return 0
	angle = int(np.math.degrees(np.math.tanh(m)))
	if angle < 0: angle = 90+angle
	if m <= 0: angle = 360-angle 
	return angle

def slop_to_angled_connector(m):
	"""calculate angle from given slop(m) of an angled line.

	Args:
		m (float): slop of an angled line

	Returns:
		int: degree/slop of line
	"""		
	if not m: return 0
	angle = int(np.math.degrees(np.math.tanh(m)))
	if angle < 0: angle = 180-angle
	if m > 0: angle = 360-angle 
	return angle
