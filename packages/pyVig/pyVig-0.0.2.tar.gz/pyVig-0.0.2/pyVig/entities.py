
# -----------------------------------------------------------------------------------

from nettoolkit import Multi_Execution

from pyVig.visio import device

# -----------------------------------------------------------------------------------
#  Visio Objects / Items
# -----------------------------------------------------------------------------------
class ItemObjects(Multi_Execution):
	"""Execution of Devices/Item objects on visio
	"""		

	def __init__(self, 
		visObj, 
		devices_data,
		connectors,
		filterOnCables=True
		):
		self.visObj = visObj
		self.devices_data = devices_data
		self.devices_details_list = (dev for i, dev in devices_data.df.iterrows())
		self.connectors = connectors
		self.filterOnCables=filterOnCables
		#
		self.devices = {}
		self.x_coordinates = []
		self.y_coordinates = []
		super().__init__(self.devices_details_list)
		self.start(multi_thread=False)

	def __getitem__(self, k): return self.devices[k]

	@property
	def top_most(self):
		"""top most used co-ordinate on visio

		Returns:
			int: maximum of used y-axis
		"""		 
		return max(self.y_coordinates)
	@property
	def bottom_most(self): 
		"""bottom most used co-ordinate on visio

		Returns:
			int: minimum of used y-axis
		"""		 
		return min(self.y_coordinates)
	@property
	def left_most(self): 
		"""left most used co-ordinate on visio

		Returns:
			int: minimum of used x-axis
		"""		 
		return min(self.x_coordinates)
	@property
	def right_most(self): 
		"""right most used co-ordinate on visio

		Returns:
			int: maximum of used x-axis
		"""		 
		return max(self.x_coordinates)
	@property
	def page_height(self): 
		"""total height occupied by drawing  on visio page

		Returns:
			int: page height
		"""		 		
		try:
			return self.top_most - self.bottom_most + 3
		except:
			return 4
	@property
	def page_width(self): 
		"""total width occupied by drawing  on visio page

		Returns:
			int: page width
		"""		 		
		try:
			return self.right_most - self.left_most + 3
		except:
			return 8
	
	def execute(self, dev):
		"""Executor
		Paralllel processing disabled currently due to visio not support

		Args:
			dev (dict): a single row details of device data

		Returns:
			None: None
		"""		
		# filter to only drop connected devices.
		if (self.filterOnCables 
			and (not (
				(dev.hostname == self.connectors.df[self.connectors.dev_a]).any() 
				or (dev.hostname == self.connectors.df[self.connectors.dev_b]).any()) ) ):
			return None

		# ---- get column values from row of a device info --- #
		x=get_col_value(dev, self.devices_data.x, isMerged=False)
		y=get_col_value(dev, self.devices_data.y, isMerged=False)
		item=get_col_value(dev, self.devices_data.dev_type, isMerged=False)
		stencil=get_col_value(dev, self.devices_data.stencil, isMerged=False)

		# // adhoc, add corordinates for future calculation purpose.
		self.x_coordinates.append(x)
		self.y_coordinates.append(y)

		if not stencil: stencil = self.devices_data.default_stencil
		if not stencil:
			print(f"no stencil or no default-stencil found for {dev.hostname} ")

		# -- start drops ---
		self.devices[dev.hostname] = device(						# drop device
			stencil=stencil, 
			visObj=self.visObj, 
			item=item,
			x=x,
			y=y,
			)
		# -- add description ---
		self.devices[dev.hostname].description(dev.description)	# description of device


# -----------------------------------------------------------------------------------
#  Visio Connectors
# -----------------------------------------------------------------------------------
class Connectors(Multi_Execution):
	"""Execution of Cabling/Connector objects on visio
	"""		

	def __init__(self, cable_matrix_data, devices):
		self.connectors = cable_matrix_data
		self.connectors_list = (connector for i, connector in cable_matrix_data.df.iterrows())
		self.devices = devices
		super().__init__(self.connectors_list)
		self.start(multi_thread=False)

	def execute(self, connector):
		"""Executor
		Paralllel processing disabled currently due to visio not support

		Args:
			connector (dict): a single row details of cabling data

		Returns:
			None: None
		"""		
		if connector[self.connectors.dev_a] and connector[self.connectors.dev_b]:
			aport_y = get_col_value(connector, self.connectors.dev_a_port + "_y")
			conn_type_x = get_col_value(connector, self.connectors.conn_type + "_x")
			color_x = get_col_value(connector, self.connectors.color + "_x")
			weight_x = get_col_value(connector, self.connectors.weight + "_x")
			pattern_x = get_col_value(connector, self.connectors.pattern + "_x")
			angle = connector.angle_straight_connector if conn_type_x == "straight" else connector.angle_angled_connector

			# connect the two devices	
			self.devices[connector[self.connectors.dev_a]].connect(
				self.devices[connector[self.connectors.dev_b]],
					connector_type=conn_type_x, 
					angle=angle, 
					aport=aport_y,
					color=color_x,
					weight=weight_x,
					pattern=pattern_x,
			)

def get_col_value(row_info, column, isMerged=True):
	"""get the value of provided column from given row details

	Args:
		row_info (dict): a single row information from a DataFrame
		column (str): column name 
		isMerged (bool, optional): is it a merged column or native. Defaults to True.

	Returns:
		str: Cell information from row
	"""	
	try:
		return row_info[column]
	except:
		if isMerged:
			print(f"column information incorrect, check column existance `{column[:-2]}`")
		else:
			print(f"column information incorrect, check column existance `{column}`")
		return ""


# -----------------------------------------------------------------------------------
