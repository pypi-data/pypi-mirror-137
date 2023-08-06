from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import func, distinct
from sqlalchemy import over
from sqlalchemy import inspect

from sqlalchemy import Column, Boolean, Date, DateTime, Float, Integer, Text, String

from sqlalchemy.orm import aliased
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
import uuid
import json
import datetime
from sqlalchemy import select


"""
Kraken_db api

methods:

- get:
    - input:

- search:



"""


"""

engine = create_engine('sqlite:///test.sqlite?''uri=true&check_same_thread=False&timeout=10', echo=False)

Base = declarative_base()


Session = sessionmaker(bind=engine)
session = Session()
"""

"""
Class declaration
"""
Base = declarative_base()


class DB_observation(Base):
    __tablename__ = 'DB_observations'

    id = Column(String)
    observation_id = Column(String, primary_key=True)
    ref_id = Column(String)
    datasource = Column(String)
    agent = Column(String)
    instrument = Column(String)
    object = Column(String)
    result = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    valid = Column(Boolean)

    record_type = Column(String)
    record_id = Column(String)
    key = Column(String)
    value = Column(String)
    value_float = Column(Float)
    value_date = Column(DateTime)
    value_id = Column(String)
    value_type = Column(String)
    credibility = Column(Float)
    created_date = Column(DateTime)    



    def _asdict(self):
        record = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

        record.pop('id')
        record.pop('ref_id')

        return record

#Base.metadata.create_all(engine)



class Kraken_db:
    
    def __init__(self, filepath):
        
        self.engine = create_engine('sqlite:///' + filepath + '.sqlite?''uri=true&check_same_thread=False&timeout=10', echo=False)

        #Base = declarative_base()


        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)



    """
    API - DB_observations
    """



    def rollback(self):
        self.session.rollback()






    def get(self, record_type = None, record_id = None, key = None, value = None):
        # Get DB_observations matching conditions
        query = self._get_observations(record_type, record_id, key, value)

        return self._to_dict(query)


    def get_max(self, record_type = None, record_id = None, key = None, value = None):
        """Return max DB_observation
        """
        query = self._get_max_observations(record_type, record_id, key, value)


        return self._to_dict(query)


    def get_summary(self, record_type = None, record_id = None, key = None, value = None):
        """Return object with max DB_observation for each key
        """

        query = self._get_summary(record_type, record_id, key, value)

        return self._to_dict(query)


    def get_summary_by_value(self, record_type = None, record_id = None):
        """Return object with max DB_observation for each key value combination
        """

        query = self._get_summaries_by_value(record_type, record_id)

        return self._to_dict(query)



    """
    API - entities
    """


    def search(self, params, order_by = None, order_direction = None, limit = None, offset = None):

        query = self._search(params, order_by, order_direction, limit, offset)

        return self._to_dict(query)


    def search_summary(self, params, order_by = None, order_direction = None, limit = None, offset = None):
        """Search and return summaries
        """

        query = self._search(params, order_by, order_direction, limit, offset)

        query = self._get_summaries(query)

        return self._to_dict(query)




    def search_first(self,params, order_by = None, order_direction = None, limit = None, skip = None):

        query = self._search(params, order_by, order_direction, 1, 0)

        return self._to_dict(query)



    def post(self, record):
        """Post an DB_observation. Need ot be committed
        """
        result = self._post_observation_from_record(record)
        result = self.commit()

        return


    def update(self, old_record_type, old_record_id, new_record_type, new_record_id):
        """Changes record_id and related references
        """

        self._update(old_record_type, old_record_id, new_record_type, new_record_id)

        self.commit()

        return


    def commit(self):
        """Commmit posting of DB_observations
        """
        self._commit()

        return

    """
    Methods
    """

    def list_record_types(self):
        """Return list of dict with record_types and number for each
        """
        query = self.session.query(func.count(distinct(DB_observation.record_id)), DB_observation.record_type).group_by(DB_observation.record_type).all()

        records = []
        for n, t in query:

            record = {
                'record_type': t,
                'n': n
            }
            records.append(record)

        return records


    def _get_observations(self, record_type, record_id, key, value):
        """ Return DB_observations matching condition
        """
        query = self.session.query(DB_observation)

        if record_type:
            query = query.filter(DB_observation.record_type == record_type)

        if record_id:
            query = query.filter(DB_observation.record_id == record_id)
            
        if key:
            query = query.filter(DB_observation.key == key)

        if value:
            query = query.filter(DB_observation.value == value)


        return query



    def _get_max_observations(self, record_type, record_id, key, value):

        query = self._get_observations(record_type, record_id, key, value)

        query.order_by(DB_observation.credibility.desc()).order_by(DB_observation.credibility.created_date())

        # Limit
        query = query.limit(1)

        return query

    def _get_summary(self, record_type = None, record_id = None, key = None, value = None):

        query1 = self._get_observations(record_type, record_id, key, value)
        
        query = self._get_summaries(query1)


        return query

    def _get_summaries(self, query):
        """Returns best DB_observation for each keys of records in scope of query
        """

        subquery1 = query

        subquery1 = subquery1.subquery()

        # Filter for top credibility
        subquery2 = self.session.query(subquery1)
        subquery2 = subquery2.group_by(subquery1.c.record_type)
        subquery2 = subquery2.group_by(subquery1.c.record_id)
        subquery2 = subquery2.group_by(subquery1.c.key)
        subquery2 = subquery2.having(func.max(subquery1.c.credibility) == subquery1.c.credibility)
        subquery2 = subquery2.subquery()
        
        # Filter for top created date
        subquery3 = self.session.query(subquery2)
        subquery3 = subquery3.group_by(subquery2.c.record_type)
        subquery3 = subquery3.group_by(subquery2.c.record_id)
        subquery3 = subquery3.group_by(subquery2.c.key)
        subquery3 = subquery3.having(func.max(subquery2.c.created_date) == subquery2.c.created_date)

        return subquery3


    def _get_summaries_by_value(self, record_type, record_id):
        """Returns best DB_observation for each keys/values of records in scope of query
        """

        # Get max cred for each key
        obs1 = aliased(DB_observation)

        subquery1 = self.session.query(obs1)
        subquery1 = subquery1.filter(obs1.record_type == record_type)
        subquery1 = subquery1.filter(obs1.record_id == record_id)
        subquery1 = subquery1.subquery()
        
        # Filter for top credibility
        subquery2 = self.session.query(subquery1)
        subquery2 = subquery2.group_by(subquery1.c.key)
        subquery2 = subquery2.group_by(subquery1.c.value)
        subquery2 = subquery2.having(func.max(subquery1.c.credibility) == subquery1.c.credibility)
        subquery2 = subquery2.subquery()
        
        # Filter for top created date
        subquery3 = self.session.query(subquery2)
        subquery3 = subquery3.group_by(subquery2.c.key)
        subquery3 = subquery3.group_by(subquery2.c.value)
        subquery3 = subquery3.having(func.max(subquery2.c.created_date) == subquery2.c.created_date)

        # Order
        subquery3 = subquery3.order_by(subquery2.c.key)
        subquery3 = subquery3.order_by(subquery2.c.credibility.desc())
        subquery3 = subquery3.order_by(subquery2.c.created_date.desc())

        return subquery3




    def _post_observation_from_record(self, record):
        
        if type(record) is list:
            for i in record:
                self._post_observation_from_record(i)
            return


        if not record.get('created_date', None):
            record['created_date'] = datetime.datetime.now()

        record_ref_id = str(record.get('record_type', None)) + '/' + str(record.get('record_id', None))

        obs = DB_observation(
            observation_id = record.get('observation_id', None),
            ref_id = record_ref_id,
            datasource = record.get('datasource', None),
            agent = record.get('agent', None),
            instrument = record.get('instrument', None),
            object = record.get('object', None),
            result = record.get('result', None),
            start_time = record.get('start_time', None),
            end_time = record.get('end_time', None),
            valid = record.get('valid', None),

            record_type = record.get('record_type', None),
            record_id = record.get('record_id', None),
            key = record.get('key', None),
            value = record.get('value', None),
            credibility = record.get('credibility', None),
            created_date = record.get('created_date', None)    
            )

        # If value is a number, update value_float for searching purposes
        if isinstance(record.get('value', None), (int, float)):
            obs.value_float = float(record.get('value', None))


        # if value is date, udate date
        if isinstance(record.get('value', None), datetime.datetime):
            obs.value_date = record.get('value', None)

        if isinstance(record.get('value', None), dict):
            if '@type' in record.keys() and '@id' in record.keys():

                obs['value_type'] = record.get('@type', None)
                obs['value_type'] = record.get('@id', None)


        self.session.merge(obs)


    def _update(self, old_record_type, old_record_id, new_record_type, new_record_id):

        # Step 1. Update record_ids
        query = self.session.query(DB_observation)
        query = query.filter(DB_observation.record_type == old_record_type)
        query = query.filter(DB_observation.record_id == old_record_id)

        query = query.update(
            {
                DB_observation.record_type: new_record_type, 
                DB_observation.record_id: new_record_id
                })


        # Step 2. Update references to record_ids
        old_record = {
            '@type': old_record_type,
            '@id': old_record_id
        }
        old_record = json.dumps(old_record, default=str)

        new_record = {
            '@type': new_record_type,
            '@id': new_record_id
        }
        new_record = json.dumps(new_record, default=str)

        query = self.session.query(DB_observation)
        query = query.filter(DB_observation.value == old_record)

        query = query.update(
            {
                DB_observation.value: new_record }
                )


    def _commit(self):

        self.session.commit()



    def _search(self, params, order_by = None, order_direction = None, limit = None, offset = None):
        """ Return entities matching multiple conditions
        """

        query = None

        obs0 = aliased(DB_observation)


        # Step 1. Find DB_observations meeting conditions
        for key, operator, value in params:
            sub_query = self.session.query(obs0.ref_id.label('ref_id2'))

            if key == 'record_type':
                sub_query = sub_query.filter(obs0.record_type.like(value))
            elif key == 'record_id':
                sub_query = sub_query.filter(obs0.record_id.like(value))
            
            elif key == 'created_date':
                sub_query = sub_query.filter(obs0.created_date.like(value))        
            else:
                # text
                if isinstance(value, str):
                    if operator in ['eq', '==']:
                        sub_query = sub_query.filter(obs0.key == key)
                        sub_query = sub_query.filter(obs0.value == value)

                # if number
                elif isinstance(value, (int, float)):

                    if operator in ['eq', '==']:
                        sub_query = sub_query.filter(obs0.key == key)
                        sub_query = sub_query.filter(obs0.value_float == value) 
                    
                    elif operator in ['gt', '>']:
                        sub_query = sub_query.filter(obs0.key == key)
                        sub_query = sub_query.filter(obs0.value_float > value)            

                    elif operator in ['ge', '>=']:
                        sub_query = sub_query.filter(obs0.key == key)
                        sub_query = sub_query.filter(obs0.value_float >= value)   

                    elif operator in ['lt', '<']:
                        sub_query = sub_query.filter(obs0.key == key)
                        sub_query = sub_query.filter(obs0.value_float < value)            

                    elif operator in ['le', '<=']:
                        sub_query = sub_query.filter(obs0.key == key)
                        sub_query = sub_query.filter(obs0.value_float <= value)   

                    elif operator in ['contains']:
                        sub_query = sub_query.filter(obs0.key == key)
                        sub_query = sub_query.filter(value in obs0.value_float)  

                    elif operator in ['in']:
                        sub_query = sub_query.filter(obs0.key == key)
                        sub_query = sub_query.filter(obs0.value_float in value)  

                # if date
                elif isinstance(value, datetime.datetime):
                    if operator in ['eq', '==']:
                        sub_query = sub_query.filter(obs0.key == key)
                        sub_query = sub_query.filter(obs0.value_date == value)  


                    elif operator in ['gt', '>']:
                        sub_query = sub_query.filter(obs0.key == key)
                        sub_query = sub_query.filter(obs0.value_date > value)            
                    elif operator in ['ge', '>=']:
                        sub_query = sub_query.filter(obs0.key == key)
                        sub_query = sub_query.filter(obs0.value_date >= value)   

                    elif operator in ['lt', '<']:
                        sub_query = sub_query.filter(obs0.key == key)
                        sub_query = sub_query.filter(obs0.value_date < value)            
                    elif operator in ['le', '<=']:
                        sub_query = sub_query.filter(obs0.key == key)
                        sub_query = sub_query.filter(obs0.value_date <= value)  

                elif isinstance(value, dict):
                    record_type = value.get('@type', None)
                    record_id = value.get('@id', None)

                    if record_type and record_id:   
                        sub_query = sub_query.filter(obs0.key == key)
                        sub_query = sub_query.filter(obs0.value_type == record_type)  
                        sub_query = sub_query.filter(obs0.value_id == record_id)  
            
            if query:
                query = query.intersect(sub_query)
            else:
                query = sub_query


        # apply order_by
        if order_by:
            if order_direction not in ['asc', 'desc']:
                order_direction = 'asc'

            query = query.order_by(getattr(getattr(obs0, order_by), order_direction)())


        # Apply unique
        query = query.distinct(obs0.ref_id)


        # apply limit and offset
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)



        # Step 2. Retrieve all DB_observations with same ref_id
        subquery = query
        subquery = subquery.subquery()
        
        
        obs1 = aliased(DB_observation)
        query = self.session.query(obs1)

        query = query.join(subquery, subquery.c.ref_id2 == obs1.ref_id )



        return query


    def test(self):
        
        query = None

        obs0 = aliased(DB_observation)
        sub_query0 = self.session.query(obs0.ref_id.label("ref_id2"))

        sub_query0 = sub_query0.filter(obs0.key == 'schema:qty')
        sub_query0 = sub_query0.filter(obs0.value > 2)
        sub_query0 = sub_query0.distinct(obs0.ref_id)

        obs1 = obs0 #aliased(DB_observation)
        sub_query1 = self.session.query(obs1.ref_id.label("ref_id2"))
        sub_query1 = sub_query1.filter(obs1.key == 'schema:qty')
        sub_query1 = sub_query1.filter(obs1.value < 5)
        sub_query1 = sub_query1.distinct(obs1.ref_id)


        query_s = sub_query0.intersect(sub_query1)



        query_s = query_s.subquery()




        obs_all = aliased(DB_observation)

        query = self.session.query(obs_all)

        for i in query:
            print(i.value, i.ref_id)


        query = query.join(query_s, obs_all.ref_id == query_s.c.ref_id2)




        #print(len(query))
        for i in query:
            print(i.value)
       


    """
    Methods: transformation
    """


    def _to_dict_single(self, record):


        if type(record) is dict:

            result = {}
            for c in record.keys():
                result[c] = getattr(record, c)


            result.pop('id')
            result.pop('ref_id')

            return result

        else:
            result = record._asdict()

        #         

        return result



    def _to_dict(self, querys):
        # COnvert sqlalchemy classes to dicts
        records = []
        for r in querys:
            record = self._to_dict_single(r)
            records.append(record)

        return records


