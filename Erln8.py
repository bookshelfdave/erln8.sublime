# ------------------------------------------------------------
# erln8.sublime: erln8 support for SublimeText2
#
# Copyright (c) 2015 Dave Parfitt
#
# This file is provided to you under the Apache License,
# Version 2.0 (the "License"); you may not use this file
# except in compliance with the License.  You may obtain
# a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# ------------------------------------------------------------
#

import os
from os.path import dirname
import sys
from subprocess import Popen
import sublime, sublime_plugin

class Erln8Command(sublime_plugin.EventListener):
	def on_post_save(self, view):
		erln8_exe=view.settings().get('erln8_path','/usr/local/bin/erln8')		
		p = view.file_name()
		d = dirname(p)
		erl_version = self.erln8_exec(d, erln8_exe, ["--show"])		
		view.set_status("erln8", "erln8: " + erl_version)

	def erln8_exec(self, cwd, erln8, cmd_list):
		sublime.status_message(cwd)
		try:
			p = subprocess.Popen([erln8] + cmd_list, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out,err=p.communicate()
			if err != "":
				sublime.error_message("Erln8 error: " + err)
				return "error"
			else:
				cmd_output = out.strip()
				return cmd_output
		except Exception as e:
			s = str(e)
			sublime.error_message("Erln8 error: %s" % s)
			return "error"

