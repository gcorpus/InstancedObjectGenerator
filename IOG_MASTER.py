""" IOG:Instanced Object Generator.
    Goal: builds series of instanced objects, adding variations on transfomations and amount.
"""
import traceback

from PySide import QtCore
from PySide import QtGui

from shiboken import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui

import random


def mayaMainWindow():
	""" Returns the Maya main window as a Python object"""

	mayaMainWindow = omui.MQtUtil.mainWindow()
	return wrapInstance(long(mayaMainWindow),QtGui.QWidget)

class GeneratorSerieUI(QtGui.QDialog):
	""" Builds the generator window with all its functions """

	signals = QtCore.Signal()

	def __init__(self,parent = mayaMainWindow()):
		super(GeneratorSerieUI,self).__init__(parent)

	#----------------#	
	#-- Build GUI ---#
	#----------------#
	def createGUI(self):
		""" Builds the main window of the tool"""

		self.setWindowTitle("Instanced Object Generator")
		self.setWindowFlags(QtCore.Qt.Tool)
		self.setFixedSize(350,250) 

		self.createWidgets()
		self.createLayout()

	def createWidgets(self):
		""" Builds each widget of the tool"""

		self.bxPos = QtGui.QPushButton("+x")
		self.bxPos.setMinimumSize(50,50)
		self.bxPos.setMaximumSize(50,50)
		self.bxNeg = QtGui.QPushButton("-x")
		self.bxNeg.setMinimumSize(50,50)
		self.bxNeg.setMaximumSize(50,50)
		self.byPos = QtGui.QPushButton("+y")
		self.byPos.setMinimumSize(50,50)
		self.byPos.setMaximumSize(50,50)
		self.byNeg = QtGui.QPushButton("-y")
		self.byNeg.setMinimumSize(50,50)
		self.byNeg.setMaximumSize(50,50)
		self.bzPos = QtGui.QPushButton("+z")
		self.bzPos.setMinimumSize(50,50)
		self.bzPos.setMaximumSize(50,50)
		self.bzNeg = QtGui.QPushButton("-z")
		self.bzNeg.setMinimumSize(50,50)
		self.bzNeg.setMaximumSize(50,50)

		self.lCount = QtGui.QLabel("Count")
		self.lCount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignCenter)
		self.eCount = QtGui.QSpinBox()
		self.eCount.setRange(1,99)

		self.lMultiply = QtGui.QLabel("Multiply")
		self.lMultiply.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignCenter)
		self.eMultiply = QtGui.QDoubleSpinBox()
		self.eMultiply.setRange(1.00, 99.99)

		self.cbTransform = QtGui.QComboBox()
		self.cbTransform.addItems(["Transfomation x","Transformation y","Transformation z"])

		self.lRange1 = QtGui.QLabel("Range")
		self.eRange1 = QtGui.QSpinBox()
		self.eRange1.setMinimumSize(50,15)
		self.eRange1.setRange(-99,99)
		self.lRange2 = QtGui.QLabel("to")
		self.eRange2 = QtGui.QSpinBox()
		self.eRange2.setMinimumSize(50,15)
		self.eRange2.setRange(-99,99)

		self.bRandom = QtGui.QPushButton("Randomizer")

	def createLayout(self):
		""" Builds the needed layouts and assign the widgets to each one. 
		    The signals are created, connecting with its slots. """

		coordGridLayout = QtGui.QGridLayout()
		coordGridLayout.addWidget(self.bxPos,0,0)
		coordGridLayout.addWidget(self.bxNeg,0,1)
		coordGridLayout.addWidget(self.byPos,1,0)
		coordGridLayout.addWidget(self.byNeg,1,1)
		coordGridLayout.addWidget(self.bzPos,2,0)
		coordGridLayout.addWidget(self.bzNeg,2,1)
		

		coordGroup = QtGui.QGroupBox("Controls")
		coordGroup.setLayout(coordGridLayout)
		

		optionsGridLayout = QtGui.QGridLayout()
		optionsGridLayout.addWidget(self.lCount,0,0)
		optionsGridLayout.addWidget(self.eCount,0,1)
		optionsGridLayout.addWidget(self.lMultiply,1,0)
		optionsGridLayout.addWidget(self.eMultiply,1,1)

		optionsGroup = QtGui.QGroupBox("Options")
		optionsGroup.setLayout(optionsGridLayout)

		randomGridLayout = QtGui.QVBoxLayout()
		randomGridLayout.addWidget(self.cbTransform)

		rangeGridLayout = QtGui.QHBoxLayout()
		rangeGridLayout.addWidget(self.lRange1)
		rangeGridLayout.addWidget(self.eRange1)
		rangeGridLayout.addWidget(self.lRange2)
		rangeGridLayout.addWidget(self.eRange2)

		randomGridLayout.addLayout(rangeGridLayout)
		randomGridLayout.addWidget(self.bRandom)

		randomGroup = QtGui.QGroupBox("Random options")
		randomGroup.setLayout(randomGridLayout)

		subMainLayout = QtGui.QVBoxLayout()
		subMainLayout.addWidget(optionsGroup)
		subMainLayout.addWidget(randomGroup)

		mainLayout = QtGui.QHBoxLayout()
		mainLayout.addWidget(coordGroup)
		mainLayout.addLayout(subMainLayout)
		mainLayout.addStretch()

		#-------------------------#
		#-- SIGNALS (events) -----#
		#-------------------------#
		self.bxPos.clicked.connect(self.objectsSerie)
		self.bxNeg.clicked.connect(self.objectsSerie)
		self.byPos.clicked.connect(self.objectsSerie)
		self.byNeg.clicked.connect(self.objectsSerie)
		self.bzPos.clicked.connect(self.objectsSerie)
		self.bzNeg.clicked.connect(self.objectsSerie)
		self.bRandom.clicked.connect(self.randomizer)

		self.setLayout(mainLayout)

	#-------------------------------#
	#-- SLOTS (functions/methods)---#
	#-------------------------------#
	def objectsSerie(self):
		""" Gets values and call the instanceObject function"""
		sender = self.sender()
		count = self.eCount.value()
		multiply = self.eMultiply.value()
		selectedObjects = cmds.ls(selection = True)

		self.instanceObject(count,multiply,selectedObjects,sender.text())


	def instanceObject(self, count, multiply, selectedObjects, sender):
		""" Creates instanced objects according to sent parameters """

		for s in selectedObjects:
			beforeObject = s

			for r in range(count):
				instancedObject = cmds.instance(beforeObject) #createObject
				transformation = cmds.xform(beforeObject,ws=True,t=True,q=True) #Get reference position


				if sender =="+x":
					transformation[0] = (multiply + transformation[0]) #Fix desired position
					cmds.xform(instancedObject, ws=True,t=(transformation[0],transformation[1],transformation[2]))#moveObject

				elif sender == "-x":
					transformation[0] = (multiply + (transformation[0]*(-1))) #Fix desired position
					cmds.xform(instancedObject, ws=True,t=(-transformation[0],transformation[1],transformation[2]))#moveObject

				if sender =="+y":
					transformation[1] = (multiply + transformation[1]) #Fix desired position
					cmds.xform(instancedObject, ws=True,t=(transformation[0],transformation[1],transformation[2]))#moveObject

				elif sender == "-y":
					transformation[1] = (multiply + (transformation[1]*(-1))) #Fix desired position
					cmds.xform(instancedObject, ws=True,t=(transformation[0],-transformation[1],transformation[2]))#moveObject

				if sender =="+z":
					transformation[2] = (multiply + transformation[2]) #Fix desired position
					cmds.xform(instancedObject, ws=True,t=(transformation[0],transformation[1],transformation[2]))#moveObject

				elif sender == "-z":
					transformation[2] = (multiply + (transformation[2]*(-1))) #Fix desired position
					cmds.xform(instancedObject, ws=True,t=(transformation[0],transformation[1],-transformation[2]))#moveObject

				beforeObject = instancedObject

	def randomizer(self):
		""" Calculates random transformation by selected object"""

		cbTransformation = self.cbTransform.currentIndex()
		range1 = self.eRange1.value()
		range2 = self.eRange2.value()
		selectedObjects = cmds.ls(selection = True)


		for s in selectedObjects:

			t = cmds.xform(s,ws=True,t=True,q=True)
			randomTrans = random.uniform(range1, range2)

			if cbTransformation == 0:
				cmds.xform(s, ws=True,t=(randomTrans,t[1],t[2]))
				print("X")

			elif cbTransformation == 1:
				cmds.xform(s, ws=True,t=(t[0],randomTrans,t[2]))
				print("Y")

			elif cbTransformation == 2:
				cmds.xform(s, ws=True,t=(t[0],t[1],randomTrans))
				print("Z")


if __name__=="__main__":
	""" Executes the class GeneratorSerieUI"""

	try:
		generatorUI.close()
	except:
		pass

	generatorUI= GeneratorSerieUI()
	generatorUI.createGUI()
	generatorUI.show()

