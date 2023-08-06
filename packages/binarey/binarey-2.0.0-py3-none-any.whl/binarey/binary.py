from functools import lru_cache
import argparse as _argparse
import json as _json
import os as _os

__doc__ = """
Binarey (binary) is used to convert any file to a binary file.
When converting a file to binary you can use a feature provided with
the binarey module that allows you to decrease the character size of each
binary file or simpily put compressing the file. All binarey compressed files
can also be decompressed and parsed to it's original form.

-- [FUNCTIONS] --
    [FUNCTION]: binary
        The binary function contains 2 parameters. param1 is a 'str' that will
        be converted to a binary 'list'. param2 is a 'bool' input that is used for
        converting the binary 'list' into a 'tuple' that can be used for compression.

        binary(str, bool) -> list or tuple
    
    [FUNCTION]: parse_binary
        The parse_binary function contains 1 parameter and does the opposite as
        the binary function. It takes in a binary 'list' or 'tuple' that then gets
        converted to a 'str'.

        parse_binary(list or tuple) -> str
    
    [FUNCTION]: compress_binary
        The compress_binary function contains 2 parameter: a binary 'list', and the depth level.
        It converts any inputed binary 'list' into a compress binary 'list'. Based on the depth (DEFAULT: 2)
        will either return a 2 level compression or a 1 level compression.

        compress_binary(list, depth) -> list
    
    [FUNCTION]: decompress_binary
        The decompress_binary function contains 1 parameter that is a binary 'tuple'.
        If the inputed param is not a 'tuple' an error will occur. The inputed binary 'tuple'
        will only be successfully decompressed if the inputed binary 'tuple' is a compressed
        binary 'tuple'. The function reverses the compression of any compressed binary 'tuple'.

        decompress_binary(tuple) -> list
    
    [CLASS]: Processor
        The Processor class allows you to either convert a file to binary or parse a binary file.
        The processor class requires a file and if the file is not a json file then it also
        requires a filename and run type.

        file: either a json file or the file that needs to be converted to binary or parsed
        filename[if no json file]: the filename requires an extension and if the base name used
        to create the new parsed or converted file.
        
        run: Must be set if no json file is provided and can only be set after the processor
        calls is created with the provided file and filename.
            processor = Processor(file, filename)
            processor.set_run_type(processor.RUN_BINARY or processor.RUN_PARSE)
        
        To execute the processor you must run processor.execute()

        When the processor.execute() method is called it will either create a new binary file
        or a new parsed binary file.

        The processor class allows you to implement settings that will change the output of
        the processor.execute() method.

        [RUN_BINARY SETTINGS]: 
            - compress (converts to binary -> compression[1] -> compression[2])
            - compress1 (converts to binary -> compression[1])
            - DEFAULT: binary
        
        [RUN_PARSE SETTINGS]:
            - decompress (decompression[1] -> decompression[2])
            - rawbinary (converts to binary)
            - rawbinary/ (converts to binary with each binary string seperated by a /)
            - DEFAULT: parsed binary string
        
        [JSON]:
            If the file provided is a JSON file it will try to use that file for execution.
            
            {
                "@compilerOptions": {
                    "@binarey": {
                        "run-file": <file>,
                        "new-filename": <filename>,
                        "run": "binary" or "parse",
                        "settings": ["compress", "compress1", "rawbinary", "rawbinary/"]
                    }
                },
                "@compiler": {
                    "@binarey": {
                        "run-file": <file>,
                        "new-filename": <filename>,
                        "run": "binary" or "parse",
                        "settings": ["compress", "compress1", "rawbinary", "rawbinary/"]
                    }
                },
                "@base": {
                    "@binarey": {
                        "run-file": <file>,
                        "new-filename": <filename>,
                        "run": "binary" or "parse",
                        "settings": ["compress", "compress1", "rawbinary", "rawbinary/"]
                    }
                },
                "@binarey": {
                    "run-file": <file>,
                    "new-filename": <filename>,
                    "run": "binary" or "parse",
                    "settings": ["compress", "compress1", "rawbinary", "rawbinary/"]
                }
            }
    
    [FUNCTION]: convert_file_to_binary
        Same as processor.execute() with the run function set to RUN_BINARY
    
    [FUNCTION]: parse_binary_file
        Same as processor.execute() with the run function set to RUN_PARSE
"""

__all__ = [
    "binary",
    "parse_binary",
    "compress_binary",
    "decompress_binary",
    "Processor",
    "convert_file_to_binary",
    "parse_binary_file",
    "compare_binary_files"
]

def binary(text: str, compression_format: bool = False) -> list | tuple:
    return [format(ord(char), "b") for char in text] if not compression_format else tuple([format(ord(char), "b") for char in text])

def parse_binary(_binary: list | tuple) -> str:
    return "".join(format(chr(int(b, 2))) for b in _binary)

@lru_cache(maxsize=2)
def __compress_binary(_binary: tuple) -> list:
    _l = {
        "0": {
            "2": "x",
            "3": "t",
            "4": "&",
            "5": "$"
        },
        "1": {
            "2": "i",
            "3": "g",
            "4": "_",
            "5": "%"
        }
    }

    def _c(i, c):
        return i < len(c)
    
    def _n(v):
        return isinstance(v, dict)
    
    def _i(b, i, r, e):
        # b -> binary string
        # i -> current index
        # r -> boolean count
        # e -> current char
        if i + r < len(b):
            return [b[_index+_r]==e for _r in range(1, r+1)].count(True) == r
        return False
    
    def _d(_c, _i):
        # _c -> char ("0", "1")
        # _i -> current index
        # (_c, _l[_c][_i])[_i > 1] -> (char, _l[char][index])[index > 1]
        # if index > 1 -> return _l[char("0", "1")][index] else return char
        return {"b": _c, "i": _i}

    def _si(_c, _s, _t, _f, _fi, _k):
        # _c -> char or index
        # _s -> second_character
        # _t -> third_character
        # _f -> fourth_character
        # _fi -> fifth_character
        # _k -> "b" or "i"
        # if fifth_character is not None -> fifth_character["b" or "i"] ("b": <string.letter>, "i": <index>)
        if _n(_fi): return _fi[_k]
        elif _n(_f): return _f[_k]
        elif _n(_t): return _t[_k]
        elif _n(_s): return _s[_k]
        else: return _c

    def next_c(_c, _i, _b2, _b1):
        # _c -> current char (_d param)
        # _i -> current index (_d param)
        # _b1 -> first ternary boolean
        # _b2 -> second teneray boolean
        # if index+1 < len(b): if [].count(True) == x: {"b": <letter>, "i": <index>} else None else None
        if _b1: 
            if _b2: return _d(_c, _i)
        return None

    _index, _string, _items = 0, "", []
    for b in _binary:
        while _index < len(b):
            _char = b[_index]

            if _char == "0" or _char == "1":
                _sc, _tc, _fc, _fic = \
                    next_c(_l[_char]["2"], 2, _i(b, _index, 1, _char), _c(_index+1, b)), \
                        next_c(_l[_char]["3"], 3, _i(b, _index, 2, _char), _c(_index+2, b)), \
                            next_c(_l[_char]["4"], 4, _i(b, _index, 3, _char), _c(_index+3, b)), \
                                next_c(_l[_char]["5"], 5, _i(b, _index, 4, _char), _c(_index+4, b))
                
                _string += _si(_char, _sc, _tc, _fc, _fic, "b")
                _index += _si(1, _sc, _tc, _fc, _fic, "i")
        _items.append(_string)
        _index, _string = 0, ""
    del _index, _string, _c, _n, _i, _d, _si, next_c
    return _items

def compress_binary(binary: list, depth: int = 2) -> list:
    if depth == 1:
        return __compress_binary(tuple(binary))
    elif not depth == 2:
        return ["ERR_INVALID_DEPTH_LVL"]
    items, repeated_chars, prev, cmpbin = [], [], "", __compress_binary(tuple(binary))
    for i in range(len(cmpbin)):
        char = cmpbin[i]

        if char == prev:
            repeated_chars.append(char)

        if len(repeated_chars) > 0 and not char == prev:
            items.append(f"{repeated_chars[0]}*{len(repeated_chars)}")
            items.append(char)
            repeated_chars = []
        else:
            if not len(repeated_chars) > 0:
                items.append(char)
        
        prev = char
    del prev, repeated_chars
    return items

@lru_cache(maxsize=2)
def decompress_binary(compressed_binary: tuple) -> list:
    _string, _items = "", []
    for c in __decompress_binary(compressed_binary):
        for _index in range(len(c)):
            _char = c[_index]

            _char_list = {
                "0": "0",
                "1": "1",
                "x": "00",
                "i": "11",
                "t": "000",
                "g": "111",
                "&": "0000",
                "_": "1111",
                "$": "00000",
                "%": "11111"
            }

            try:
                _string += _char_list[_char]
            except KeyError:
                pass
        _items.append(_string)
        _string = ""
    return _items

def __decompress_binary(compressed_binary: list) -> list:
    _items = []
    for c in compressed_binary:
        if not "*" in c:
            _items.append(c)
        elif "*" in c:
            c_list = c.split("*")
            for t in range(int(c_list[-1])):
                _items.append(c_list[0])
        else: _items.append(c)
    return _items

class _JsonParser:
    # Main: index.json, binary.json, binarey.json, config.json

    def __init__(self, _path: str):
        self._path = _path
    
    def _is_file_type(self, _file, _extension) -> bool:
        if _os.path.isfile(_file):
            name, extension = _os.path.splitext(_file)
            if extension == _extension:
                return True
        return False
    
    def read_json(self, json_file):
        with open(json_file) as _file:
            _json_data = _json.load(_file)
        
        _json_list, _json_comp = [
            "@compilerOptions", "@compiler",
            "@base", "@binarey"
        ], None
        for _val in _json_list:
            if _val in _json_data:
                _json_comp = _val
                break
        
        return _json_data[_json_list[-1]] if _json_comp == _json_list[-1] else _json_data[_json_comp]["@binarey"]

class Processor(_JsonParser):
    BINARY_BASE_NAME = "-binary"
    PARSED_BASE_NAME = "-parsed"
    RUN_BINARY = "convert->binary"
    RUN_PARSE = "convert->parse"

    def __init__(self, file: str, filename: str, settings: list = None):
        _msg = "Invalid type for argument \"{}\" expected: 'str' got '{}'"

        if not isinstance(file, str):
            raise TypeError(_msg.format("file", type(file)))
        
        if not isinstance(filename, (str, type(None))):
            raise TypeError(_msg.format("filename", type(filename)))
        
        extension = None
        try:
            extension = filename.split(".")[1]
        except (IndexError, AttributeError):
            if not filename is None:
                raise TypeError("Filename should contain an extension.")

        self._file = file
        self._filename = filename.split(".")[0] if not filename is None else None
        self._run = None
        self._settings = None
        self._extension = extension
    
    def __process_json_file(self):
        _json_settings = super().read_json(self._file)
        _json_file = self._file
        _json_bool = ["run-file" in _json_settings, "new-filename" in _json_settings, 
                "run" in _json_settings, "settings" in _json_settings]
        if _json_bool.count(True) >= 3:
            def _err(ex, msg): raise ex(msg)
            _filename_json = _json_settings["new-filename"]
            self._file = _json_settings["run-file"]
            self._filename = _filename_json.split(".")[0] if "." in _filename_json else _err(TypeError, "new-filename should contain an extension.")
            self._run = ((self.RUN_PARSE if _json_settings["run"] == "parse" else None), 
                self.RUN_BINARY)[_json_settings["run"] == "binary"]
            self._extension = _filename_json.split(".")[1] if "." in _filename_json else "txt"
            self._settings = _json_settings["settings"] if _json_bool[-1] else None
            return
        class JSONMissingArgumentsError(Exception): pass
        err_msg_format_data = [
            _json_file,
            0 if _json_bool[0] else 1,
            0 if _json_bool[1] else 1,
            0 if _json_bool[2] else 1,
            0 if _json_bool[3] else None
        ]
        raise JSONMissingArgumentsError(
            "Json file: \"{}\" ethier contains invalid or missing arguments. (0: Found, 1: Invalid); \n\"run-file\": {}, \"new-filename\": {}, \"run\": {}, \"*settings\": {}".format(*err_msg_format_data))

    def set_run_type(self, run: str) -> None:
        if not isinstance(run, str) or not [run == self.RUN_BINARY, run == self.RUN_PARSE].count(True) > 0:
            _msg = "Invalid argument \"{}\" expected: (RUN_BINARY or RUN_PARSE) got '{}'"
            raise TypeError(_msg.format("run", run))
        self._run = run

    def set_settings(self, settings: list = None) -> None:
        if not isinstance(settings, (list, type(None))):
            raise TypeError(f"Processor.set_settings(): Settings argument expected a list or none.")
        self._settings = settings

    def __parse_settings(self) -> list:
        if isinstance(self._settings, type(None)):
            return [self._settings]
        return self._settings

    def __create_file(self, filename_addon: str = None):
        _file_name = self._filename + self._extension
        if not filename_addon == None:
            _file_name = f"{self._filename}{filename_addon}.{self._extension}"
        
        if not _os.path.exists(_file_name):
            with open(_file_name, "x") as new_file:
                new_file.close()
        return _file_name

    def __convert_to_binary(self):
        with open(self._file, "r") as file_to_convert:
            file_binary = file_to_convert.read()
        
        _binary = binary(file_binary, True)
        settings = self.__parse_settings()
        if "compress" in settings:
            _binary = compress_binary(binary(file_binary, True))
        
        if "compress1" in settings:
            _binary = compress_binary(binary(file_binary, True), 1)

        with open(self.__create_file(self.BINARY_BASE_NAME), "w") as binary_file:
            binary_file.write("/".join(_binary))
    
    def __parse_binary_file(self):
        with open(self._file, "r") as file_to_parse:
            _items = tuple(str(file_to_parse.read()).split("/"))
        settings = self.__parse_settings()
        _split = "/" if "rawbinary/" in settings else ""
        _parsed_binary = (parse_binary(decompress_binary(_items)), decompress_binary(_items))["rawbinary" in settings or "rawbinary/" in settings]

        with open(self.__create_file(self.PARSED_BASE_NAME), "w") as parse_file:
            parse_file.write(_split.join(_parsed_binary))
            del _items, settings, _split
    
    def execute(self):
        print(_os.path.join(_os.getcwd(), self._file))
        if super()._is_file_type(self._file, ".json"):
            self.__process_json_file()

        if self._run == self.RUN_BINARY:
            self.__convert_to_binary()
        elif self._run == self.RUN_PARSE:
            self.__parse_binary_file()
        else:
            raise TypeError("Invalid \"run\" command. Expected (RUN_BINARY or RUN_PARSE) got \"{}\"".format(self._run))

def convert_file_to_binary(file: str, filename: str, settings: str = None) -> "dict[str, int]":
    if not [isinstance(file, str), isinstance(filename, str)].count(True) > 0:
        return {"status": 1}
    
    binary_converter = Processor(file, filename)
    binary_converter.set_run_type(binary_converter.RUN_BINARY)
    binary_converter.set_settings(settings)
    binary_converter.execute()
    return {"status": 0}

def parse_binary_file(file: str, filename: str, settings: list = None):
    if not [isinstance(file, str), isinstance(filename, str)].count(True) > 0:
        return {"status": 1}
    
    binary_parser = Processor(file, filename)
    binary_parser.set_run_type(binary_parser.RUN_PARSE)
    binary_parser.set_settings(settings)
    binary_parser.execute()
    return {"status": 0}

def compare_binary_files(binary_file: str, __binary_file: str) -> object:
    class _binary_compare_output(object):
        def __init__(self,
            binary_file_size, binary_file_length, __binary_file_size, __binary_file_length,
            smaller_file_size_name, smaller_file_length_name, smaller_file_size, smaller_file_length, 
            larger_file_size_name, larger_file_length_name, larger_file_size, larger_file_length,
            file_differences
        ):
            self.first_binary_file_size = binary_file_size
            self.first_binary_file_length = binary_file_length

            self.second_binary_file_size = __binary_file_size
            self.second_binary_file_length = __binary_file_length

            self.smaller_file_size_name = smaller_file_size_name
            self.smaller_file_length_name = smaller_file_length_name
            self.smaller_file_size = smaller_file_size
            self.smaller_file_length = smaller_file_length

            self.larger_file_size_name = larger_file_size_name
            self.larger_file_length_name = larger_file_length_name
            self.larger_file_size = larger_file_size
            self.larger_file_length = larger_file_length

            self.file_size_difference = file_differences["size"]
            self.file_length_difference = file_differences["length"]
    
    with open(binary_file, "r") as first_binary_file:
        fbf_length = len(str(first_binary_file.read()))
        fbf_size = _os.path.getsize(binary_file)
    
    with open(__binary_file, "r") as second_binary_file:
        sbf_length = len(str(second_binary_file.read()))
        sbf_size = _os.path.getsize(__binary_file)

    _smaller_file_size, _smaller_file_length, \
        _larger_file_size, _larger_file_length, \
            _smaller_file_size_name, _smaller_file_length_name, \
                _larger_file_size_name, _larger_file_length_name, \
                    file_differences = None, None, None, None, \
                        None, None, None, None, {
                            "size": abs(fbf_size-sbf_size),
                            "length": abs(fbf_length-sbf_length)
                        }

    if fbf_length < sbf_length:
        _smaller_file_length = fbf_length
        _smaller_file_length_name = binary_file
        _larger_file_length = sbf_length
        _larger_file_length_name = __binary_file
    elif fbf_length > sbf_length:
        _smaller_file_length = sbf_length
        _smaller_file_length_name = __binary_file
        _larger_file_length = fbf_length
        _larger_file_length_name = binary_file
    
    if fbf_size < sbf_size:
        _smaller_file_size = fbf_size
        _smaller_file_size_name = binary_file
        _larger_file_size = sbf_size
        _larger_file_size_name = __binary_file
    elif fbf_size > sbf_size:
        _smaller_file_size = sbf_size
        _smaller_file_size_name = __binary_file
        _larger_file_size = fbf_size
        _larger_file_size_name = binary_file
    
    _comparision_data = _binary_compare_output(
        fbf_size, fbf_length, sbf_size, sbf_length,
        _smaller_file_size_name, _smaller_file_length_name,
        _smaller_file_size, _smaller_file_length,
        _larger_file_size_name, _larger_file_length_name,
        _larger_file_size, _larger_file_length,
        file_differences
    )
    return _comparision_data

def _on_run(file, filename, run, settings) -> None:
    processor = Processor(file, filename)

    if run == "binary":
        processor.set_run_type(processor.RUN_BINARY)
    elif run == "parse":
        processor.set_run_type(processor.RUN_PARSE)
    
    processor.set_settings(settings)
    processor.execute()

def main():
    parser = _argparse.ArgumentParser()
    parser.add_argument("-file", type=str, required=True)
    parser.add_argument("-filename", type=str, required=False)
    parser.add_argument("-run", type=str, required=False)
    parser.add_argument("--settings", type=str, nargs="*", required=False)

    args = parser.parse_args()
    _on_run(file=args.file, filename=args.filename, run=args.run, settings=args.settings)

if __name__ == "__main__":
    main()