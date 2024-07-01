import os
from typing import Iterator

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document


class ReadmeLoader(BaseLoader):
    """
    A document loader that loads README.md files in my personal Git repositories.
    """

    def __init__(self, repos_directory: str, limit: int) -> None:
        """
        Initialize the loader with the directory containing the repositories and a limit on the number of README files
        to load.
        :param repos_directory: The directory containing the repositories. For example, "/Users/me/code".
        :param limit: The maximum number of README files to load.
        """
        self.repos_directory = repos_directory
        self.limit = limit

    def lazy_load(self) -> Iterator[Document]:
        count = 0

        for dir_name in os.listdir(self.repos_directory):
            if count >= self.limit:
                break

            directory_path = os.path.join(self.repos_directory, dir_name)
            if not os.path.isdir(directory_path):
                continue

            readme_path = os.path.join(directory_path, 'README.md')

            if not os.path.isfile(readme_path):
                continue

            # Read the file content into a string
            with open(readme_path, 'r') as f:
                content = f.read()

            yield Document(page_content=content,
                           metadata={"source": readme_path})

            count += 1
