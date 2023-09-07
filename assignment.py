class Data:
    def __init__(self, **kwargs):
        self._data = {}
        self._default_value = {}
        for key, value in kwargs.items():
            setattr(self, key, value)
    @classmethod
    def from_dict(cls, data):
        instance = cls()
        for key, value in data.items():
            if isinstance(value, dict):
                instance._data[key] = cls.from_dict(value)
            else:
                instance._data[key] = value
        return instance
    def to_dict(self):
        output = {}
        for key, value in self._data.items():
            if isinstance(value, Data):
                output[key] = value.to_dict()
            else:
                output[key] = value
        return output
    
    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        # Begin new code: 
        matches = [key for key in self._data if key.startswith(name)]
        if len(matches) == 1:  # only one matching attribute
            return self._data[matches[0]]
        # End new code
        elif name in self._default_value:
            return self._default_value[name]
        else:
            return None
            # raise AttributeError(f"'Data' object has no attribute '{name}'")
    def __setattr__(self, name, value):
        if name in ['_data', '_default_value']:
            super().__setattr__(name, value)
        else:
            if not hasattr(self, '_data'):
                self._data = {}
            if isinstance(value, (dict, Data)):
                self._data[name] = Data.from_dict(value if isinstance(value, dict) else value.to_dict())
            else:
                self._data[name] = value


data = {
    "id": "1",
    "name": "first",
    "metadata": {
        "system": {
            "size": 10.7
        },
        "user": {
            "batch": 10
        }
    }
}
# load data from dict
my_inst_1 = Data.from_dict(data)
print(my_inst_1.metadata.system.size)  # Reflects inner value as well

# load from inputs
my_inst_2 = Data(name="my", email="aamirsaggi@gmail.com")

print(my_inst_2._data)

# Default values
print(my_inst_1.metadata.system.height)  # prints None
my_inst_1.metadata.system.height = 100  # Set a default value of 100
print(my_inst_1.to_dict()['metadata']['system']['height'])  # prints 100

# # Autocomplete
print(my_inst_1.metadata.user.batch)  # prints 10
print(my_inst_1.metadata.system.s)  # Autocompletes to "size"