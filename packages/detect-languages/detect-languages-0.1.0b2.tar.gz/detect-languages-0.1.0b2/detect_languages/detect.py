import logging
import os
from typing import List

import jmespath
from pygments.lexers import guess_lexer_for_filename
from pygments.util import ClassNotFound

from detect_languages.languages import name_type_extensions


class DetectLanguages:
    def __init__(
        self,
        debug: bool = False,
        path: str = ".",
        language_types: List[str] = ["programming", "prose", "data", "markup"],
        exclude_dirs: List[str] = [],
        exclude_dirs_recursively: bool = False,
    ) -> None:
        """Instance and execute the analysis.

        Args:
            debug (bool, optional): Show debug info. Defaults to False.
            path (str, optional): Path to project or repository. Defaults to ".".
            language_types (List[str], optional): Language types. Defaults to ["programming", "prose", "data", "markup"].
            exclude_dirs (List[str], optional): Exclude dirs. Defaults to [].
            exclude_dirs_recursively (bool, optional): Exclude dirs recursively. Defaults to False.
        """
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG if debug else None)
        self.__language_types = []
        self.__language_types.extend(language_types)
        self.__exclude_dirs = [".git"]
        self.__exclude_dirs.extend(exclude_dirs)
        self.__exclude_dirs_recursively = exclude_dirs_recursively
        self.__analysis = {}
        self.__total_files_size = 0
        self.main_language = None
        self.all_languages = []
        self.__language_types_extensions = []
        self.__run_analysis(path)

    def __run_analysis(self, path: str) -> None:
        """Run analysis.

        Args:
            path (str): Path to project or repository.
        """
        logging.debug("Detecting languages...")
        logging.debug(f"Language types: {self.__language_types}")
        self.__filter_language_types()
        self.__filter_exclude_dirs(path)
        self.__percentage_calculation()
        if len(self.__analysis.keys()) == 0:
            logging.debug("Not detected languages")
            return
        self.main_language = max(self.__analysis.items(), key=lambda a: self.__analysis[a[0]]["size"])[0]
        logging.debug(f"Detected main language: {self.main_language}")
        self.all_languages = dict(sorted(self.__analysis.items(), key=lambda kv: float(kv[1]["percentage"]), reverse=True))
        logging.debug(f"Detected languages: {list(self.all_languages.keys())}")

    def __filter_language_types(self) -> None:
        """Filter extensions by language types."""
        for language_type in self.__language_types:
            extensions = jmespath.search(f"[?type=='{language_type}'].extensions[]", name_type_extensions())
            self.__language_types_extensions.extend(extensions)

    def __is_in_language_types(self, language: str) -> bool:
        """Check if language is in language types.

        Args:
            language (str): Language to check.

        Returns:
            bool: Returns a boolean value.
        """
        language_type = jmespath.search(f"[?name=='{language}'].type | [0]", name_type_extensions())
        return language_type in self.__language_types

    def __guess_file_language(self, file: str) -> str:
        """Guess file language using pygments.

        Args:
            file (str): File path.

        Returns:
            str: Returns language.
        """
        try:
            with open(file, "r", encoding="utf-8") as reader:
                file_content = reader.read()
                try:
                    language = guess_lexer_for_filename(file, file_content, stripnl=False).__class__.name
                except ClassNotFound as ex:
                    logging.debug(ex)
                    return
                return language
        except UnicodeDecodeError:
            logging.debug(f"'{file}' is not a text file.")
            return

    def __filter_exclude_dirs(self, path: str) -> None:
        """Filter exclude dirs on root level or recursively.

        Args:
            path (str): Path to project or repository.
        """
        root, subdirs, files = next(os.walk(path))
        for filename in files:
            file = os.path.join(root, filename)
            _, file_extension = os.path.splitext(file)
            file_size = os.path.getsize(file)
            if file_size == 0:
                continue
            self.__check_file(file, file_extension, file_size)
        for subdir in subdirs:
            if subdir not in self.__exclude_dirs:
                subdir_path = os.path.join(root, subdir)
                if not self.__exclude_dirs_recursively:
                    self.__find_files(subdir_path)
                else:
                    self.__filter_exclude_dirs(subdir_path)

    def __find_files(self, subdir_path: str) -> None:
        """Find files to check.

        Args:
            subdir_path (str): Subdirectory path.
        """
        for root, _, files in os.walk(subdir_path):
            for filename in files:
                file = os.path.join(root, filename)
                _, file_extension = os.path.splitext(file)
                file_size = os.path.getsize(file)
                if file_size == 0:
                    continue
                self.__check_file(file, file_extension, file_size)

    def __check_file(self, file: str, file_extension: str, file_size: int) -> None:
        """Check the file extension and language type.

        Args:
            file (str): File path.
            file_extension (str): File extension.
            file_size (int): File size.
        """
        if not file_extension or file_extension in self.__language_types_extensions:
            language = self.__guess_file_language(file)
            logging.debug(f"file: '{file}', language: '{language}', size: {file_size}")
            if not language:
                return
            if language == "Text only":
                return
            if not self.__is_in_language_types(language):
                logging.debug(f"'{language}' language type is not in language types {self.__language_types}")
                return
            self.__add_file_size_and_total_files_size(language, file_size)

    def __add_file_size_and_total_files_size(self, language: str, size: int) -> None:
        """Add file size and total files size.

        Args:
            language (str): Language to add.
            size (int): File size.
        """
        if language in self.__analysis:
            self.__analysis[language]["size"] += size
        else:
            self.__analysis[language] = {"size": size}
        self.__total_files_size += size

    def __percentage_calculation(self) -> None:
        """Percentage calculation"""
        for language in self.__analysis.keys():
            self.__analysis[language]["percentage"] = round(((self.__analysis[language]["size"] / self.__total_files_size) * 100), 2)
