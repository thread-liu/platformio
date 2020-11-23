import os
import sys
import shutil
import logging



def init_logger():
    log_format = " %(filename)s %(lineno)d <ignore> %(levelname)s %(message)s "
    date_format = '%Y-%m-%d  %H:%M:%S %a '
    logging.basicConfig(level=logging.INFO,
                        format=log_format,
                        datefmt=date_format
                        )


def do_copy_file(src, dst):
    if not os.path.exists(src):
        raise Exception("ERROR: Can’t get resource {0}, please check the resource.".format(src))

    file_dir_path = os.path.dirname(dst)
    if not os.path.exists(file_dir_path):
        os.makedirs(file_dir_path)

    try:
        shutil.copy2(src, dst)
    except Exception as e:
        logging.error("Error Message: {0}".format(e))
        raise Exception("ERROR: Can‘t copy resource {0}.".format(src))

    return True


def platformio_test(cwd):
    os.mkdir(os.path.join(cwd, "test"))
    do_copy_file(os.path.join(cwd, "dist", "platformio.exe"), os.path.join(cwd, "platformio.exe"))
    do_copy_file(os.path.join(cwd, "dist", "pio.exe"), os.path.join(cwd, "pio.exe"))
    do_copy_file(os.path.join(cwd, "dist", "piodebuggdb.exe"), os.path.join(cwd,"piodebuggdb.exe"))
    os.system("pio boards")
    os.system("platformio boards")
    os.system("platformio init --board nucleo_h743zi --ide=eclipse --project-option framework=cmsis --project-dir test")
    os.system("platformio -f -c eclipse run --project-dir test")
    os.system("platformio -f -c eclipse run --target clean --project-dir test")
    
    return 0

def win_release_to_oss():
    try:
        if os.system(r'ossutil64 -c %FILE_OSSUTILCONFIG% cp -r -f release_platformio oss://realthread-download/rt-studio/backend/') != 0:
            raise Exception('Deploy to oss fail.')
    except OSError:
        raise Exception('Deploy command executes fail.')


def release():
    try:
        os.system(r'pyinstaller --clean --win-private-assemblies  -F ./platformio.py -i ./platformio-logo.ico  --hiddenimport xmltodict')
        os.system(r'pyinstaller --clean --win-private-assemblies  -F ./pio.py -i ./platformio-logo.ico  --hiddenimport xmltodict')
        os.system(r'pyinstaller --clean --win-private-assemblies  -F ./piodebuggdb.py -i ./platformio-logo.ico  --hiddenimport xmltodict')
        os_type = sys.platform
        logging.info("os type : {0}".format(os_type))
        cwd = os.getcwd()
        if os_type.find("linux") != -1:
            pass
        else:
            do_copy_file(os.path.join(cwd, "dist", "platformio.exe"), os.path.join(cwd, "release_platformio", "platformio.exe"))
            do_copy_file(os.path.join(cwd, "dist", "pio.exe"), os.path.join(cwd, "release_platformio", "pio.exe"))
            do_copy_file(os.path.join(cwd, "dist", "piodebuggdb.exe"), os.path.join(cwd, "release_platformio", "piodebuggdb.exe"))

        logging.info(os.listdir(os.path.join(cwd, "release_platformio")))

    except Exception as e:
        logging.error("Error message : {0}".format(e))

    platformio_test(cwd)
    win_release_to_oss()

    return 0



def main():
    init_logger()
    release()


if __name__ == "__main__":
    sys.exit(main())