#  Copyright (c) 2018 PaddlePaddle Authors. All Rights Reserve.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    from configparser import ConfigParser
except BaseException:
    from ConfigParser import ConfigParser

import logging

CONFIG_SECS = [
    'train',
    'valid',
    'test',
    'infer',
]


def parse_config(cfg_file):
    """parse_config"""
    parser = ConfigParser()
    cfg = AttrDict()
    parser.read(cfg_file)
    for sec in parser.sections():
        sec_dict = AttrDict()
        for k, v in parser.items(sec):
            try:
                v = eval(v)
            except BaseException:
                pass
            setattr(sec_dict, k, v)
        setattr(cfg, sec.upper(), sec_dict)

    return cfg


def merge_configs(cfg, sec, args_dict):
    """merge_configs"""
    assert sec in CONFIG_SECS, "invalid config section {}".format(sec)
    sec_dict = getattr(cfg, sec.upper())
    for k, v in args_dict.items():
        if v is None:
            continue
        try:
            if hasattr(sec_dict, k):
                setattr(sec_dict, k, v)
        except BaseException:
            pass
    return cfg


def print_configs(cfg, mode):
    """print_configs"""
    logger = logging.getLogger(__name__)
    logger.info(
        "---------------- {:>5} Arguments ----------------".format(mode))
    for sec, sec_items in cfg.items():
        logger.info("{}:".format(sec))
        for k, v in sec_items.items():
            logger.info("    {}:{}".format(k, v))
    logger.info("-------------------------------------------------")


class AttrDict(dict):
    """AttrDict"""
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value
        else:
            self[key] = value
