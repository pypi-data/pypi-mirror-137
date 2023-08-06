import sys
import os
from fuse import FUSE, fuse_exit
import subprocess
import time
import mlflow
import glob
import json

import infinstor
from infinstor.infinfs.infinfs import InfinFS

INPUT_SPEC_CONFIG = os.getcwd() + "/infin-input-spec.conf"

def launch_fuse_infinfs(ifs):
    mountpath = ifs.get_mountpoint()
    umountp = subprocess.Popen(['umount', '-lf', mountpath], stdout=sys.stdout, stderr=subprocess.STDOUT)
    umountp.wait()
    FUSE(ifs, mountpath, nothreads=True, foreground=False)
    print("exiting")

def infin_declare_input(mountpath, name=None):
    if 'INFINSTOR_SERVICE' not in os.environ:
        print("No action needed")
        return

    mountname = name
    service_name = os.environ.get('INFINSTOR_SERVICE')
    print('Infinstor service: ' + service_name)

    ##Always re-mount if a mountpoint exists
    if not mountpath or mountpath[0] != '/':
        raise Exception("Mountpath must be an absolute path")
    mpath = mountpath.rstrip('/')

    if not os.path.exists(mpath):
        os.makedirs(mpath)

    with open(INPUT_SPEC_CONFIG) as fp:
        specs = json.load(fp)

    named_spec_map = get_named_input_spec_map(specs)

    if mountname:
        spec_list = named_spec_map.get(mountname)
    else:
        spec_list = specs

    if len(spec_list) > 1:
        index = 0
        for spec in spec_list:
            if mountname:
                extended_mpath = os.path.join(mpath, mountname+"-"+str(index))
            else:
                extended_mpath = os.path.join(mpath, "part-" + str(index))
            os.mkdir(extended_mpath)
            index +=1
            input_spec_str = json.dumps(spec)
            print("Mounting..." + extended_mpath)
            fuse_process = subprocess.Popen(['python', os.path.realpath(__file__), extended_mpath, input_spec_str],
                                            stdout=sys.stdout, stderr=subprocess.STDOUT)
            time.sleep(1)
        time.sleep(2)
    else:
        print("Mounting..." + mpath)
        input_spec_str = json.dumps(spec_list[0])
        fuse_process = subprocess.Popen(['python', os.path.realpath(__file__), mpath, input_spec_str],
                                        stdout=sys.stdout, stderr=subprocess.STDOUT)
        time.sleep(3)
    ##Wait for some time for mounts to become visible
    print("Mounted")

def infin_log_output(output_dir):
    if 'INFINSTOR_SERVICE' not in os.environ:
        print("No action needed")
        return
    if mlflow.active_run():
        infinstor.log_all_artifacts_in_dir(None, None, output_dir, delete_output=False)
    else:
        print('No active run')

def get_named_input_spec_map(inputs):
    named_map = dict()
    for item in inputs:
        name = item['name']
        if name not in named_map:
            named_map[name] = list()
        named_map[name].append(item)
    return named_map

if __name__ == '__main__':
    mountpoint = sys.argv[1]
    input_spec_str = sys.argv[2]
    input_spec = json.loads(input_spec_str)

    if input_spec == None:
        print('Error no input spec found, skipping mount')
        exit(-1)

    service_name = os.environ.get('INFINSTOR_SERVICE')
    ifs = InfinFS(mountpoint, input_spec, service_name)
    launch_fuse_infinfs(ifs)
    exit(0)
