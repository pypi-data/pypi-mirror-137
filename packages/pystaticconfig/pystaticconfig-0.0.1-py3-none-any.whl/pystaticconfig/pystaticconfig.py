import json
import os


class BaseConfig:
    """Base class for config. Creates file with name stored in `_config_location`. 
    Class is static so it doesn't need to be instantiated. 

    Private fiels starting with underscore (like `_config_location`) won't
    be saved in JSON file. Other public attributes will be stored in file. 

    Inherit from `BaseConfig` for creating your own config. Like this:
    ```python
    class Config(BaseConfig):

    
    ```
    """
    # values starting with '_' will not be included in the json config file
    _config_location = 'config.json'

    @classmethod
    def attributes(cls):
        """Method for getting all public attributes of config class

        Returns:
            dict of pairs `{attribute: value}` 
        """
        return {attr: val for attr, val in cls.__dict__.items() if not attr.startswith("_") and not isinstance(val, classmethod)}

    @classmethod
    def load(cls):
        """Call this method to load all attributes from JSON file saved 
        at `_config_location`
        """
        if os.path.exists(cls._config_location):
            attrs = cls.attributes()
            data = {attr: val for attr, val in json.load(open(cls._config_location, "r")).items() if attr in attrs}
            for k, v in data.items():
                setattr(cls, k, v)

    @classmethod
    def save(cls):
        """Call this method to save all public attributes to JSON file 
        at location `_config_location`
        """
        json.dump(cls.attributes(), open(cls._config_location, 'w'), sort_keys=True, indent=4)

