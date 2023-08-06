# ------------------------------------------------------------------------------
#  IMPORTS
# ------------------------------------------------------------------------------
import win32com.client
from win32com.client import constants
import traceback
from random import randint

from pyVig.static import *
from pyVig.common import get_filename

# ------------------------------------------------------------------------------
#  VisioObject class
# ------------------------------------------------------------------------------
class VisioObject:
	'''Creates a Visio Object. 
	Param : stencils  - object stancils
	example : oVis = VisioObject(stencils=[stencil1, stencil2])
			  stencil1 and stencil2 are two different stencils.
	'''

	# stencils dictionary
	stn = {}

	# --------------------------------------------------------------------------
	#  dunders
	# --------------------------------------------------------------------------

	# object initializer
	def __init__(self, stencils=None, outputFile=None):
		"""Initialize Visio Object by starting Visio Application, 
		Opens a blank Visio Document/Page inside it.
		open all stencils mentioned

		Args:
			stencils (list, optional): List of stencils. Defaults to None.
			outputFile (str, optional): output filename. Defaults to None.
		"""		
		self.page_number = 0
		self.no_of_icons = 0
		self.icons = {}
		self.outputFile = outputFile
		self._startVisio
		self._openBlankVisioDoc
		if all([stencils is not None, 
				self.visio is not None,
				self.doc is not None,
				# self.page is not None,
				]):
			for value in stencils:
				v = get_filename(value)
				self.stn[v] = self.openStencil(value)

	# context Load
	def __enter__(self):
		return self

	# context end
	def __exit__(self, exc_type, exc_value, tb):
		self._saveVisio(self.outputFile)
		self._closeVisio()
		if exc_type is not None:
			traceback.print_exception(exc_type, exc_value, tb)

	# Object Representation
	def __repr__(self):
		return f'VisioObject: {self.outputFile}'

	# --------------------------------------------------------------------------
	#  Internal
	# --------------------------------------------------------------------------

	# save visio output file
	def _saveVisio(self, file):
		try: self.doc.SaveAs(file)
		except: pass

	# close visio application
	def _closeVisio(self):
		try:
			self.doc.Close()
			self.visio.Quit()
		except:
			pass

	# Internal use only: starts a new Visio Application
	@property
	def _startVisio(self):
		try:
			self.visio = win32com.client.Dispatch("Visio.Application")
		except:
			self.visio = None

	# Internal use only: Open a blank visio page inside opened Visio Application
	@property
	def _openBlankVisioDoc(self):
		self.doc = self.visio.Documents.Add("")

	def insert_new_page(self, name=None):
		self.page_number += 1
		self.page = self.doc.Pages.Add()
		self.page = self.doc.Pages.Item(self.page_number)
		if name: self.page.Name = name

	# Return item from Stencil
	def _selectItemfromStencil(self, item, stencil):
		return self.stn[stencil].Masters.Item(item)

	# Drops 'item' on visio page at given position index ( posX and posY )
	def _dropItemtoPage(self, item, posX, posY):
		try: 
			itemProp = self.page.Drop(item, posY, posX)
			return itemProp
		except: 
			pass

	@staticmethod
	def _border(item, borderLineColor=None, borderLinePattern=None,
		borderLineWeight=0) :
		if borderLineColor is not None:
			item.Cells( 'LineColor' ).FormulaU = borderLineColor
		if borderLinePattern is not None and isinstance(borderLinePattern, int):
			item.Cells( 'LinePattern' ).FormulaU = borderLinePattern
		if borderLineWeight > 0:
			item.Cells( 'LineWeight' ).FormulaU = borderLineWeight

	@staticmethod
	def _fill(item, fillColor=None, fillTransparency=None):
		if fillColor is not None:
			item.Cells( 'Fillforegnd' ).FormulaU = fillColor
		if fillTransparency is not None:
			if isinstance(fillTransparency, int):
				fillTransparency = str(fillTransparency) + "%"
			item.CellsSRC(visSectionObject, visRowFill, visFillForegndTrans).FormulaU = fillTransparency
			item.CellsSRC(visSectionObject, visRowFill, visFillBkgndTrans).FormulaU = fillTransparency

	@staticmethod
	def _text(item, text=None, textColor=None, textSize=0, vAlign=1, hAlign=0, style=None):
		if text is not None:
			item.Text = text
		if textColor is not None:
			item.CellsSRC(visSectionCharacter, 0, visCharacterColor).FormulaU = textColor
		if textSize > 0 and isinstance(textSize, int):
			item.Cells( 'Char.size' ).FormulaU = textSize
		if isinstance(vAlign, int) and (vAlign>=0 and vAlign<=2):
			item.Cells( 'VerticalAlign' ).FormulaU = vAlign
		if isinstance(hAlign, int) and (hAlign>=0 and hAlign<=2):
			item.CellsSRC(visSectionParagraph, 0, visHorzAlign).FormulaU = hAlign
		if style is not None:
			if isinstance(style, str):
				item.CellsSRC(visSectionCharacter, 0, visCharacterStyle).FormulaU = visCharStyle[style]
			elif isinstance(style, (list, tuple)):
				for x in style:
					item.CellsSRC(visSectionCharacter, 0, visCharacterStyle).FormulaU = visCharStyle[x]

	### FORMATTING ###	
	def _format(self, icon,
		text=None, textColor=None, textSize=0, vAlign=1, hAlign=0, style=None,
		fillColor=None, fillTransparency=None,
		borderLineColor=None, borderLinePattern=None, borderLineWeight=0  
		):
		''' Formatting Parameters '''
		self._border(icon, borderLineColor, borderLinePattern, borderLineWeight)
		self._fill(icon, fillColor, fillTransparency)
		self._text(icon, text, textColor, textSize, vAlign, hAlign, style)
		self.no_of_icons += 1
		self.icons[self.no_of_icons] = icon

	# --------------------------------------------------------------------------
	#  External
	# --------------------------------------------------------------------------

	# Internal + External : Open mentioned stencil in opened visio application. 
	def openStencil(self, stencil):
		"""open a stencil in visio document

		Args:
			stencil (str): stencil file

		Returns:
			visioStencil: visio stencil object
		"""		
		stencil = stencil.replace("/", "\\")
		try:
			return self.visio.Documents.Open(stencil)
		except:
			pass

	def selectNdrop(self, stencil, item, posX, posY, **format):
		"""Selects item 'item' from provided stencil 'stencil' for selected visio object.
		And drops that item on visio Object at given position index ( posX and posY )
		usage: icon = visObj.selectNdrop(stencil,item,posX,posY)
		**format = shape formatting (see _format() for type of formats available)
		
		Args:
			stencil (str): name of stencil
			item (str, int): icon name or number from stencil
			posX (int): plane x-coordinate
			posY (int): plane y-coordinate

		Returns:
			iconObject: dropped icon object
		"""		
		itm = self._selectItemfromStencil(item, stencil)
		if itm is not None:
			icon = self._dropItemtoPage(itm, posX, posY)
			self._format(icon=icon, **format)
			return icon

	def shapeDrow(self, shape, lx, lr, rx, rr, **format):
		"""Drops provided shape to visio page.
		Usage: shape = visObj.shapeDrow(shape, lx, lr, rx, rr, **format)
		**format = shape formatting (see _format() for type of formats available)

		Args:
			shape (str): [description]
			lx (int): x1 - coordinate
			lr (int): y1 - coordinate
			rx (int): x2 - coordinate
			rr (int): y2 - coordinate

		Returns:
			shapeObject: shape object from visio
		"""		
		shaping = True
		if shape.lower() == "rectangle":
			rect = self.page.DrawRectangle(lx, lr, rx, rr)
		elif shape.lower() == "ellipse":
			rect = self.page.DrawOval(lx, lr, rx, rr)
		elif shape.lower() == "arc":
			rect = self.page.DrawQuarterArc(lx, lr, rx, rr, visArcSweepFlagConvex)
		elif shape.lower() == "line":
			rect = self.page.DrawLine(lx, lr, rx, rr)
		else:
			shaping =False

		if shaping:
			self._format(icon=rect, **format)
			return rect

	def join(self, connector, shpObj1, shpObj2):
		"""use Connector object to join two shapes (Device objects)

		Args:
			connector (Connector): Connector object
			shpObj1 (Device): Device Object 1
			shpObj2 (Device): Device Object 2
		"""		
		try:
			connector.obj.Cells("BeginX").GlueTo(shpObj1.obj.Cells("PinX"))
		except:
			x, y = shpObj1.x, shpObj1.y
			connector.obj.CellsSRC(visSectionObject, visRowXForm1D, vis1DBeginX).FormulaU = f"{x} in"
			connector.obj.CellsSRC(visSectionObject, visRowXForm1D, vis1DBeginY).FormulaU = f"{y} in"
		try:
			connector.obj.Cells("EndX").GlueTo(shpObj2.obj.Cells("PinX"))		
		except:
			x, y = shpObj2.x, shpObj2.y
			connector.obj.CellsSRC(visSectionObject, visRowXForm1D, vis1DEndX).FormulaU = f"{x} in"
			connector.obj.CellsSRC(visSectionObject, visRowXForm1D, vis1DEndY).FormulaU = f"{y} in"


	def fit_to_draw(self, height, width):
		"""resize visio page to fit the page to drawing.

		Args:
			height (int)): page height to be resized (inch)
			width (int): page width to be resized (inch)
		"""		
		self.page.PageSheet.CellsSRC(visSectionObject, visRowPage, visPageWidth).FormulaU = f"{width} in"
		self.page.PageSheet.CellsSRC(visSectionObject, visRowPage, visPageHeight).FormulaU = f"{height} in"
		self.page.PageSheet.CellsSRC(visSectionObject, visRowPage, visPageDrawSizeType).FormulaU = "1"
		self.page.PageSheet.CellsSRC(visSectionObject, visRowPage, 38).FormulaU = "2"


# ------------------------------------------------------------------------------
# A Single Connector Class defining connector properties and methods.
# ------------------------------------------------------------------------------
class Connector():
	'''s1_s2_Connector = self.connector()
	Drops a connector to visio page.
	param : connector_type = ( eg - straight, curved, default=angled )
	param : x, u = coordinates where to drop connector (default=0,0)
	'''

	def __init__(self, visObj, connector_type=None):
		self.visObj = visObj
		self.connector_type = connector_type

	def drop(self, connector_type=None):
		"""drops a connector to visio page.

		Args:
			connector_type (str, optional): connector tpe (valid options are: 
				angled, straight, curved). Defaults to None=angled.

		Returns:
			connectorObj: Connector Object from visio
		"""		
		item = self.visObj.page.Drop(self.visObj.visio.ConnectorToolDataObject, randint(1, 50), randint(1, 50))
		if self.connector_type == "straight":
			item.CellsSRC(visSectionObject, visRowShapeLayout, visSLOLineRouteExt).FormulaU = "1"
			item.CellsSRC(visSectionObject, visRowShapeLayout, visSLORouteStyle).FormulaU = "16"
		elif self.connector_type == "curved":
			item.CellsSRC(visSectionObject, visRowShapeLayout, visSLOLineRouteExt).FormulaU = "2"
			item.CellsSRC(visSectionObject, visRowShapeLayout, visSLORouteStyle).FormulaU = "1"
		else:
			item.CellsSRC(visSectionObject, visRowShapeLayout, visSLOLineRouteExt).FormulaU = "1"
			item.CellsSRC(visSectionObject, visRowShapeLayout, visSLORouteStyle).FormulaU = "1"
		self.obj = item
		return item

	def add_a_port_info(self, aport_info, at_angle, connector_type, indent=True):
		"""add port information for (a-side interface) on connector

		Args:
			aport_info (str): port information
			at_angle (int): rotate information at angle
			connector_type (str): connector type ( angled, straight, curved )
			indent (bool, optional): indent text or not. Defaults to True.
		"""		
		self.description(aport_info)
		if connector_type and connector_type != "angled":
			# print(connector_type)
			self.text_rotate(at_angle)
		if indent: self.text_indent()

	def format_line(self, color=None, weight=None, pattern=None):
		"""formatting of line

		Args:
			color (str, optional): set color of line (blue, red, gray etc.). Defaults to None=black.
				see line_color for all available options.
			weight (int, optional): thickness of line. Defaults to None=1.
			pattern (int, optional): line patterns. Defaults to solid line.
		"""		
		if color: self.line_color(color)
		if weight: self.line_weight(weight)
		if pattern: self.line_pattern(pattern)

	@property
	def object(self):
		"""visio object

		Returns:
			visioObject: visio object
		"""		
		return self.obj

	def text_rotate(self, degree=90):
		"""Rotation of text at given angle

		Args:
			degree (int, optional): angle to be rotate to. Defaults to 90.
		"""		
		self.obj.CellsSRC(visSectionObject, visRowTextXForm, visXFormAngle).FormulaU = f"{degree} deg"

	def text_indent(self):
		"""Indention to be done on oject
		"""		
		inch = self.obj.LengthIU / 2 
		self.obj.CellsSRC(visSectionParagraph, 0, visIndentLeft).FormulaU = f"{inch} in"

	def description(self, remarks):
		"""description to be add to object.

		Args:
			remarks (str, memo): description
		"""		
		try:
			self.obj.Characters.Text = remarks
		except:
			pass

	def line_color(self, color=None):
		"""color of a line object

		Args:
			color (str tuple, optional): color of line. Defaults to black.
				valid string options are (red, green, blue, gray, lightgray, darkgray )
				Other option is to provide RGB color in tuple ex: (10, 10, 10)

		Returns:
			None: None
		"""		
		if isinstance(color, str):
			if color.lower() == "red": clr = "THEMEGUARD(RGB(255,0,0))"
			if color.lower() == "green": clr = "THEMEGUARD(RGB(0,255,0))"
			if color.lower() == "blue": clr = "THEMEGUARD(RGB(0,0,255))"
			if color.lower() == "gray": clr = "THEMEGUARD(RGB(127,127,127))"
			if color.lower() == "lightgray": clr = "THEMEGUARD(RGB(55,55,55))"
			if color.lower() == "darkgray": clr = "THEMEGUARD(RGB(200,200,200))"
		elif isinstance(color, (list, tuple)) and len(color) == 3:
			clr = f"THEMEGUARD(RGB({color[0]},{color[1]},{color[2]}))"
		else:
			return None
		try:
			self.obj.CellsSRC(visSectionObject, visRowLine, visLineColor).FormulaU = clr
		except: pass

	def line_weight(self, weight=None):
		"""set weight/thickness of a line

		Args:
			weight (int, optional): thickness of line. Defaults to None=1.
		"""		
		self.obj.CellsSRC(visSectionObject, visRowLine, visLineWeight).FormulaU = f"{weight} pt"

	def line_pattern(self, pattern=None):
		"""set line pattern

		Args:
			pattern (int, optional): pattern number. Defaults to solid line.
		"""		
		self.obj.CellsSRC(visSectionObject, visRowLine, visLinePattern).FormulaU = pattern


# ------------------------------------------------------------------------------
# A Single Visio Item Class defining its properties and methods.
# ------------------------------------------------------------------------------
class Device():
	"""A Device Object
	"""		

	def __init__(self, visObj, item, x, y):
		"""Initialize Device Object

		Args:
			visObj (Visio): visio object
			item (str): Device/Item name
			x (int): x-coordinate
			y (int): y-coordinate
		"""		
		self.visObj = visObj
		self.item = item
		self.x = x
		self.y = y

	def drop_from(self, stencil):
		"""drop an item from stencil, if item not found in stencil then it will drop a rectangle.

		Args:
			stencil (str): stencil name
		"""		
		if stencil and self.item:
			self.obj = self.visObj.selectNdrop(stencil=stencil, 
				item=self.item, posX=self.y, posY=self.x, textSize=.8)
		else:
			self.obj = self.visObj.shapeDrow('rectangle', 
				self.x, self.y, self.x+1.7, self.y+1.2,
				vAlign=1, hAlign=1)

	@property
	def object(self):
		"""self object

		Returns:
			self.obj: self object
		"""		
		return self.obj

	def connect(self, 
		remote, 
		connector_type=None, 
		angle=0, 
		aport="",
		color=None,
		weight=None,
		pattern=None,
		):
		"""connects self object with remote object using connector.

		Args:
			remote (Device): remote Device object
			connector_type (str, optional): connector type. Defaults to None='angled'.
			angle (int, optional): a-port info rotate at. Defaults to 0.
			aport (str, optional): line a-port info. Defaults to "".
			color (str, optional): line color. Defaults to None.
			weight (int, optional): line weight. Defaults to None.
			pattern (int, optional): line pattern. Defaults to None.
		"""				
		connector = Connector(self.visObj, connector_type)
		connector.drop()
		self.visObj.join(connector, self, remote)
		connector.add_a_port_info(aport, angle, connector_type, indent=False)
		connector.format_line(color, weight, pattern)

	def description(self, remarks):
		"""set description/remark of current object.

		Args:
			remarks (str, memo): remark for the object.
		"""		
		try:
			self.obj.Characters.Text = remarks
		except:
			dev = device(						# drop rectangle
				stencil=None, 
				visObj=self.visObj, 
				item="",
				x=self.x-1,
				y=self.y-1)
			dev.description(remarks)


# ------------------------------------------------------------------------------
# Device class object return by dropping it to given position
# ------------------------------------------------------------------------------
def device(stencil, visObj, item, x, y):
	"""Drop an item from stencil given to visio object at given x,y co-ordinates.

	Args:
		stencil (str): stencil name
		visObj (Visio): Visio Object
		item (str): name or number of device/item from stencil
		x (int): x coordinate
		y (int): y coordinate

	Returns:
		Device: Device Object
	"""	
	D = Device(visObj, item, x, y)
	D.drop_from(stencil)
	return D


# ------------------------------------------------------------------------------
