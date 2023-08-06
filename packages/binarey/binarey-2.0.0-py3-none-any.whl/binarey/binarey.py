import argparse as _argparse

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

def binary(text: str) -> list:
    return [format(ord(char), "b") for char in text]

def compress_binary(_binary: list) -> list:
    _compress_letters = {
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
    _index, _string, _items = 0, "", []
    for b in _binary:
        while _index < len(b):
            _char = b[_index]

            if _char == "0" or _char == "1":
                _second_char, _third_char, _fourth_char, _fifth_char = None, None, None, None
                if _index + 1 < len(b):
                     if b[_index+1]==_char:
                        _second_char = b[_index + 1]
                if _index + 2 < len(b):
                     if [b[_index+1]==_char,b[_index+2]==_char].count(True) == 2:
                        _third_char = b[_index + 2]
                if _index + 3 < len(b):
                     if [b[_index+1]==_char,b[_index+2]==_char,\
                            b[_index+3]==_char].count(True) == 3:
                        _fourth_char = b[_index + 3]
                if _index + 4 < len(b):
                    if [b[_index+1]==_char,b[_index+2]==_char,\
                            b[_index+3]==_char,b[_index+4]==_char].count(True) == 4:
                        _fifth_char = b[_index + 4]
                
                if not _fifth_char is None:
                    _string += _compress_letters[_char]["5"]
                    _index += 5
                elif not _fourth_char is None:
                    _string += _compress_letters[_char]["4"]
                    _index += 4
                elif not _third_char is None:
                    _string += _compress_letters[_char]["3"]
                    _index += 3
                elif not _second_char is None:
                    _string += _compress_letters[_char]["2"]
                    _index += 2
                else: 
                    _string += _char
                    _index += 1
            else:
                _index += 1
        _items.append(_string)
        _index = 0
        _string = ""
    return _items

def decompress_binary(compressed_binary: list) -> list:
    _index, _string, _items = 0, "", []
    for c in compressed_binary:
        while _index < len(c):
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
                if _char in _char_list:
                   _string += _char 
            _index += 1
        _items.append(_string)
        _index = 0
        _string = ""
    return _items

def parse_binary(_binary: list) -> str:
    return "".join(format(chr(int(b, 2))) for b in _binary)

class Processor:
    BINARY_BASE_NAME = "-binary"
    PARSED_BASE_NAME = "-parsed"
    RUN_BINARY = "convert->binary"
    RUN_PARSE = "convert->parse"

    def __init__(self, file: str, filename: str, settings: list = None):
        _msg = "Invalid type for argument \"{}\" expected: 'str' got '{}'"

        if not isinstance(file, str):
            raise TypeError(_msg.format("file", type(file)))
        
        if not isinstance(filename, str):
            raise TypeError(_msg.format("filename", type(filename)))
        
        try:
            extension = filename.split(".")[1]
        except IndexError:
            raise TypeError("Filename should contain an extension.")

        self._file = file
        self._filename = filename.split(".")[0]
        self._run = None
        self._settings = None
        self._extension = extension
    
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
        
        if not __import__("os").path.exists(_file_name):
            with open(_file_name, "x") as new_file:
                new_file.close()
        
        return _file_name

    def __convert_to_binary(self):
        with open(self._file, "r") as file_to_convert:
            file_binary = file_to_convert.read()
        
        _binary = compress_binary(binary(file_binary))
        settings = self.__parse_settings()
        if "compress" in settings:
            _binary = compress_binary(binary(file_binary))
        
        if "rawbinary" in settings:
            _binary = binary(file_binary)

        with open(self.__create_file(self.BINARY_BASE_NAME), "w") as binary_file:
            binary_file.write("/".join(_binary))
    
    def __parse_binary_file(self):
        with open(self._file, "rb") as file_to_parse:
            _items = str(file_to_parse.read()).split("/")
        _parsed_binary = parse_binary(decompress_binary(_items))

        _split = ""
        settings = self.__parse_settings()
        if "rawbinary" in settings:
            _parsed_binary = decompress_binary(_items)
        
        if "rawbinary/" in settings:
            _parsed_binary = decompress_binary(_items)
            _split = "/"
        
        with open(self.__create_file(self.PARSED_BASE_NAME), "w") as parse_file:
            parse_file.write(_split.join(_parsed_binary))
    
    def execute(self):
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
    import os

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
        fbf_size = os.path.getsize(binary_file)
    
    with open(__binary_file, "r") as second_binary_file:
        sbf_length = len(str(second_binary_file.read()))
        sbf_size = os.path.getsize(__binary_file)

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
    else:
        return
    processor.set_settings(settings)
    processor.execute()

def main():
    parser = _argparse.ArgumentParser()
    parser.add_argument("-file", type=str, required=True)
    parser.add_argument("-filename", type=str, required=True)
    parser.add_argument("-run", type=str, required=True)
    parser.add_argument("--settings", type=str, nargs="*", required=False)

    args = parser.parse_args()
    _on_run(file=args.file, filename=args.filename, run=args.run, settings=args.settings)

if __name__ == "__main__":
    main()