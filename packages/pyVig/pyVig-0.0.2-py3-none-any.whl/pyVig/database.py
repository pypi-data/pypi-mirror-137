

# -----------------------------------------------------------------------------------
import pandas as pd
# from math import tanh, degrees

from pyVig.maths import df_with_slops_and_angles
# -----------------------------------------------------------------------------------

class Data():
	'''
	Parent class defining device and connectors.
	'''

	def __init__(self, data_file):
		"""Initialize the object

		Args:
			data_file (str): file name of excel database containing devices and cabling details.
		"""		
		self.data_file = data_file

	def read(self, sheet_name):
		"""read data from given excel sheet and set dataframe for the object.

		Args:
			sheet_name (str): Excel sheet name
		"""		
		self.df = pd.read_excel(self.data_file, sheet_name=sheet_name).fillna("")


# -----------------------------------------------------------------------------------


class DeviceData(Data):
	"""Devices Data Object Building
	"""		

	def __init__(self, 
		data_file, 
		sheet_name,
		x="x",
		y="y",
		stencil_colname=None,
		device_type_colname=None,
		default_stencil=None,
		):
		super().__init__(data_file)
		self.x = x
		self.y = y
		self.stencil = stencil_colname
		self.dev_type = device_type_colname
		self.default_stencil = default_stencil
		self.read(sheet_name)

	def read(self, sheet_name):
		"""read data from given excel sheet containing device data and set dataframe for the object.

		Args:
			sheet_name (str): Excel sheet name
		"""		
		super().read(sheet_name)
		self.add_missing_cols()

	def add_missing_cols(self):
		"""add the additional blank columns to dataframe if missing.
		"""		
		if not self.stencil:
			self.stencil = "stencil"
			self.df[self.stencil] = ""
		if not self.dev_type:
			self.dev_type = "dev_type"
			self.df[self.dev_type] = ""

	def add_description(self, columns_to_merge):
		"""add a description column to dataframe, which will be output of merged data of provided columns

		Args:
			columns_to_merge (iterable): provide list/set/tuple of column names to be merged in a single
			description column.

		Raises:
			ValueError: Raises error if Mandtory hostname column is missing.
		"""		
		cols = []
		for x in columns_to_merge:
			try:
				cols.append(self.df[x])
			except:
				print(f"column `{x}` is missing in input file")
		try:
			self.df['description'] = self.df.hostname
		except:
			raise ValueError("Missing mandatory column `hostname` ")

		for col in cols:
			if col.empty:  continue
			self.df.description += "\n"+ col.str.strip().fillna("invalid datatype")


# -----------------------------------------------------------------------------------

def merged_df_on_hostname(devices_df, cablemtx_df, hostname_col_hdr, sortby):
	"""merge two dataframes by matching hostname column

	Args:
		devices_df (DataFrame): Devices details dataframe
		cablemtx_df (DataFrame): Cabling details dataframe
		hostname_col_hdr (str): column name of hostname from cabling dataframe to be merge with
		sortby (str): adhoc column name on which data to be sorted

	Raises:
		ValueError: Raise Exception if hostname column missing.

	Returns:
		DataFrame: merged DataFrame
	"""		
	try:
		cablemtx_df['hostname'] = cablemtx_df[hostname_col_hdr]
	except:
		raise ValueError(f"Missing mandatory column `{hostname_col_hdr}`")
	cablemtx_df = cablemtx_df.reset_index()
	return pd.merge(cablemtx_df, devices_df, 
		on=["hostname",], 
		sort="False", 
		).fillna("").sort_values(sortby)

# -----------------------------------------------------------------------------------
class CableMatrixData(Data):
	"""Cabling Data Object Building
	"""		

	def __init__(self, 
		data_file, 
		sheet_name,
		a_device_colname, 
		b_device_colname,
		a_device_port_colname=None,
		connector_type_colname=None,
		cable_color_colname=None,
		cable_weight_colname=None,
		cable_line_pattern_colname=None,
		):
		super().__init__(data_file)
		self.dev_a = a_device_colname
		self.dev_b = b_device_colname
		self.dev_a_port = a_device_port_colname
		self.conn_type = connector_type_colname
		self.color = cable_color_colname		
		self.weight = cable_weight_colname
		self.pattern = cable_line_pattern_colname
		self.read(sheet_name)

	def read(self, sheet_name):
		"""read data from given excel sheet containing cabling data and set dataframe for the object.

		Args:
			sheet_name (str): Excel sheet name
		"""		
		super().read(sheet_name)
		self.add_missing_cols()

	def add_missing_cols(self):
		"""add the additional blank columns to dataframe if missing.
		"""		
		if not self.dev_a_port:
			self.dev_a_port = "a_device_port"
			self.df[self.dev_a_port] = ""
		if not self.conn_type:
			self.conn_type = "conn_type"
			self.df[self.conn_type] = ""
		if not self.color:
			self.color = "color"
			self.df[self.color] = ""
		if not self.weight:
			self.weight = "weight"
			self.df[self.weight] = ""
		if not self.pattern:
			self.pattern = "pattern"
			self.df[self.pattern] = ""

	# optional
	def filter_eligible_cables_only(self):
		"""optional filter: filters DataFrame for the column `include` with values as `y`
		"""				
		if "include" in self.df.columns:
			self.df = self.df[ self.df.include == "y"]

	# optional
	def filter(self, **kwargs):
		"""filter the dataframe for given column:value
		multiple kwargs act as 'and' operation.
		"""		
		for k, v in kwargs.items():
			self.df = self.df[self.df[k] == v]

	# mandatory
	def calc_slop(self, DD):
		"""calculate the slop and angle of the two end points and add it in respective column
		in dataframe.

		Args:
			DD (DeviceData): DeviceData object
		"""		
		dev_df = DD.df.reset_index()
		df2a = merged_df_on_hostname(dev_df, self.df, self.dev_a, 'index_x')
		df2b = merged_df_on_hostname(dev_df, self.df, self.dev_b, 'index_y')
		mdf = pd.merge(df2a, df2b, on=[self.dev_a, self.dev_b])
		mdf = mdf[mdf.index_x_x==mdf.index_x_y]		
		# self.df = df_with_slops_and_angles(mdf, 'y_x', 'y_y', 'x_x', 'x_y')
		yx = DD.y + "_x"
		yy = DD.y + "_y"
		xx = DD.x + "_x"
		xy = DD.x + "_y"
		self.df = df_with_slops_and_angles(mdf, yx, yy, xx, xy)


# -----------------------------------------------------------------------------------

