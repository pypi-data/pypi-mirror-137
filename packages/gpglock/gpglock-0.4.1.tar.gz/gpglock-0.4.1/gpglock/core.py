#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import gnupg
import hashlib
import os
import subprocess
from .utils.console_logging_formatter import get_formatted_console_logger

logger = get_formatted_console_logger("gpglocker")


def __is_dir_inited(dir_path):
    config_path = os.path.join(dir_path, ".gpglock")
    return os.path.isfile(config_path)


def __get_search_list(dir_path):
    config_path = os.path.join(dir_path, ".gpglock")
    if os.path.isdir(config_path):
        logger.error("Cannot load config, the path for .gpglock is occupied by a directory.")

    res = []
    with open(config_path, 'r') as config_file:
        lines = config_file.readlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            res.append(line)

    return res


def __digest_binary_hash(data):
    return hashlib.sha1(data).hexdigest()
        

def __digest_file_hash(filepath):
    with open(filepath, "rb") as opened_file:
        return __digest_binary_hash(opened_file.read())


def __encrypt_file(gpg, filepath, recipient):
    stream = open(filepath, "rb")
    res = gpg.encrypt_file(stream, recipient)
    return res.data


def __decrypt_file(gpg, filepath):
    stream = open(filepath, "rb")
    res = gpg.decrypt_file(stream)
    return res.data


def __lock_file(gpg, dir, clear_file, recipient):
    clear_file_realpath = os.path.realpath(os.path.join(dir, clear_file))
    encrypted_file = "%s.asc" % clear_file
    encrypted_file_realpath = "%s.asc" % clear_file_realpath

    if not os.path.isfile(clear_file_realpath):
        logger.warning("Invalid file to encrypt: %s" % clear_file)
        return
    
    if os.path.isdir(encrypted_file_realpath):
        logger.error("Invalid path to encrypt: %s" % encrypted_file)
        return

    if os.path.isfile(encrypted_file_realpath):
        existing_data = __decrypt_file(gpg, encrypted_file_realpath)
        existing_hash = __digest_binary_hash(existing_data)
        pending_hash = __digest_file_hash(clear_file_realpath)
        if pending_hash == existing_hash:
            logger.info("No content change: %s" % clear_file)
            return

    encrypted_data = __encrypt_file(gpg, clear_file_realpath, recipient)

    with open(encrypted_file_realpath, 'wb') as target_file:
        target_file.write(encrypted_data)
    logger.info("Locked %s" % clear_file)


def __unlock_file(gpg, dir, clear_file):
    clear_file_realpath = os.path.realpath(os.path.join(dir, clear_file))
    encrypted_file = "%s.asc" % clear_file
    encrypted_file_realpath = "%s.asc" % clear_file_realpath

    if not os.path.isfile(encrypted_file_realpath):
        logger.warning("Invalid file to decrypt: %s" % encrypted_file)
        return
    
    if os.path.isdir(clear_file_realpath):
        logger.error("Invalid path to decrypt: %s" % clear_file)
        return

    clear_data = __decrypt_file(gpg, encrypted_file_realpath)

    with open(clear_file_realpath, 'wb') as target_file:
        target_file.write(clear_data)
    logger.info("Unlocked %s" % clear_file)


def __get_gpg_info():

    gpg_home = None
    default_recipient = None

    try:
        gpg = subprocess.Popen(["gpg", "--version"], stdout=subprocess.PIPE)
        output = gpg.communicate()[0].decode('ascii')
        for line in output.split("\n"):
            if line.startswith("Home:"):
                gpg_home = line[6:]
                gpg_conf = os.path.join(gpg_home, "gpg.conf")
                with open(gpg_conf) as gog_conf_file:
                    for line in gog_conf_file.readlines():
                        keypair = line.strip().split(" ")
                        if len(keypair)!=2:
                            continue
                        key = keypair[0].strip()
                        if(key == "default-recipient"):
                            default_recipient = keypair[1].strip()
                            break
    except FileNotFoundError as e:
        pass

    return {
                "gpgHome": gpg_home,
                "defaultRecipient": default_recipient
            }

def init_dir(dir_path):
    if not os.path.isdir(dir_path):
        logger.error("Invalid dir: %s" % dir_path)
        return

    gpg_info = __get_gpg_info()
    if not gpg_info["gpgHome"]:
        logger.error("Failed fetching gpg home, make sure gpg is installed.")
        return

    gpg = gnupg.GPG()
    gpg.encoding = 'utf-8'
    print(gpg.gnupghome)
    public_keys = gpg.list_keys()

    if __is_dir_inited(dir_path):
        logger.error("Current working directory is already initialised.")
        return

    TEMPLATE = """# List secret files which need to be locked below.

# example:
# ./secret.txt
# ./sub-folder/token.conf
# ...

"""

    config_path = os.path.join(dir_path, ".gpglock")
    with open(config_path, "w") as config_file:
        config_file.write(TEMPLATE)
    
    logger.info("Init succeeded, check [.gpglock] and add secret files to lock.")
    

def lock_dir(dir_path):
    if not os.path.isdir(dir_path):
        logger.error("Invalid dir: %s" % dir_path)
        return

    if not __is_dir_inited(dir_path):
        logger.error("Current working directory has not been initialised, run [gpglock init] first.")
        return

    gpg_info = __get_gpg_info()
    if not gpg_info["gpgHome"]:
        logger.error("Failed fetching gpg home, make sure gpg is installed.")
        return

    if not gpg_info["defaultRecipient"]:
        logger.error("Failed loading default recipient, please add [default-recipient email-address] to [gpg.conf] in [%s]." % gpg_info["gpgHome"])
        return
    
    gpg = gnupg.GPG()
    gpg.encoding = 'utf-8'

    searching_list = __get_search_list(dir_path)

    if not len(searching_list):
        logger.info("No specific file to lock.")
        return

    for searching_item in searching_list:
        __lock_file(gpg, dir_path, searching_item, gpg_info["defaultRecipient"])


def unlock_dir(dir_path):
    if not os.path.isdir(dir_path):
        logger.error("Invalid dir: %s" % dir_path)
        return

    if not __is_dir_inited(dir_path):
        logger.error("Current working directory has not been initialised, run [gpglock init] first.")
        return

    gpg_info = __get_gpg_info()
    if not gpg_info["gpgHome"]:
        logger.error("Failed fetching gpg home, make sure gpg is installed.")
        return

    gpg = gnupg.GPG()
    gpg.encoding = 'utf-8'

    searching_list = __get_search_list(dir_path)

    if not len(searching_list):
        logger.info("No specific file to unlock.")
        return

    for searching_item in searching_list:
        __unlock_file(gpg, dir_path, searching_item)
