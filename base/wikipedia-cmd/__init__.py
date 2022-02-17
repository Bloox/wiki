import app,sys

print("starting session . . .")
print('')
print('')
print('')
try:
    app.check(sys.argv[1])
except:
    app.check(app.base)