import os

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb.config import Settings

from semantic_search.loader import ReadmeLoader


def index(repositories_dir: str, limit: int, vector_store_dir: str, open_ai_embeddings: OpenAIEmbeddings):
    """
    Build an index of all the README.md files in my personal Git repositories. By convention, I put all my repositories
    as subdirectories in a particular directory on my computer. All my repositories have at least a brief README.md, and
    most have a substantial README.md.

    :return:
    """
    print('Indexing...')

    if os.path.exists(vector_store_dir):
        msg = (f"An index already exists ({vector_store_dir}). Can't create a new index. Consider deleting the "
               f"existing one.")
        raise FileExistsError(msg)
    else:
        os.makedirs(vector_store_dir)

    loader = ReadmeLoader(repos_directory=repositories_dir, limit=limit)
    docs = loader.load()

    print(f'Found {len(docs)} README files')
    for doc in docs:
        print(doc.metadata['source'])

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    print(f'Created {len(splits)} text splits')

    client_settings = Settings(anonymized_telemetry=False, is_persistent=True)

    vectorstore = Chroma.from_documents(documents=splits,
                                        embedding=open_ai_embeddings,
                                        collection_name="semantic-search-collection",
                                        client_settings=client_settings,
                                        persist_directory=vector_store_dir)

    print('Indexing complete. Vector store created of length', len(vectorstore))
