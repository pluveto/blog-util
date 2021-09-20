import deploy
import release_all
from subprocess import call
import os
import shutil
from pathlib import Path
import yaml


def main():
    set_working_dir()    

    config_file_path = "config.yaml"
    config = yaml.load(open(config_file_path, encoding="utf-8",
                            mode="r"), Loader=yaml.SafeLoader)

    print("releasing to `content`...")

    release_all.main()

    print("clearing public directory...")

    build_path = config['build_path']
    if not os.path.exists(build_path):
        os.mkdir(build_path)
    clear_dir(build_path)

    print("generating...")

    ret = call("hugo", cwd=get_parent(build_path), shell=True)
    if(ret != 0):
        print("FAILED")
        exit(1)

    print("deploying...")

    deploy.main()

def clear_dir(dirname):
    shutil.rmtree(dirname)


def get_parent(dir = None):
    if dir == None:
        path = Path(os.getcwd())
    else:
        path = Path(dir)
    return(path.parent.absolute())

def set_working_dir():
    # 将工作目录设置为脚本所在目录
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

if __name__ == "__main__":
    main()
