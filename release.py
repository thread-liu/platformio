import os
import sys
import json
import shutil
import logging
import tarfile


def init_logger():
    log_format = " %(filename)s %(lineno)d <ignore> %(levelname)s %(message)s "
    date_format = '%Y-%m-%d  %H:%M:%S %a '
    logging.basicConfig(level=logging.INFO,
                        format=log_format,
                        datefmt=date_format
                        )


def do_remove_folder(dst_dir):
    try:
        if os.path.exists(dst_dir):
            shutil.rmtree(dst_dir)
    except Exception as e:
        logging.error("Error message : {0}.".format(e))
        raise Exception("ERROR: Can‘t delete folder {0}, please check the resource.".format(dst_dir))
    return True


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


def do_copy_folder(src_dir, dst_dir, ignore=None):
    if not os.path.exists(src_dir):
        raise Exception("ERROR: Can’t get resource {0}, please check the resource.".format(src_dir))

    try:
        shutil.copytree(src_dir, dst_dir, ignore=ignore)
    except Exception as e:
        logging.error("Error message: {0}".format(e))
        raise Exception("ERROR: Copy {0} failed.".format(src_dir))

    return True


def platformio_test(cwd):
    do_copy_file(os.path.join(cwd, "dist", "platformio.exe"), os.path.join(cwd, "platformio.exe"))
    do_copy_file(os.path.join(cwd, "dist", "pio.exe"), os.path.join(cwd, "pio.exe"))
    do_copy_file(os.path.join(cwd, "dist", "piodebuggdb.exe"), os.path.join(cwd,"piodebuggdb.exe"))

    if os.system("pio --version") != 0:
        sys.exit(1)

    logging.info("list all platformio boards :")
    os.system("pio boards")

    logging.info("create a arduino project, works at Eclipse IDE :")
    os.mkdir(os.path.join(cwd, "prj_nucleo_h743zi"))
    os.system("platformio init --board nucleo_h743zi --ide=eclipse --project-option framework=cmsis --project-dir prj_nucleo_h743zi")

    logging.info("build project :")
    os.system("platformio -f -c eclipse run --project-dir prj_nucleo_h743zi")

    logging.info("clean project :")
    os.system("platformio -f -c eclipse run --target clean --project-dir prj_nucleo_h743zi")

    return 0


def make_targz(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def release():
    """ release platformio core"""
    try:
        os.system(r'pyinstaller --clean --win-private-assemblies  '
                  r'-F ./platformio.py -i ./platformio-logo.ico  --hiddenimport xmltodict')
        os.system(r'pyinstaller --clean --win-private-assemblies  '
                  r'-F ./pio.py -i ./platformio-logo.ico  --hiddenimport xmltodict')
        os.system(r'pyinstaller --clean --win-private-assemblies  '
                  r'-F ./piodebuggdb.py -i ./platformio-logo.ico  --hiddenimport xmltodict')
        logging.info("os type : {0}".format(sys.platform))
        cwd = os.getcwd()

        do_copy_file(os.path.join(cwd, "dist", "platformio.exe"),
                     os.path.join(cwd, "release_platformio", "platformio.exe"))
        do_copy_file(os.path.join(cwd, "dist", "pio.exe"),
                     os.path.join(cwd, "release_platformio", "pio.exe"))
        do_copy_file(os.path.join(cwd, "dist", "piodebuggdb.exe"),
                     os.path.join(cwd, "release_platformio", "piodebuggdb.exe"))
        do_copy_folder(os.path.join(cwd, "platformio_core"),
                       os.path.join(cwd, "release_platformio", "platformio_core"))

        logging.info(os.listdir(os.path.join(cwd, "release_platformio")))
        do_remove_folder(os.path.join(cwd, "platformio_core", "Scripts"))

    except Exception as e:
        logging.error("Error message : {0}".format(e))
        sys.exit(1)

    platformio_test(cwd)

    return 0


def update_platformio_core(json_path):
    try:
        with open(json_path, 'r') as f:
            json_data = json.load(f)
    except Exception as e:
        logging.error(e)
        sys.exit(1)

    if len(json_data) == 0:
        return 0

    latest_version = None
    old_version = None
    for package in json_data:
        for key, value in package.items():
            if (key == "name") and (value == "platformio"):
                latest_version = package['latest_version']
                old_version = package['version']
                break

    logging.info("platformio will upgrade {0} ==> {1}".format(old_version, latest_version))
    cmd = "python.exe -m pip install -U platformio=={0} --no-warn-script-location".format(latest_version)
    logging.info(cmd)
    os.system(cmd)


def install_platformio_core():
    """ update platformio version """
    old_path = os.getcwd()
    os.chdir(os.path.join(old_path, "platformio_core"))
    os.system("python.exe get-pip.py")
    if os.system("python.exe -m pip install platformio --no-warn-script-location") != 0:
        sys.exit(1)
    os.system("python.exe -m pip list")

    os.system("python.exe -m pip list --outdated --format=json > py_pip.json")
    json_path = os.path.join(old_path, "platformio_core", "py_pip.json")
    update_platformio_core(json_path)

    os.system("python.exe -m pip list")
    os.chdir(old_path)

    return 0


def main():
    init_logger()
    install_platformio_core()
    release()

    return 0


if __name__ == "__main__":
    sys.exit(main())
