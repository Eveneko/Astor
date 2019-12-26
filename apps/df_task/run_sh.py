import os
import uuid


def run(user_id, algorithm, dataset, cpu, mem):
    if not os.path.join('static', 'Out', str(user_id)):
        os.mkdir(os.path.join('static', 'Out', str(user_id)))
    out_uuid = str(uuid.uuid4())
    command = 'python3 {program} -i {parameters} > {out}'.format(
            program=os.path.join('media', 'Algorithm', algorithm, 'main.py'),
            parameters=os.path.join('media', 'Data', str(user_id), dataset),
            out=os.path.join('static', 'Out', str(user_id), out_uuid)
        )
    os.system(command)
    return out_uuid
