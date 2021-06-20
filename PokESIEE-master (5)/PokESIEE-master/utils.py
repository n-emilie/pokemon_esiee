from typing import Any,Dict

class PokemonParseError(Exception):

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "PokemonParseError, {} ".format(self.message)
        else:
            return "PokemonParseError has been raised"


def get_args(data: Dict[str, Any], key: str, _id: Any, default=None, type_check=None, _type="pokemon")-> Any:
    value = None
    if default is not None:
        value = data[key] if key in data else None if default == "NONE" else default
    else:
        if key not in data:
            raise PokemonParseError("No {} value for a {} ({}) !".format(key, _type, _id))
        value = data[key]
    if type_check:
        if value and not isinstance(value, type_check):
            raise PokemonParseError("Invalid var type for {} need be {} for {} ({})".format(key, type_check, _type, _id))
    return value