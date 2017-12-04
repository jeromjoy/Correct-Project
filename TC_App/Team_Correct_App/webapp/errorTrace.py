import traceback

def handleErrorTracePsyco(e):
    print("I am unable to connect to the database")
    print(e)
    print(e.pgcode)
    print(e.pgerror)
    print(traceback.format_exc())

def handleErrorTrace():
    print(traceback.format_exc())