import datetime
import logging
import os
import re

import docums.structure
from docums import utils
from docums.config import config_options
from docums.plugins import BasePlugin

logger = logging.getLogger("docums.plugin.select-files")


class SelectFiles(BasePlugin):

    config_scheme = (
        ('disabled_if_env', config_options.Type(utils.string_types)),
        ('select', config_options.Type(utils.string_types, default='(\d+)')),
        ('where', config_options.Type(
            utils.string_types, default='lambda x: int(x) >= 0')),
    )

    def __init__(self):
        self.disabled = False

    def on_config(self, config):
        if 'disabled_if_env' in self.config:
            env_name = self.config['disabled_if_env']
            if env_name:
                self.disabled = os.environ.get(env_name) == '1'
                if self.disabled:
                    logger.warning(
                        'select-file is disabled (set environment variable %s to 0 to enable)', env_name)

    def on_files(self, files, **kwargs):
        if self.disabled:
            return files

        logger.debug("Filtering files")
        # some variables that the user can use in the select lambda:
        global_vars = {
            'now' : datetime.datetime.isoformat(datetime.datetime.now()),
            'sfc' : os.getenv('SELECT_FILE_CONDITION'),
        }

        try:
            select = re.compile(self.config["select"])
        except Exception as e:
            logger.error("Error parsing select regular expression : %s", e)
            return files

        try:
            where = eval(self.config["where"], global_vars)
        except Exception as e:
            logger.error("Error evaluating where expression : %s", e)
            return files

        def ok(path):
            m = select.search(path)
            if m:
                args = m.groups()
                if where(*args):
                    logger.debug("MATCH : %s", path)
                    return True
                else:
                    logger.debug("DROP : %s", path)
                    return False
            else:
                logger.debug("PASS : %s", f.src_path)
                return True

        res = []
        for f in files:
            try:
                t = ok(f.src_path)
            except Exception as e:
                logger.error("Error evaluating regular expression : %s", e)
                t = True

            if t:
                res.append(f)

        return docums.structure.files.Files(res)
