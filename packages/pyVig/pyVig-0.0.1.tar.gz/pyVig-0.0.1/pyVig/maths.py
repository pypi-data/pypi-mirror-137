import numpy as np



def df_with_slops_and_angles(df, x1_col, x2_col, y1_col, y2_col):
	df['slop'] = (df[y2_col] - df[y1_col])/(df[x2_col] - df[x1_col])
	df = df.fillna("")
	df['angle_angled_connector'] = df.slop.apply(slop_to_angled_connector)
	df['angle_straight_connector'] = df.slop.apply(slop_to_straight_connector)
	return df.fillna("")


def slop_to_straight_connector(m):
	if not m: return 0
	angle = int(np.math.degrees(np.math.tanh(m)))
	if angle < 0: angle = 90+angle
	if m < 0: angle = 360-angle 
	return angle

def slop_to_angled_connector(m):
	if not m: return 0
	angle = int(np.math.degrees(np.math.tanh(m)))
	if angle < 0: angle = 180-angle
	if m > 0: angle = 360-angle 
	return angle
