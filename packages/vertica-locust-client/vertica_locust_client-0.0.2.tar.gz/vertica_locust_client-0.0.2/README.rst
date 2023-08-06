=====================
Vertica Locust Client
=====================

The package includes an object that you can use as a client for the locust.io
load testing tool.  The client can be used to write load testing workloads that
automatically connect to a Vertica database.

The client also integrates with a graphite backend to be able to flow metrics to it.

Installation
------------

To install this package:

::

  pip install vertica_locust_client


Locust Command Line Parameters
------------------------------

This will automatically add parameters to locust that will control how to
connect to Vertica and the graphite backend.  These parameters are also exposed
in the webUI.

::

  --user              ID of user to connect to Vertica with (defaults to dbadmin)
  --password          Password of the Vertica user ID (defaults to empty string)
  --carbon-endpoint   The carbon endpoint to connect to.
                      The endpoint is defined as: host[:port][,host[:port]...]
  --carbon-namespace  The namespace for the carbon metric.  This is treated as
                      the prefix when constructing the full metric name.


Sample locustfile
-----------------

Here is a sample locustfile.py to show the client in action.  This will issue a
simple query to count the number of sessions in the database.

::

  from locust import task
  from vertica_locust_client import VerticaUser

  class SessionCounterUser(VerticaUser):
      def __init__(self, environment):
          super().__init__(environment)

      @task
      def query_users(self):
          with self.client.make_cursor(carbon_metric="query") as cur:
              cur.execute('''
                  select count(session_id) sessions
                  from v_monitor.sessions
                  where session_id not in (
                      select session_id
                      from current_session
                  )
                  ''')