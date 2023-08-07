from .shell import *
from .file import read_file
import time
from datetime import datetime, timedelta


def install_modules(project_dir, project_name):
    cmd = 'source {}{}_venv/bin/activate && pip install -r {}requirements.txt'.format(project_dir, project_name,
                                                                                      project_dir)
    succ, err = exec_shell(cmd)
    print_succ(succ)
    print_err(err)


def start_gunicorn(project_dir, project_name, log_dir):
    cmd = '{}{}_venv/bin/gunicorn -c {}gunicorn_conf.py {}.wsgi:application'.format(project_dir, project_name, project_dir, project_name)
    exec_shell(cmd)
    time.sleep(1)
    read_last_log(log_dir, 6)


def read_last_log(log_dir, line_count):
    succ, err = exec_shell('tail -{} {}error.log'.format(line_count, log_dir))
    print_succ(succ)
    print_err(err)
    return succ, err


def reload_gunicorn(log_dir):
    pid_filename = '{}pid.pid'.format(log_dir)
    pid = read_file(pid_filename).strip()
    print('gunicorn pid:{}'.format(pid))
    if not pid:
        print_err('重启gunicorn失败,pid不存在:{}'.format(pid_filename))
    exec_shell('kill -HUP {}'.format(pid))
    time.sleep(1)
    succ, err = read_last_log(log_dir, 6)
    if not succ:
        print_err('重启失败！重启失败！重启失败！')
        return
    # 判断时间是不是2s内
    line = next(filter(lambda x: 'Hang up: Master' in x, succ.split('\n')), None)
    if not line:
        print_err('重启失败！重启失败！重启失败！')
        return
    if datetime.strptime(line[1:20], '%Y-%m-%d %H:%M:%S') > (datetime.now() - timedelta(seconds=2)):
        print_succ('重启成功:{}'.format(line[1:20]))
    else:
        print_err('重启失败！重启失败！重启失败！')