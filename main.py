#! coding: utf-8
from elasticsearch import Elasticsearch
from flask import Flask, redirect, url_for, request, jsonify
from flask_restful import Resource, Api 
from elasticsearch_dsl.query import MultiMatch, Match
from elasticsearch.exceptions import RequestError,NotFoundError
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q
from elasticsearch_dsl.query import Range, Bool
from werkzeug.exceptions import BadRequest
from flask_cors import CORS
import elasticsearch_dsl
import logging
import traceback

# connects to the remote Elastic Search server
es = Elasticsearch('https://search-test-weather-report-fptvnjecv4pqkkzb663b4zmleq.us-east-2.es.amazonaws.com/')
# creating the flask app 
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
# creating an API object 
api = Api(app) 

class login(Resource):   
   def __init__(self):
      self.log = logging.getLogger("main")
      #tracking information that everything is going as expected
      self.log.setLevel(logging.INFO)
   def post(self):
      try:
         data = request.get_json().get('data','')
         fromTime = request.get_json().get('fromTime','')
         fromTime = fromTime[:-5]+fromTime[-1]
         toTime = request.get_json().get('toTime','')
         toTime = toTime[:-5]+toTime[-1]   
         search = Search(using=es, index='stag_wx_report')     #search object
         r = Range(** {'date_time': {'time_zone': '+01:00', 'gte': fromTime, 'lte': toTime}})   #date-time range filter
         search = search.query(Q('multi_match', query=data, fields=['area','city','city_name','location','comment','title','lonlat[0]','lonlat[1]'])).query(r)
         start_page = int(request.get_json().get('start_page',''))
         start_page = (start_page-1)*12
         end_page = start_page+12
         response = search[start_page:end_page].execute()
         response = response.to_dict()
      except BadRequest as e:
         raise e
      except RequestError as e: # elasticsearch.exceptions.RequestError: RequestError(400, 'illegal_argument_exception', 'Cannot parse scroll id')
         err_msg = "scrollid : Invalid scrollid"
         self.log.error(err_msg)
         return { "message": err_msg }, e.status_code
      except NotFoundError as e: # elasticsearch.exceptions.NotFoundError: NotFoundError(404, 'search_phase_execution_exception', 'No search context found for id [54260]')
         err_msg = "scrollid : No search context found for id. The search might have expired."
         self.log.error(err_msg)
         return { "message":err_msg }, e.status_code
      except Exception as e:
         err_msg = "{}\n{}".format(repr(e), traceback.format_exc())
         self.log.error(err_msg)
         return {"message": "Internal server error."}, 500

      self.log.info("200")

      return response,200

api.add_resource(login, '/')

#driver function
if __name__ == '__main__':
   app.run(debug = True)