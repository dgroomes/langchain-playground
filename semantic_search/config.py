import os
import urllib.parse
from urllib.parse import ParseResult
from typing import Optional, Callable


class Config:
    """
    Encapsulates the configuration settings specific to the program. Settings are read from environment variables, where
    the setting is read from a same-named environment variable but prefixed with 'LANGCHAIN_PLAYGROUND_'. For example,
    the setting 'INDEX_LIMIT' is read from 'LANGCHAIN_PLAYGROUND_INDEX_LIMIT'.
    """

    # Maximum number of files to index. You should limit this to save time and cost while experimenting.
    index_limit: int
    chat_model: str
    embedding_model: str
    openai_api_key: str
    # The base URL of the OpenAI API. For example, 'https://api.openai.com/v1'.
    openai_api_base_url: ParseResult
    # Directory path to find local Git repositories.
    repositories_dir: str
    # Directory path where the vector indexes are stored.
    vector_store_dir: str

    def __init__(self):
        self.index_limit = get_and_validate_env_var('LANGCHAIN_PLAYGROUND_INDEX_LIMIT', validate_int, default='3')
        self.chat_model = get_env_var('LANGCHAIN_PLAYGROUND_CHAT_MODEL', default='gpt-4o')
        self.embedding_model = get_env_var('LANGCHAIN_PLAYGROUND_EMBEDDING_MODEL', default='text-embedding-3-large')
        self.openai_api_key = get_env_var('LANGCHAIN_PLAYGROUND_OPENAI_API_KEY')
        self.openai_api_base_url = get_and_validate_env_var('LANGCHAIN_PLAYGROUND_OPENAI_API_BASE_URL', validate_url)
        self.repositories_dir = get_and_validate_env_var('LANGCHAIN_PLAYGROUND_REPOSITORIES_DIR', validate_dir)
        self.vector_store_dir = get_and_validate_env_var('LANGCHAIN_PLAYGROUND_VECTOR_STORE_DIR', validate_dir)


def get_env_var(var_name: str, default: Optional[str] = None) -> str:
    value = os.getenv(var_name, default)
    if value is None:
        raise EnvironmentError(f"Error: Missing required environment variable: {var_name}")
    return value


def get_and_validate_env_var(var_name: str, validate: Callable, default: Optional[str] = None):
    value = get_env_var(var_name, default)
    return validate(value, var_name)


def validate_int(value: str, var_name: str) -> int:
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"Error: Environment variable '{var_name}' value '{value}' must be a valid integer.")


def validate_dir(path: str, var_name: str) -> str:
    if not os.path.isabs(path):
        raise ValueError(f"Error: Environment variable '{var_name}' value '{path}' must be an absolute directory path.")
    return path


def validate_url(url: str, var_name: str) -> ParseResult:
    parsed_url = urllib.parse.urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise ValueError(f"Error: Environment variable '{var_name}' value '{url}' must be a valid URL.")
    return parsed_url
