"""Setup the DODGR application"""
import logging

from dodgr.config.environment import load_environment
from dodgr.model import meta

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup dodgr here"""
    load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    meta.metadata.create_all(bind=meta.engine)
