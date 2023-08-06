import os
import subprocess
import sys
os.environ['ANSI_COLORS_DISABLED']="1"
import fire
def _run_command(args):
    return subprocess.check_call(" ".join(args), shell=True)
class CLI:
    def hi(self):
        print('Hi, welcome to use  !'.center(50, '*'))
    def run(self,host="localhost",port=8004,dc_data_source="./data.db"):
        from cloudos_webdav_server.wsgidav.server.server_cli import run
        import yaml
        config_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),"data/wsgidav_config.yaml")
        with open(config_path,'r') as f:
            cfg=yaml.safe_load(f)
        cfg["host"]=host
        cfg["port"]=port
        cfg["cloudos_dc"]["data_source"]=dc_data_source
        run(cfg)
    @classmethod
    def cmd(cls, *args, **kwargs):
        _run_command(sys.argv[2:])

    @classmethod
    def testsysargv(cls, *args, **kwargs):
        import sys
        print("sys.argv:", sys.argv)
        print("executable:", sys.executable)

def main():
    fire.Fire(CLI())

if __name__ == '__main__':
    main()