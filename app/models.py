
from sqlalchemy import Column, Float, Text, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from flask.ext.appbuilder import Model
from flask.ext.appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""
        
class Batch(Model):
	id = Column(Integer, primary_key=True)
	arch =  Column(String(128) )
	rev = Column(String(7))
	timestamp = Column(DateTime)
	error = Column(Integer)
	xfail = Column(Integer)
	tpass = Column(Integer)
	skip = Column(Integer)
	total = Column(Integer)
	xpass = Column(Integer)
	fail = Column(Integer)

	def __repr__(self):
		return self.name

class Failure(Model):
	id = Column(Integer, primary_key=True)
	test = Column(String(16))
	runtime = Column(Float)
	log = Column(Text)
	batch = Column(Integer, ForeignKey('batch.id'))


