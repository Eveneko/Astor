import docker
import datetime
import os


def run(algorithm, dataset_path, cpu, mem):
    main_path = 'media/Algorithm/{0}/main.py'.format(algorithm)
    print(main_path)
    client = docker.from_env()
    client.containers.run('eveneko/code-runner:latest', 'media/Algorithm/a_multi_b/run.sh')
