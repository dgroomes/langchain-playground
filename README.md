# langchain-playground

📚 Learning and exploring LangChain.

> LangChain is a framework for developing applications powered by large language models (LLMs).
>
> https://github.com/langchain-ai/langchain


## Overview

I want to learn LangChain, and more generally, how to build applications powered by large language models (LLMs). This
repository is me doing that.


**NOTE**: This project was developed on macOS. It is designed for my own personal use.

With this project, I want to use LangChain in a basic semantic search application. I want to index all the `README.md`
files in my personal Git repositories and then offer a semantic search over them. The relevant text snippets will be
displayed. I expect that the LangChain APIs will make this easy to do. I'm following the [*Q&A with RAG* example](https://python.langchain.com/docs/use_cases/question_answering/quickstart/.)

I'm disappointed with how many dependencies LangChain is bringing in. I'd like to reduce it down closer to the
essentials, but I need to start with something that works first. The LangChain libraries appear to be modularized, so in
theory it should be feasible to break down to a small set of dependencies. Right now, `poetry show --only main | wc -l`
is showing 123 packages, so this is less than a typical Node.js project, and close to a typical Gradle/JVM project,
but still. In particular, I don't need the prompt/generative stuff because I'm only using embeddings in this example.


## Instructions

Follow these instructions to run an example LangChain-powered application.

1. Pre-requisite: Python and Poetry
   * I'm using Poetry 1.8.3 which I installed via `pipx`.
2. Pre-requisite: OpenAI key
   * You will supply an OpenAI API key to the Python program as an environment variable.
3. Download dependencies
   * ```shell
     poetry install
     ```
4. Enter the virtual environment
   * ```shell
     poetry shell
     ```
   * We want to develop with our toolchain in place. This is exactly what Python virtual environments are for. This
     command starts a subshell with the virtual environment activated.
5. Set environment variables
   * Below is an example of the environment variables used by the program. Change the values for your own needs. Study
     the code to understand what each variable is used for.
   * ```shell
     export LANGCHAIN_PLAYGROUND_INDEX_LIMIT="3"
     export LANGCHAIN_PLAYGROUND_OPENAI_API_KEY="REPLACE_WITH_YOUR_OPENAI_API_KEY"
     export LANGCHAIN_PLAYGROUND_OPENAI_API_BASE_URL="https://api.openai.com/v1"
     export LANGCHAIN_PLAYGROUND_REPOSITORIES_DIR="/Users/dave/repos/personal"
     export LANGCHAIN_PLAYGROUND_VECTOR_STORE_DIR="/Users/dave/Library/Caches/semantic_search/vectorstore"
     ```
6. Build the index
   * Run a program command that does document retrieval, splitting, and creates embeddings from the splits. Ultimately,
     this process creates a semantic index over the documents.  
   * ```shell
     python -m semantic_search index
     ```
7. Search the index (not implemented to the vision exactly; I need to get rid of the generation part)
   * Run a program command that takes a query and returns the most relevant documents from the index.
   * ```shell
     python -m semantic_search search "tasks list"
     ```
   * This should yield snippets of the `README.md` files that contain what I title "Wish List" sections. Notice that the
     search term was for "tasks" but the results yield "Wish List". This works because the LLM-powered search is a *semantic
     search* and not a keyword search.


## Running llama.cpp

I've been able to build and run llama.cpp with some success, but I've had issues getting it to create embeddings from
this project. I run the llama server with the following command:

```shell
build/bin/llama-server --model models/nomic-embed-text-v1.5.Q5_K_M.gguf --ctx-size 8192 --batch-size 8192 --embedding
```

And then I run this app to generate embeddings, and I see what look like good embeddings but then eventually the logs
show one full of nulls. Here is a snippet of the logs:

```text
Response: 200 POST http://localhost:8080/embeddings
Headers: Headers({'access-control-allow-origin': '', 'content-length': '63003', 'content-type': 'application/json; charset=utf-8', 'keep-alive': 'timeout=5, max=5', 'server': 'llama.cpp'})
Body: {"model":"text-embedding-ada-002","object":"list","usage":{"prompt_tokens":0,"total_tokens":0},"data":[{"embedding":[null,null,null
... omitted ...
```

I'd love to get this to work, but I'm going to just move on and use the OpenAI API instead.


## Wish List

General clean-ups, TODOs and things I wish to implement for this project:

* [x] DONE Find all README.md files in my personal Git repositories
* [x] DONE Figure out if I need to use a proper embedding model
* [x] DONE (Yes this is just easier and I already have had the experience of coding straight to embedding arrays and 
  cosine similarity). Should I bother with a vector database? I only want something as light as an embedded database so if there is a
  SQLite of vector databases I guess that's fine. Or, if it makes using LangChain easier, I'll use it. But if there is
  LangChain "files as a database" then I'd rather use that.
* [x] DONE (Appeared to work, but I don't know how to validate it. On to actual searching, next) Index
* [ ] IN PROGRESS Implement the `search` command
  * DONE First, I'm just copying from the example. But what I really want it to just pare it down to just an embedding
    comparison and not actually do any content generation. 
  * DONE Expand to the strongest models and all of my README files.
  * Customize the prompt to describe to the model what it's looking at (a bunch of my README files).
  * Get rid of the generation. Figure out the "right way" to do the embedding comparison (I imagine there are some
    sensible default settings for this). 
* [ ] How do I get an idea of the API cost?
