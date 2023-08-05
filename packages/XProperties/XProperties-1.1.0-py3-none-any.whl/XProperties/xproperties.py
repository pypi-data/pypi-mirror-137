import re
import json
import typing
from xml.etree import ElementTree

__all__ = [
    "Properties"
]


class Properties:
    """
    Parse properties file.
    """

    def __init__(self) -> None:
        super().__init__()
        self._properties: dict = {}

    def __setitem__(self, key: str, value: str) -> None:
        """
        Setting the value of a property.

        :param key: Property name.
        :param value: Value to set for the property.
        """
        self.set_property(key, value)

    def __getitem__(self, key: str) -> str:
        """
        Getting the value of a property.

        :param key: Property name.
        :exception KeyError: When property does not exist.
        :return: Property Value.
        """
        return self.get_property(key)

    def __delitem__(self, key: str) -> None:
        """
        Deleting the value of a property.

        :param key: Property name.
        :exception KeyError: When property does not exist.
        """
        self.delete_property(key)

    def __iter__(self) -> typing.Iterator[typing.Any]:
        """
        Get an iterator object.

        :return: Iterator object.
        """
        return iter(self.items())

    def __len__(self) -> int:
        """
        Get the number of properties.

        :return: The number of properties.
        """
        return self.count()

    def __contains__(self, key: str) -> bool:
        """
        Returns a value whether the key exists.

        :return: Boolean value of key existence.
        """
        return self.contains(key)

    def __eq__(self, other: typing.Any) -> bool:
        """
        Returns a value whether two object instances are equal.

        :param other: other object to compare.
        :return: Boolean value of whether two object instances are equal.
        """
        return self.equals(other)

    def __str__(self) -> str:
        """
        Convert instance to string.

        :return: Converted string.
        """
        return self.to_string()

    def load(self, file_name: str) -> None:
        """
        Loads a property list(key and element pairs) from the .properties file.
        The file is assumed to use the ISO-8859-1(Latin1) character encoding.

        :param file_name: .properties file name.
        :exception IOError: When an error occurs while reading the file.
        :exception ValueError: When the file contains a malformed
                               Unicode escape sequence.
        """
        with open(file_name, "r", encoding="iso-8859-1") as file:
            temp = file.read()
            temp = re.sub("^[#!].*[\r\n\f]+", "", temp)
            temp = re.sub("(?<!\\\\)\\\\[ \t]*[\r\n\f]+[ \t]*", "", temp)
            raw_data = re.split("[\r\n\f]+", temp)
        for i in raw_data:
            pair = re.split("(?<!\\\\)[ \t]*(?<!\\\\)[=:][ \t]*", i, 1)
            key = self._load_convert(pair[0], is_convert_key=True)
            if len(pair) == 2:
                value = self._load_convert(pair[1])
                self._properties[key] = value
            else:
                self._properties[key] = ""

    def save(self, file_name: str) -> None:
        """
        Saves a property list(key and element pairs) to the .properties file.
        The file will be writen in ISO-8859-1(Latin1) character encoding.

        :param file_name: .properties file name.
        :exception IOError: When an error occurs while writing the file.
        """
        with open(file_name, "w", encoding="iso-8859-1") as file:
            for k, v in zip(self._properties.keys(), self._properties.values()):
                key = self._save_convert(k, is_convert_key=True)
                value = self._save_convert(v)
                pair = key + "=" + value
                file.write(pair + "\n")

    def load_from_xml(self, file_name: str) -> None:
        """
        Loads a property list(key and element pairs) from the .xml file.

        The XML document must have the following DOCTYPE declaration:
        <!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">

        :param file_name: .xml file name.
        :exception IOError: When an error occurs while writing the file.
        :exception ValueError: When the XML file is malformed.
        """
        try:
            doc = ElementTree.parse(file_name)
        except ElementTree.ParseError:
            raise ValueError("Malformed XML format.")
        root = doc.getroot()
        pairs = root.findall("entry")
        for pair in pairs:
            if "key" in pair.attrib:
                key = pair.get("key")
                value = pair.text
                self._properties[key] = value
            else:
                raise ValueError("Malformed XML format.")

    def save_to_xml(self, file_name: str) -> None:
        """
        Saves a property list(key and element pairs) to the .xml file.

        The XML document will have the following DOCTYPE declaration:
        <!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">

        :param file_name: .xml file name.
        :exception IOError: When an error occurs while writing the file.
        """
        xml_declaration = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        doctype = ("<!DOCTYPE properties SYSTEM "
                   "\"http://java.sun.com/dtd/properties.dtd\">\n")
        root = ElementTree.Element("properties")
        for property_ in self._properties.items():
            element = ElementTree.Element("entry")
            element.set("key", property_[0])
            element.text = property_[1]
            root.append(element)
        tree = ElementTree.ElementTree(root)
        with open(file_name, "wb") as file:
            file.write(xml_declaration.encode("utf-8"))
            file.write(doctype.encode("utf-8"))
            tree.write(file, "utf-8", False)

    @staticmethod
    def _load_convert(value: str, is_convert_key: bool = False) -> str:
        """
        Converts escape sequences to chars.

        :param value: String to convert.
        :exception ValueError: When the value contains a malformed
                               Unicode escape sequence.
        :return: Converted string.
        """
        if is_convert_key:
            value = value.replace("\\ ", " ")
        value = value.replace("\\t", "\t")
        value = value.replace("\\r", "\r")
        value = value.replace("\\n", "\n")
        value = value.replace("\\f", "\f")
        escapes = set(re.findall("\\\\u[A-F0-9]{4}", value))
        for escape in escapes:
            temp = 0
            for i in escape[2:]:
                if i in "0123456789":
                    temp = (temp << 4) + ord(i) - ord("0")
                elif i in "abcdef":
                    temp = (temp << 4) + 10 + ord(i) - ord("a")
                elif i in "ABCDEF":
                    temp = (temp << 4) + 10 + ord(i) - ord("A")
                else:
                    raise ValueError("Malformed \\uxxxx encoding.")
            value = value.replace(escape, chr(temp))
        return value

    @staticmethod
    def _save_convert(value: str, is_convert_key: bool = False) -> str:
        """
        Converts chars to escape sequences.

        :param value: String to convert.
        :return: Converted string.
        """
        buffer = []
        if is_convert_key:
            value = value.replace(" ", "\\ ")
            value = value.replace("=", "\\=")
            value = value.replace(":", "\\:")
        value = value.replace("\\", "\\\\")
        value = value.replace("\t", "\\t")
        value = value.replace("\r", "\\r")
        value = value.replace("\n", "\\n")
        value = value.replace("\f", "\\f")
        for char in value:
            if ord(char) < 0x20 or ord(char) > 0x7e:
                char = "\\u" + hex(ord(char))[2:].zfill(4)
            buffer.append(char)
        return "".join(buffer)

    def set_property(self, key: str, value: str) -> None:
        """
        Setting the value of a property.

        :param key: Property name.
        :param value: Value to set for the property.
        """
        self._properties[key] = value

    def get_property(self, key: str, default: str = "") -> str:
        """
        Getting the value of a property.

        :param key: Property name.
        :param default: Default value if property does not exist.
        :exception KeyError: When property does not exist.
        :return: Property Value.
        """
        if key in self._properties.keys():
            return self._properties[key]
        return default

    def delete_property(self, key: str) -> None:
        """
        Deleting the value of a property.

        :param key: Property name.
        :exception KeyError: When property does not exist.
        """
        del self._properties[key]

    def clear(self) -> None:
        """
        Remove all properties.
        """
        self._properties.clear()

    def keys(self) -> typing.List[str]:
        """
        Getting the list of properties name.

        :return: List of properties name.
        """
        return list(self._properties.keys())

    def values(self) -> typing.List[str]:
        """
        Getting the list of properties value.

        :return: List of properties value.
        """
        return list(self._properties.values())

    def items(self) -> typing.List[typing.Tuple[str, str]]:
        """
        Getting the list of properties key-value pair.

        :return: List of properties key-value pair.
        """
        return list(map(tuple, self._properties.items()))

    def count(self) -> int:
        """
        Get the number of properties.

        :return: The number of properties.
        """
        return len(self._properties)

    def contains(self, key: str) -> bool:
        """
        Returns a value whether the key exists.

        :return: Boolean value of key existence.
        """
        return key in self._properties

    def equals(self, other: typing.Any) -> bool:
        """
        Returns a value whether two object instances are equal.

        :param other: other object to compare.
        :return: Boolean value of whether two object instances are equal.
        """
        return self._properties == other

    def to_string(self) -> str:
        """
        Convert the current object to string.

        :return: Converted string.
        """
        return json.dumps(self._properties)
