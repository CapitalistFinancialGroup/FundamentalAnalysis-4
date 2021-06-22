"""
=========
Helper functions
=========
This file includes functionalities to aide the library in its functionality.
"""
import yaml
import logging

def __prepare_configuration() -> dict:
    """
    Reads and prepares the configuration
    Returns
    -------
    config (dict) : Dictionary containing the configurations
    """

    logging.info("Reading configuration file")

    with open('../resources/configuration.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    return config

config = __prepare_configuration()

def resolve_config_value(keys):
    """
    Resolves and returns the particular configuration value
    Parameters
    ----------
    keys : @list
           List of keys as it is embedded

    Returns
    -------
    @obj : the configuration value
    """

    config_value = config
    for key in keys:
        config_value = config_value[key]

    return config_value

