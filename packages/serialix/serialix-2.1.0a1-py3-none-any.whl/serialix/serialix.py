from .core import BaseLang


class Serialix:
    """
    ``serialix`` unified instance generator for any officially supported language.

    This class should be used for creation of the basic ``serialix`` object for one of the officially supported languages. Currently supported languages: ``json``, ``yaml``, ``toml``

    :param file_format: Format of language to be used. Currently supported languages: ``json``, ``yaml`` (or ``yml``), ``toml`` (or ``tml``)
    :type file_format: str
    :param file_path: Path to preferred local file destination
        If the file does not exist at the specified path, it will be created
    :type file_path: str
    :param default_dictionary: Default local file path ``str`` or ``dict``
        that will be used for local file start values and , defaults to {}
    :type default_dictionary: Union[str, dict], optional
    :param auto_file_creation: Automatic local file creation on object initialization, defaults to True
    :type auto_file_creation: bool, optional
    :param force_overwrite_file: Whether the file needs to be overwritten if it already exists, defaults to False
    :type force_overwrite_file: bool, optional
    :param parser_write_kwargs: Pass custom arguments to parser's write to local file action, defaults to {}
    :type parser_write_kwargs: dict, optional
    :param parser_read_kwargs: Pass custom arguments to parser's read from local file action, defaults to {}
    :type parser_read_kwargs: dict, optional
    :raises ValueError: If provided data type in argument ``default_dictionary`` is not
        the path ``str`` or ``dict``
    :raises ValueError: If provided data in argument ``file_format`` is not one of the supported languages

    .. versionadded:: 2.1.0
    """
    def __new__(self, file_format: str, file_path: str, default_dictionary={}, auto_file_creation=True, force_overwrite_file=False, parser_write_kwargs={}, parser_read_kwargs={}) -> BaseLang:
        file_format = file_format.lower()
        if file_format == 'json':
            from .langs.json import JSON_Format

            return JSON_Format(file_path=file_path, default_dictionary=default_dictionary, auto_file_creation=auto_file_creation, force_overwrite_file=force_overwrite_file, parser_write_kwargs=parser_write_kwargs, parser_read_kwargs=parser_read_kwargs)
        elif file_format in ('yaml', 'yml'):
            from .langs.yaml import YAML_Format

            return YAML_Format(file_path=file_path, default_dictionary=default_dictionary, auto_file_creation=auto_file_creation, force_overwrite_file=force_overwrite_file, parser_write_kwargs=parser_write_kwargs, parser_read_kwargs=parser_read_kwargs)
        elif file_format in ('toml', 'tml'):
            from .langs.toml import TOML_Format

            return TOML_Format(file_path=file_path, default_dictionary=default_dictionary, auto_file_creation=auto_file_creation, force_overwrite_file=force_overwrite_file, parser_write_kwargs=parser_write_kwargs, parser_read_kwargs=parser_read_kwargs)
        else:
            raise ValueError("'file_format' should be one of the supported languages name, not '{}'".format(file_format))
