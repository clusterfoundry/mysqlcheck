#!/usr/bin/env python

from bottle import route, run, response, HTTPResponse
from json import dumps
import MySQLdb
import sys

@route('/api/clustersize/<cluster_size:int>')
def healthcheck(cluster_size):
	dbconn = MySQLdb.connect(user='mysqlcheck',host='127.0.0.1')
	dbcur = dbconn.cursor()
	dbcur.execute("show status like 'wsrep_%'")
	dbstatus = dict(dbcur.fetchall())
	if dbcur: dbcur.close()

	if dbstatus['wsrep_cluster_size']:
		# if wsrep_cluster_size does not meet quorum
		if not (cluster_size / 2) < ((int(dbstatus['wsrep_cluster_size']) / 2) + 1):
			response.status = 503
			result = { 'wsrep_cluster_size': 'fail' }
		else:
			result = { 'wsrep_cluster_size': 'pass' }

	if dbstatus['wsrep_cluster_status'] == 'Primary':
		result.update({ 'wsrep_cluster_status': 'pass' })
	else:
		result.update({ 'wsrep_cluster_status': 'fail' })
		response.status = 503

	if dbstatus['wsrep_ready'] == 'ON':
		result.update({ 'wsrep_ready': 'pass' })
	else:
		result.update({ 'wsrep_ready': 'fail' })
		response.status = 503


	## get values from 'show variables'
	dbcur = dbconn.cursor()
	dbcur.execute("show variables like 'wsrep_%'")
	dbvars = dict(dbcur.fetchall())
	if dbcur: dbcur.close()
	
	if dbconn: dbconn.close()

	response.content_type = 'application/json'
	return dumps(dict({'conditions': result, 'status': dbstatus, 'variables': dbvars}), indent=4)

@route('/api/key/<table>/<key>')
def getKeyValue(table, key):
	dbconn = MySQLdb.connect(user='mysqlcheck',host='127.0.0.1')
	dbcur = dbconn.cursor()
	dbcur.execute("show %s like %s", (table, key))

	row = dict(dbcur.fetchall())

	if dbcur: dbcur.close()
	if dbconn: dbconn.close()
	if not row:
		return HTTPResponse(status=404, body='Error: Key not found')

	response.content_type = 'application/json'
	return dumps(row, indent=4)

def main():
	run(host='0.0.0.0', port=3305)
	return 0

if __name__ == '__main__':
	sys.exit(main())
