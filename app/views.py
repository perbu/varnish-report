
from flask.ext.appbuilder.models.datamodel import SQLAModel
from flask.ext.appbuilder import ModelView
from app import appbuilder, db
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface

from .models import Batch, Failure

class BatchModelView(ModelView):
    datamodel = SQLAInterface(Batch)
    related_views = [Failure]

    label_columns = { 'tpass':'Pass'}
    list_columns = ['arch','rev','tpass','fail']


class FailureModelView(ModelView):
    datamodel = SQLAInterface(Failure)

    label_columns = {'test':'Test'}
    list_columns = ['id','batch','test','runtime']

db.create_all()

appbuilder.add_view(BatchModelView, "List Batches")
appbuilder.add_view(FailureModelView, "List Failures")