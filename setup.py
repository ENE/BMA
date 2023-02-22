import os
import sys
import time
import shutil
import logging
import pendulum
import threading
import subprocess
from zipfile import ZipFile
from cx_Freeze import setup, Executable

class Stopwatch:
    def __init__(self, locale=pendulum._LOCALE):
        self.start_time = None
        self.stop_time = None
        self.locale = locale

    def start(self):
        self.start_time = pendulum.now()

    def stop(self):
        self.stop_time = pendulum.now()

    def elapsed_time(self):
        if self.start_time is None:
            return None
        elif self.stop_time is None:
            return pendulum.now() - self.start_time
        else:
            return self.stop_time - self.start_time

    def elapsed_time_for_humans(self):
        return self.elapsed_time().in_words(locale=self.locale)

    def restart(self):
        self.start_time = pendulum.now()
        self.stop_time = None

class RedirectStdStreams(object):
    def __init__(self, stdout=None, stderr=None):
        # Construtor para a sintaxe com "with"
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr
        # TODO estudar possibilidades das alterantivas "or" acima

    def __enter__(self):
        # Forçando esvaziamento dos canais iniciais
        sys.stdout.flush()
        sys.stderr.flush()
        # Redirecionando "with" (para) os novos canais
        sys.stdout = self._stdout
        sys.stderr = self._stderr
        sys.stdout.flush()
        sys.stderr.flush()

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout.flush()
        sys.stderr.flush()
        sys.__stdout__.flush()
        sys.__stderr__.flush()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

def _fix_path(str):
    return str.replace("/", "\\\\")

def _tail_path_friendly(path):
    return '/'.join(path.replace("\\\\", "/").split('/')[-2:])

def PutGlobalVariables():
    global site_packages
    global devdir
    global project
    global egg
    global zipname
    global icons_src
    global icons_dst
    global err_log
    global out_log
    global cxe_log
    global cxo_log
    global new_log

    # Temporary variables 
    user = "Alexandre"
    version = "310"  # of Python
    filename = "PyNeuro-1.3.1-py3.10" # TODO scan?
    root_dir = "D:/Git/EEG" # TODO yaml
    build = "exe.win-amd64-3.10" # TODO scan?

    # Processing values
    site_packages = f"C:/Users/{user}/AppData/Local/Programs/Python/Python{version}/Lib/site-packages"
    #site_packages = _fix_path(site_packages) # TODO env vars?
    devdir = _fix_path(f"{root_dir}/Pull/PyNeuro") # TODO yaml, it only? 
    project = _fix_path(f"{root_dir}/BMA") # TODO yaml
    egg = _fix_path(f"{site_packages}/{filename}.egg")
    zipname = _fix_path(f"{site_packages}/{filename}.zip")
    icons_src = _fix_path(f"{project}/icons")
    icons_dst = _fix_path(f"{project}/build/{build}/icons")
    err_log = _fix_path(f"{project}/build/error.log")
    cxe_log = _fix_path(f"{project}/build/error-freeze.log")
    out_log = _fix_path(f"{project}/build/output.log")
    cxo_log = _fix_path(f"{project}/build/output-freeze.log")

    # Restart log files?
    new_log = True
    
    if new_log:
        if os.path.exists(err_log):
            os.remove(err_log)
        if os.path.exists(out_log):
            os.remove(out_log)
        if os.path.exists(cxe_log):
            os.remove(cxe_log)
        if os.path.exists(cxo_log):
            os.remove(cxo_log)

class Log:
    INFO  = "  [info]"
    WARN  = "  [warn]"
    ERROR = " [error]"
    FAIL  = "  [fail]"
    FATAL = " [fatal]"

    def __setattr__(self, name, value):
        raise TypeError("Você não pode alterar as constantes")

class PackageHammer():
    class Action:
        INSTALL = "install"
        UNINSTALL = "uninstall"
    
        def __setattr__(self, name, value):
            raise TypeError("Você não pode alterar as constantes")

    def __init__(self, package="PyNeuro", directory=None):
        self.pkg = package
        self.dir = directory
        self.err_file = err_log
        self.out_file = out_log

    def _exec_pip(self, command=Action.UNINSTALL):
        with open(self.out_file, "w") as output_file,open(self.err_file, "w") as error_file:
            self.last_code = subprocess.Popen(
                [sys.executable, "-m", "pip", command, "-y", self.pkg],
                stdout=output_file, stderr=error_file
            ).wait()
        self._on_error_print(f"{Log.FAIL} pip {command} {self.pkg}")

    def _exec_setuptools(self, command=Action.INSTALL):
        with open(self.out_file, "w") as output_file,open(self.err_file, "w") as error_file:
            self.last_code = subprocess.Popen(
                [sys.executable, "setup.py", command], cwd=self.dir,
                stdout=output_file, stderr=error_file
            ).wait()
        msg  = f"{Log.FAIL} python setup.py {command}\n"
        msg += f"{Log.INFO} it was trying in {self.dir}"
        self._on_error_print(msg)

    def install(self):
        print()
        print(f" Installing package {self.pkg}")
        if not self.dir:
            NotADirectoryError
        self._exec_setuptools()

    def uninstall(self):
        print()
        print(f" Removing package {self.pkg}")
        self._exec_pip(PackageHammer.Action.UNINSTALL)

    def _on_error_print(self, message):
        if self.last_code != 0:
            print(message)
            print(f"{Log.INFO} subprocess return code {self.last_code}")
            sys.exit(-2)

def explode_egg_in_folder():
    if os.path.exists(zipname):
        os.remove(zipname)  # garante ZIP inexistente
        fname = zipname.split('\\')[-1]
        print(f"{Log.INFO} {fname} removed")
    shutil.move(egg, zipname)
    print(f"{Log.INFO} new ZIP created (.egg moved)")
    with ZipFile(zipname, 'r') as zip_ref:
        print()
        print(" Beginning extraction to -egg dir")
        zip_ref.extractall(egg)
    print(f"{Log.INFO} extraction terminated")
    os.remove(zipname)  # garante ZIP inexistente
    print(f"{Log.INFO} the new ZIP file was erased too")
    # parece não haver malefícios

def copy_all_icons_to_build():  # unsed
    try:
        shutil.copytree(icons_src, icons_dst)
    except FileExistsError:
        print("[warning] icons/ já existia no destino")

def ConfigureFreezerLogging():
    # Cria dois manipuladores de arquivo, um para sys.stdout e outro para sys.stderr
    stdout_handler = logging.FileHandler(cxo_log, mode='w')
    stderr_handler = logging.FileHandler(cxe_log, mode='w')
    # Define os níveis de log para cada manipulador
    stdout_handler.setLevel(logging.CRITICAL)
    stderr_handler.setLevel(logging.CRITICAL)
    # Define o formato da mensagem para cada manipulador
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stdout_handler.setFormatter(formatter)
    stderr_handler.setFormatter(formatter)
    # Adiciona os manipuladores ao logger padrão
    logger = logging.getLogger()
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

def ExecutePrebuild():    
    PackageHammer().uninstall()
    PackageHammer(directory=devdir).install()
    explode_egg_in_folder()
    print()
    print(" Starting building...")
    print(" (it can take a long time)")
    print()

def ExecuteSetup():
    #print(f"{Log.INFO} configuring the loggers ")
    #ConfigureFreezerLogging()
    cho = open(cxo_log, 'w')
    che = open(cxe_log, 'w')
    print(f"{Log.INFO} calling the setup()'s configurator")
    with RedirectStdStreams(stdout=cho, stderr=che):
        setup(
                name = "Blink Modulation Assistant",
                version = "0.1", #TODO
                description = '''O assistente para modulação de piscadas possibilita
                que uma pessoa portadora de ELA faça uso do NeuroSky
                Mindwave Mobile (versão 2) como dispositivo de
                entrada "switch" (F12) para o ACAT.''',
                executables = [
                    Executable('bma.py',
                        base = 'Win32GUI',
                        icon = 'icons/olho-aberto.ico')
                ],
                options = {
                    'build_exe': {
                        'include_files': [ 'icons/' ],
 
                    }
                }
            )
    print(f"{Log.INFO} call ended")

def ExecuteAfterBuild():  # unsed
    copy_all_icons_to_build()

if __name__ == '__main__':
    timer = Stopwatch()
    error_code = 0
    try: # prebuilding, and continue
        PutGlobalVariables()
        ExecutePrebuild()    
        timer.start()  # this goes up to the "finally" block (see there)
        ExecuteSetup()
        # building...
    except NotADirectoryError as nadE:
        print(f"{Log.ERROR} {nadE.strerror}")
        print(f"{Log.INFO} {nadE.filename}")
        error_code = nadE.errno
    except ImportError as ie:
        print(ie.msg)
        print(ie.name)
        print(ie.path)
        error_code = -3
    except Exception as e:
        #print(f"{Log.FATAL} serious failure, unhandled exception ")
        print(f"{Log.FATAL} {e}")
        error_code = -1
    finally:
        gap_in_words = timer.elapsed_time_for_humans()
        print()
        print(f"Stopwatch result: {gap_in_words}")
        if error_code:
            print()
            print("See records:")
            print(f" > {_tail_path_friendly(err_log)}")
            print(f" > {_tail_path_friendly(out_log)}")
            #print()
            sys.exit(error_code)