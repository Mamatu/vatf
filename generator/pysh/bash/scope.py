from pysh import core

def handle(body, endLine = ''):
    if body != None:
        if type(body) is core.Command:
            body()
        elif callable(body):
            body()
        elif type(body) is str:
            if type(endLine) is str:
                core.sh("{}{}".format(body, endLine))
            elif type(endLine) is bool:
                if endLine:
                    core.shnl(body)
                else:
                    core.sh(body)
