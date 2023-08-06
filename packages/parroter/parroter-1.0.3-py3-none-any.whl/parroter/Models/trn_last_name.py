import LibHanger.Models.fields as fld
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import Null

# Baseクラス生成
Base = declarative_base()

class trn_last_name(Base):
	
	# テーブル名
	__tablename__ = 'last_name'
	
	# 列定義
	ranking = fld.NumericFields(6,0,primary_key=True,default=0)
	last_name = fld.CharFields(40,default='')
	numPeple = fld.NumericFields(9,0,default=0)
