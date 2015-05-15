import sublime, sublime_plugin, os, threading

class WSync(sublime_plugin.EventListener):
	def on_post_save(self, view):
		thread = WSyncer(view.file_name())
		thread.start()

class WSyncer(threading.Thread):
	def __init__(self, filename):
		self.filename = filename
		threading.Thread.__init__(self)

	def run(self):
		settings = sublime.active_window().project_data().get('settings', {}).get('wsync')
		if not settings:
			return

		repo = settings.get('repo')
		if not repo:
			return

		local_base = os.path.dirname(sublime.active_window().project_file_name())

		if not self.filename.startswith(local_base + '/'):
			return

		path = self.filename.replace(local_base, '')
		remote_base = "/nfs/repos-sf/%s" % repo

		# os.system("scp %s %s" % (local_base + path, remote_base + path))
		# print("scp %s %s" % (local_base + path, remote_base + path))
