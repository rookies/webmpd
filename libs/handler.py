import sys, traceback, atexit, io

## GLOBAL VARIABLES:
STATUS = 200
HEADERS = {
	"Content-Type": "text/html"
}
CONTENT = io.StringIO()
## HANDLER FUNCTION FOR EXCEPTIONS:
def exception_hook(exc_type, exc, tb):
	global CONTENT
	set_status(500)
	print("<pre>", file=CONTENT)
	traceback.print_exception(exc_type, exc, tb, limit=2, file=CONTENT)
	print("</pre>", file=CONTENT)
	sys.exit()
## HANDLER FUNCTION FOR EXITING:
def exit_hook():
	global STATUS, HEADERS, CONTENT
	sys.stdout = sys.__stdout__
	print("Status: %d" % STATUS)
	for key, val in HEADERS.items():
		print("%s: %s" % (key, val))
	print("")
	print(CONTENT.getvalue(), end="")
## FUNCTION TO SET HTTP STATUS CODE:
def set_status(code):
	global STATUS
	try:
		code = int(code)
	except:
		return False
	else:
		STATUS = code
		return True
## FUNCTION TO SET HTTP HEADER:
def set_header(key, val):
	global HEADERS
	HEADERS[key] = val
## REGISTER HANDLER FUNCTIONS:
sys.excepthook = exception_hook
atexit.register(exit_hook)
sys.stdout = CONTENT
