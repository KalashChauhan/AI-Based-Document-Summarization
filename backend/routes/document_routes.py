from flask import Blueprint,jsonify
from models.database import list_records,get_record,delete_record

document_bp=Blueprint('document',__name__)
def serialize(row): return dict(row)
@document_bp.get('/history')
def history(): return jsonify(success=True,items=[serialize(x) for x in list_records()])
@document_bp.get('/history/<int:summary_id>')
def detail(summary_id):
    row=get_record(summary_id)
    return (jsonify(success=True,item=serialize(row)),200) if row else (jsonify(success=False,error='Summary not found.'),404)
@document_bp.delete('/history/<int:summary_id>')
def delete(summary_id):
    return (jsonify(success=True,message='Summary deleted.'),200) if delete_record(summary_id) else (jsonify(success=False,error='Summary not found.'),404)
