import json
import logging
import sys
import time
import traceback
import urllib.request

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QCheckBox

logFile = ""

def report_error(logFile):
	urllib.request.Request("https://sentry.io/api/6180531/store/", data=json.dumps(obj), headers={
		"Content-Type": "application/json",
		"X-Sentry-Auth": "Sentry sentry_version=7, sentry_key=bb24092faa44db38842a02d70273e68, sentry_client=errorhandler/1",
	})



def excepthook(excType, excValue, tracebackobj):
	"""
	Global function to catch unhandled exceptions.

	@param excType exception type
	@param excValue exception value
	@param tracebackobj traceback object
	"""
	separator = '-' * 80
	notice = \
		"""An unhandled exception occurred. Please report the problem\n"""\
		"""using the error reporting dialog.\n"""\
		"""A log has been written to "<a href="file">%s</a>".\n\nError information:\n""" % \
		( logFile,)
	versionInfo="0.0.1"
	timeString = time.strftime("%Y-%m-%d, %H:%M:%S")

	tbinfo = traceback.format_tb(tracebackobj)
	errmsg = '%s: \n%s' % (str(excType), str(excValue))
	sections = [separator, timeString, separator, errmsg, separator]+ tbinfo
	msg = '\n'.join(sections)
	logging.error(msg)

	errorbox = QMessageBox()
	errorbox.setIcon(QMessageBox.Critical)
	errorbox.setWindowTitle("Application Error")
	errorbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Abort)
	errorbox.setDefaultButton(QMessageBox.Ok)
	errorbox.setText(str(notice)+str(msg)+str(versionInfo))
	#cbReport = QCheckBox("Report this error including log file")
	#errorbox.setCheckBox(cbReport)
	try:
		#TODO for some reason, the exec method fails with the following exception *after* closing the dialog
		#TypeError: unable to convert a C++ 'QProcess::ExitStatus' instance to a Python object
		res = errorbox.exec()
		print("msgbox result",res)
		#if cbReport.isChecked():
		#	report_error(logFile)
		if res == QMessageBox.Abort:
			sys.exit(2)
	except Exception as e:
		traceback.print_exc()
		print(str(e))

