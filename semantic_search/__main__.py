import argparse

import httpx
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from semantic_search.config import Config
from semantic_search.index import index
from semantic_search.search import search
import logging


def main():
    # logging.getLogger("httpx").setLevel(logging.DEBUG)

    logging.basicConfig(
        format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO
    )

    config = Config()

    parser = argparse.ArgumentParser(description='Semantic search')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    subparsers.add_parser('index', help='Build an embedding index over the documents')

    parser_search = subparsers.add_parser('search', help='Semantic search the index and return relevant documents')
    parser_search.add_argument('query', type=str, help='Search query')

    args = parser.parse_args()

    # httpx_client = httpx.Client(event_hooks={'request': [log_request], 'response': [log_response]})
    httpx_client = httpx.Client()

    open_ai_embeddings = OpenAIEmbeddings(http_client=httpx_client, openai_api_key=config.openai_api_key,
                                          openai_api_base=config.openai_api_base_url.geturl(),
                                          model=config.embedding_model)

    if args.command == 'index':
        index(config.repositories_dir, config.index_limit, config.vector_store_dir, open_ai_embeddings)
    elif args.command == 'search':
        chat_openai = ChatOpenAI(http_client=httpx_client, model=config.chat_model, api_key=config.openai_api_key,
                                 base_url=config.openai_api_base_url.geturl())
        search(config.vector_store_dir, open_ai_embeddings, chat_openai, args.query)
    else:
        parser.print_help()


def log_request(request):
    print(f"Request: {request.method} {request.url}")
    print(f"Headers: {request.headers}")
    print(f"Body: {request.content.decode()}")


def log_response(response):
    request = response.request
    response.read()
    print(f"Response: {response.status_code} {request.method} {request.url}")
    print(f"Headers: {response.headers}")
    print(f"Body: {response.text}")


if __name__ == "__main__":
    main()
