import numpy as np
import sqlite3




class dbOperations:

	def __init__(self):
		self.connection = None
		self.isConnected = False
		self.docTableExists = False
		self.labelTableExists = False
		self.connection_cursor = None
		self.connect()
		self.createDocTable()
		#self.createLabelTable()

	def connect(self):
		try:
			self.connection = sqlite3.connect('static/test.db')
			self.connection_cursor = self.connection.cursor()
			self.isConnected = True
		except Exception as e:
			self.isConnected = False

	def createDocTable(self):

		query = '''CREATE TABLE IF NOT EXISTS doc (
		docId INTEGER PRIMARY KEY AUTOINCREMENT, docName text NOT NULL,
		docPath text NOT NULL
		);'''

		if self.isConnected:
			try:
				self.connection_cursor.execute(query)
				self.connection.commit()
				self.docTableExists = True
			except Exception as e:
				self.docTableExists = False
				print(e)

	def insertIntoDoc(self,docName,docPath):
		if self.isConnected and self.docTableExists:
			query = '''INSERT INTO doc (docName, docPath)
					VALUES ("{}", "{}")'''.format(docName,docPath)
			try:
				self.connection_cursor.execute(query)
				self.connection.commit()
				return ['success']
			except Exception as e:
				return ['alert',e]
				pass
		else:
			return ['alert','DB connection Error']

	def listDocTable(self):
		if self.isConnected and self.docTableExists:
			query = '''SELECT * from doc'''
			try:
				self.connection_cursor.execute(query)
				rows = self.connection_cursor.fetchall()
				return ['success',np.array(rows)]
			except Exception as e:
				return ['alert',e]
		else:
			return ['alert','DB connection Error']

	def queryDocTable(self,docId):
		if self.isConnected and self.docTableExists:
			query = '''SELECT docPath WHERE docId = {}'''.format(docId)
			try:
				self.connection_cursor.execute(query)
				docPath = self.connection_cursor.fetchall()
				return ['success',docPath]
			except Exception as e:
				return ['alert',e]
		else:
			return ['alert','DB connection Error']









#done
