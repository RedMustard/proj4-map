"""
Very simple Flask web site, with one page
displaying a course schedule.

"""

import flask
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify # For AJAX transactions

import json
import logging

# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# Our own module
# import acp_limits


###
# Globals
###
app = flask.Flask(__name__)
import CONFIG

import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)


###
# Pages
###

@app.route("/")
@app.route("/index")
@app.route("/calc")
def index():
  app.logger.debug("Main page entry")
  return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("calc")
    return flask.render_template('page_not_found.html'), 404

############### Work around for loading extra js plugins ##############
@app.route("/_moment")
def moment():
  app.logger.debug("Moment.js Page")
  return flask.render_template('moment.js')

@app.route("/_collapse")
def collapse():
  app.logger.debug("Collapse.js Page")
  return flask.render_template('collapse.js')

@app.route("/_transitions")
def transitions():
  app.logger.debug("Transition.js Page")
  return flask.render_template('transition.js')

@app.route("/_bootdate")
def bootdate():
  app.logger.debug("Bootstrap Datepicker.js Page")
  return flask.render_template('bootstrap-datetimepicker.min.js')

@app.route("/_boot")
def boot():
  app.logger.debug("Bootstrap min.js Page")
  return flask.render_template('bootstrap.min.js')
######################################################

###############
#
# AJAX request handlers 
#   These return JSON, rather than rendering pages. 
#
###############
@app.route("/_calc_close_times")
def calc_times():
  """
  Calculates open/close times from miles, using rules 
  described at http://www.rusa.org/octime_alg.html.
  Expects one URL-encoded argument, the number of miles. 
  """
  app.logger.debug("Got a JSON request");
  miles = request.args.get('miles', 0, type=int)
  # brevetDist = request.args.get('brevetDist', 0, type=int)

  if miles in range(0,601):
    return jsonify(result=miles/15)

  elif miles in range(601,1000):
    return jsonify(result=miles/11.428)

  elif miles in range(1000, 1300):
    return jsonify(result=miles/13.333)
 

@app.route("/_calc_open_times")
def calc_open_times():
  """
  Calculates open/close times from miles, using rules 
  described at http://www.rusa.org/octime_alg.html.
  Expects one URL-encoded argument, the number of miles. 
  """
  app.logger.debug("Got a JSON request");
  miles = request.args.get('miles', 0, type=int)
  # brevetDist = request.args.get('brevetDist', 0, type=int)

  if miles in range(0,201):
    # hours=miles/34
    return jsonify(hours=miles//34)

  elif miles in range(201,401):
    return jsonify(hours=miles//32)

  elif miles in range(401,601):
    return jsonify(result=miles//30)

  elif miles in range(601,1001):
    return jsonify(result=miles//28)

  elif miles in range(1001, 1301):
    return jsonify(result=miles//26)

#################
#
# Functions used within the templates
#
#################

@app.template_filter( 'fmtdate' )
def format_arrow_date( date ):
    try: 
        normal = arrow.get( date )
        return normal.format("ddd MM/DD/YYYY")
    except:
        return "(bad date)"

@app.template_filter( 'fmttime' )
def format_arrow_time( time ):
    try: 
        normal = arrow.get( date )
        return normal.format("hh:mm")
    except:
        return "(bad time)"



#############


if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT)

    
