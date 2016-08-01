
def traverse(edge, tcs, index):
    if edge.type.name == 'DTMF':
        add_step('Dial - ' + edge.properties['Number'], tcs, index)
    elif edge.type.name == 'Speech':
        add_step('Say - ' + edge.properties['Response'], tcs, index)
    elif edge.type.name == 'Data':
        add_step('Alter Data Requirement - '
            + edge.properties['source']
            + edge.properties['value']
            + edge.properties['parameter'], tcs, index)


def add_step(step, tcs, index):
    tcs.append(str(index) + ', ' + step)
