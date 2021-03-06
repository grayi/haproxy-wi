#!/usr/bin/env python3
import html
import cgi
import os
import funct
import configparser

form = cgi.FieldStorage()
serv = form.getvalue('serv')

funct.head("Old Versions HAproxy config")
funct.check_config()
funct.check_login()

path_config = "haproxy-webintarface.config"
config = configparser.ConfigParser()
config.read(path_config)

hap_configs_dir = config.get('configs', 'haproxy_save_configs_dir')

funct.chooseServer("delver.py#conf", "Delete Versions HAproxy config", "n")

if serv is not None and form.getvalue('open') is not None:
	
	print('<center><h3>Choose old version</h3>')
	print('<form action="delver.py#conf" method="post">')
	
	import glob

	os.chdir(hap_configs_dir)

	for files in sorted(glob.glob('*.cfg')):
		ip = files.split("-")
		if serv == ip[0]:
			print('<label for="%s"> %s </label><input type="checkbox" value="%s" name="%s" id="%s"><br />' % (files, files, files, files, files))

	print('<input type="hidden" value="%s" name="serv">' % serv)
	print('<input type="hidden" value="open" name="open">')
	print('<input type="hidden" value="del" name="del">')
	print('<p>')
	funct.mode_admin("Delete", level="admin")
	print('</p></form>') 

	Select = form.getvalue('del')

	if Select is not None:
		os.chdir(hap_configs_dir)
		print("<b>The following files were deleted:</b><br />")
		for get in form:
			if "cfg" in get:
				try:
					os.remove(form.getvalue(get))
					print(form.getvalue(get) + "<br />")
					funct.logging(serv, "delver.py deleted config: %s" % form.getvalue(get))				
				except OSError: 
					print ("Error: %s - %s." % (e.filename,e.strerror))
		print('<meta http-equiv="refresh" content="10; url=delver.py?serv=%s&open=open">' % form.getvalue('serv'))		
		
funct.footer()