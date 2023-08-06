
# -----------------------------------------------------------------------------
import PySimpleGUI as sg
from pprint import pprint

# -----------------------------------------------------------------------------
declaration = """
 ~~~~ IMPORTANT INFORMATION ~~~~
 This program was tested with MS-Visio Professional 2013.
 It may or may not work depending on your visio version.
 File save feature is not working in this visio version.
 hence it is disabled. Save the file manually.

 Macros and vBA scripting requires to be enabled in visio
 in order to access the visio components.
 select 'Enable all macros' and, check 'Trust access to vBA'
 from trust center setting of MS-visio.


 Please reachout to me, [Aliasgar Lokhandwala] for any Qs.
"""

# -----------------------------------------------------------------------------
# Class to initiate UserForm
# -----------------------------------------------------------------------------

class UserForm():
	'''Inititate a UserForm asking user inputs.	'''
	version  = 'Visio Generator : ver: 0.0.2'
	header = 'Visio Generator'

	# Object Initializer
	def __init__(self):
		self.boot = False
		self.dic = {
			'stencil_folder':"",
			# -- database variables --
			'data_file' : "",
			'devices_sheet_name':'Devices',
			'x-coordinates_col': 'x-axis',
			'y-coordinates_col': 'y-axis',
			'stencils_col': 'stencils',
			'device_type_col': 'device_type',
			'default_stencil': '',	# Default STencil
			'cabling_sheet_name': 'Cablings',
			'a_device_col': 'a_device',
			'b_device_col': 'b_device',
			'a_device_port_col': 'a_device_port',
			'connector_type_col': 'connector_type',
			'color_col': 'color',
			'weight_col': 'weight',
			'pattern_col': 'pattern',
			#
			'op_file': 'abcd.vsdx',				# optional
			'cols_to_merge': set(),			# optional
			'is_sheet_filter': False,
			'sheet_filters':{},				# optional
			'filter_on_include_col': False,	# optional
			'filter_on_cable': True			# optional
			}
		self.create_form()

	def __repr__(self):
		return f'User : {self.dic["un"]}'

	def __getitem__(self, key):
		'''get an item from parameters'''
		try:
			return self.dic[key]
		except: return None

	def enable_boot(self):
		self.boot = False
		self.w.Element('Go').Update(disabled=False)

	@property
	def blank_line(self): return [sg.Text(''),]
	def item_line(self, item, length): return [sg.Text(item*length)]
	def under_line(self, length): return [sg.Text('_'*length)]
	def button_ok(self, text, **kwargs):  return sg.OK(text, size=(10,1), **kwargs)	
	def button_cancel(self, text, **kwargs):  return sg.Cancel(text, size=(10,1), **kwargs)
	def banner(self):
		return [sg.Text(self.version, font='arialBold', justification='center', size=(768,1))] 

	def button_pallete(self):
		return [sg.Frame(title='Button Pallete', 
				size=(1024, 4), 
				title_color='blue', 
				relief=sg.RELIEF_RIDGE, 
				layout=[
			[self.button_ok("Go", bind_return_key=True), self.button_cancel("Cancel"),],
		] ), ]

	def create_form(self):
		self.tabs()
		layout = [
			self.banner(), 
			self.button_pallete(),
			self.tabs_display(),
		]
		self.w = sg.Window(self.header, layout, size=(1000,700))#, icon='data/sak.ico')
		while True:
			event, (i) = self.w.Read()
			# - Events Triggers - - - - - - - - - - - - - - - - - - - - - - - 
			if event == 'Cancel': 
				del(self.dic)
				break
			if event == 'Go': self.event_update_Go(i)
			if event == 'is_sheet_filter': self.event_update_filter(i)
			if event == 'filt_col_add': self.sheet_filter_add_col_value(i)
			if event == 'cms': self.add_columns_to_merge(i)
			if event == 'def_stn': self.update_default_stencil(i)

			# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
			if self.boot:
				self.w.Element('Go').Update(disabled=True)
				break
		self.w.Close()

	def tabs(self, **kwargs):
		tabs = []
		for k, v in kwargs.items():
			tabs.append( sg.Tab(k, [[v]]) )
		return sg.TabGroup( [tabs] )

	def tabs_display(self):
		tabs_dic = {
			'Declaration': self.show_declaration(),
			'Input Your Data': self.input_data(), 
			'Apply Filters': self.select_filters(),
			'Other Options': self.other_options(),

		}
		return [self.tabs(**tabs_dic),]

	def event_update_Go(self, i):
		exception_key_list = ('add exception list here', 'sheet_filters',
			'filt_col_key', 'filt_col_value', 'filt_col_add',
			'cols_to_merge', 'cms',
			'def_stn', 'default_stencil',)
		self.boot = True
		for k in self.dic:
			if k in exception_key_list: continue
			self.dic[k] = i[k]

	def input_data(self):
		return sg.Frame(title='User Input / Database', 
						title_color='red', 
						size=(500, 4), 
						key='user_input',						
						relief=sg.RELIEF_SUNKEN, 
						layout=[
			[sg.Text('select database file :', size=(20, 1), text_color="blue"), 
				sg.InputText(self.dic['data_file'], key='data_file'),  
				sg.FileBrowse()],
			[sg.Text('select stencils folder :', size=(20, 1), text_color="blue"), 
				sg.InputText(self.dic['stencil_folder'], key='stencil_folder'),  
				sg.FolderBrowse()],
			[sg.Text('select default stencil file :', size=(20, 1)), 
				sg.InputText("", key='def_stn', change_submits=True),
				sg.FileBrowse()],
			self.under_line(80),
			[sg.Text('devices sheet name', size=(20, 1), font='TimesBold'), sg.InputText(self.dic['devices_sheet_name'], key='devices_sheet_name', size=(20, 1))],
			[sg.Text('x-coordinates col' , size=(20, 1)), sg.InputText(self.dic['x-coordinates_col' ], key='x-coordinates_col' , size=(20, 1))],
			[sg.Text('y-coordinates col' , size=(20, 1)), sg.InputText(self.dic['y-coordinates_col' ], key='y-coordinates_col' , size=(20, 1))],
			[sg.Text('stencils col'      , size=(20, 1)), sg.InputText(self.dic['stencils_col'      ], key='stencils_col'      , size=(20, 1))],
			[sg.Text('device-type col'   , size=(20, 1)), sg.InputText(self.dic['device_type_col'   ], key='device_type_col'   , size=(20, 1))],
			self.under_line(80),
			[sg.Text('cabling sheet name', size=(20, 1), font='TimesBold'), sg.InputText(self.dic['cabling_sheet_name'], key='cabling_sheet_name', size=(20, 1))],
			[sg.Text('a-device col'      , size=(20, 1)), sg.InputText(self.dic['a_device_col'      ], key='a_device_col'      , size=(20, 1))],
			[sg.Text('b-device col'      , size=(20, 1)), sg.InputText(self.dic['b_device_col'      ], key='b_device_col'      , size=(20, 1))],
			[sg.Text('a-device port col' , size=(20, 1)), sg.InputText(self.dic['a_device_port_col' ], key='a_device_port_col' , size=(20, 1))],
			[sg.Text('connector-type col', size=(20, 1)), sg.InputText(self.dic['connector_type_col'], key='connector_type_col', size=(20, 1))],
			[sg.Text('color col'         , size=(20, 1)), sg.InputText(self.dic['color_col'         ], key='color_col'         , size=(20, 1))],
			[sg.Text('weight col'        , size=(20, 1)), sg.InputText(self.dic['weight_col'        ], key='weight_col'        , size=(20, 1))],
			[sg.Text('pattern col'       , size=(20, 1)), sg.InputText(self.dic['pattern_col'       ], key='pattern_col'       , size=(20, 1))],				
			self.under_line(80),
			])

	def select_filters(self):
		return sg.Frame(title='Database Filters', 
						title_color='red', 
						size=(500, 4), 
						key='database_filters',						
						relief=sg.RELIEF_SUNKEN, 
						layout=[
			# [sg.Text("Output Filename",), sg.InputText(self.dic['op_file'], key='op_file', size=(12, 1), disabled=True)],
			# self.under_line(80),
			# [sg.Text("Columns To be Merged"), sg.InputText("", key='cms', size=(12, 1), change_submits=True) ],
			# [sg.Text("  **Provide multiple columns separated by Comma")],
			# [sg.Text("  details from selected columns will be appended to device details along with hostname in visio")],
			# self.under_line(80),
			[sg.Checkbox('Enable filter on matching cables', default=self.dic['filter_on_cable'], key='filter_on_cable', change_submits=False) ],
			[sg.Text("  **Enabling this will omit the devices which doen't participate in cabling,")],
			[sg.Text("  Disabling will include all devices irrespective of their existance in cabling")],
			self.under_line(80),
			[sg.Text("DATA Filters",  text_color='darkBlue', font='arialBold')],
			[sg.Checkbox('Filter data based on `include` col == `x`', default=self.dic['filter_on_include_col'], key='filter_on_include_col', change_submits=False) ],
			[sg.Checkbox('Enable multi-sheet layout ', default=self.dic['is_sheet_filter'], key='is_sheet_filter', change_submits=True) ],
			[sg.Text("  **sheet name will be column name mentioned below, \n and sheet-data will be choosen based on matching values given in that particular column")],
			[sg.Text("Column Name"), sg.InputText("", key='filt_col_key', size=(12, 1), disabled=True), 
			sg.Text(" == "), sg.InputText("", key='filt_col_value', size=(12, 1), disabled=True), sg.Text(" Column Value "),
			sg.Button("ADD", change_submits=False, key='filt_col_add', disabled=True)
			],
			[sg.Text("Applied Filters:")],
			[sg.Multiline("", key='merged_filt_cols', autoscroll=True, disabled=True) ]

			])

	def other_options(self):
		return sg.Frame(title='Other Options', 
						title_color='red', 
						size=(500, 4), 
						key='oth_options',						
						relief=sg.RELIEF_SUNKEN, 
						layout=[
			[sg.Text("Output Filename",), sg.InputText(self.dic['op_file'], key='op_file', size=(12, 1), disabled=True)],
			self.under_line(80),
			[sg.Text("Columns To be Merged"), sg.InputText("", key='cms', size=(12, 1), change_submits=True) ],
			[sg.Text("  **Provide multiple columns separated by Comma")],
			[sg.Text("  details from selected columns will be appended to device details along with hostname in visio")],
			self.under_line(80),
			])

	def show_declaration(self):
		return sg.Frame(title='Declaration', 
						title_color='red', 
						size=(500, 4), 
						key='declaration',						
						relief=sg.RELIEF_SUNKEN, 
						layout=[
			self.under_line(80),
			[sg.Multiline(declaration, autoscroll=True, disabled=True, size=(40,20)) ]

			])

	def event_update_element(self, **kwargs):
		for element, update_values in kwargs.items():
			self.w.Element(element).Update(**update_values)

	def event_update_filter(self, i):
		updates = {
			'filt_col_key': {'disabled': not i['is_sheet_filter']},
			'filt_col_value': {'disabled': not i['is_sheet_filter']},
			'filt_col_add': {'disabled': not i['is_sheet_filter']},
		}
		self.event_update_element(**updates)

	def sheet_filter_add_col_value(self, i):
		self.dic['sheet_filters'][i['filt_col_key']] = i['filt_col_value']
		mfc = "\n".join([k +": "+ v for k, v in self.dic['sheet_filters'].items()])
		updates ={
			'filt_col_key': {'value': ""},
			'filt_col_value': {'value': ""},
			'merged_filt_cols': {'value': mfc}
		}
		self.event_update_element(**updates)

	def add_columns_to_merge(self, i):
		self.dic['cols_to_merge'] = set(x.strip() for x in i['cms'].split(","))

	def update_default_stencil(self, i):
		self.dic['default_stencil'] = ".".join(i['def_stn'].split("/")[-1].split(".")[:-1])

# ------------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
	# Test UI #
	u = UserForm()
	pprint(u.dic)
	del(u)
# ------------------------------------------------------------------------------
