import datetime
import os

IMAGE_NAME = 'eveneko/code-runner'
SELF_DIR = '/Users/eveneko/Documents/Astor/static'
# SELF_DIR = 'media'
SANDBOX_DIR = '/workspace'


def drun(user_id, algorithm, dataset, cpu, mem):
    # main_path = 'media/Algorithm/{0}/main.py'.format(algorithm)
    # print(main_path)

    client = docker.from_env()
    volumes = {SELF_DIR: {'bind': SANDBOX_DIR, 'mode': 'ro'}}
    cpu_num = cpu.split(' ')[0]
    mem_m = mem.split(' ')[0] * 1
    # command = 'python3 {program} -i {parameters}'.format(
    #     program=os.path.join(SANDBOX_DIR, 'Algorithm', algorithm, 'main.py'),
    #     parameters=os.path.join(SANDBOX_DIR, 'Data', str(user_id), dataset)
    # )
    command = 'python3 {program}'.format(
        program=os.path.join(SANDBOX_DIR, 'test', 'b.py')
    )
    # command = 'pip3 list'

    container = client.containers.run(IMAGE_NAME,
                                      command=command,
                                      detach=True,
                                      mem_limit=str(mem_m) + 'm',
                                      nano_cpus=1000000000 * int(cpu_num),
                                      volumes=volumes,
                                      read_only=True,
                                      memswap_limit=str(int(mem_m * 2)) + 'm',
                                      working_dir=SANDBOX_DIR,
                                      tmpfs={
                                          '/tmp': 'rw,size=1g',
                                          '/run': 'rw,size=1g'
                                      },
                                      stdout=True,
                                      stderr=True,
                                      )

    stdout = True
    stderr = True

    if stdout:
        _stdout = container.logs(
            stdout=True,
            stderr=False
        )
    else:
        _stdout = b''
    if stderr:
        _stderr = container.logs(
            stdout=False,
            stderr=True
        )
    else:
        _stderr = b''

    print("stdout:", _stdout.decode('utf8'))
    print("stderr:", _stderr.decode('utf-8'))

    return _stdout.decode('utf8'), _stderr.decode('utf8')


if __name__ == '__main__':
    drun('36', 'a_multi_b', '0cb4febb-73f5-4ec6-a290-e997352d0f8c', '1 core', '512 m')
