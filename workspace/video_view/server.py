from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
class Handler(SimpleHTTPRequestHandler):
 def do_GET(self):
  if self.path=='/': self.path='/video_view/index.html'
  elif self.path!='/chapter1.mp4': self.send_error(404); return
  return super().do_GET()
ThreadingHTTPServer(('0.0.0.0',8000),Handler).serve_forever()
