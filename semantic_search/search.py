import os

from chromadb import Settings
from langchain import hub
# What's the difference between langchain_community.vectorstores and langchain_chroma?
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI


def search(vector_store_dir: str, openai_embeddings: OpenAIEmbeddings, chat_openai: ChatOpenAI, query: str):
    print('Searching...')

    if not os.path.exists(vector_store_dir):
        msg = f"No index exists at ({vector_store_dir}). You need to build an index before searching from it."
        raise FileExistsError(msg)

    client_settings = Settings(anonymized_telemetry=False, is_persistent=True)
    vectorstore = Chroma(embedding_function=openai_embeddings, collection_name="semantic-search-collection",
                         client_settings=client_settings,
                         persist_directory=vector_store_dir)

    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | chat_openai
            | StrOutputParser())

    output = rag_chain.invoke(query)
    print(output)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
