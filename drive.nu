# This file is designed to help you iteratively develop from Nushell. Source this file with "source drive.nu".

$env.LANGCHAIN_PLAYGROUND_INDEX_LIMIT = 1000
$env.LANGCHAIN_PLAYGROUND_OPENAI_API_BASE_URL = "https://api.openai.com/v1"
$env.LANGCHAIN_PLAYGROUND_REPOSITORIES_DIR = "/Users/dave/repos/personal"
$env.LANGCHAIN_PLAYGROUND_VECTOR_STORE_DIR = "/Users/dave/Library/Caches/semantic_search/vectorstore"

# Load key from the clipboard. You must have first copied the key to the clipboard.
def --env load_key [] {
    let result = pbpaste | complete
    if ($result.exit_code != 0) {
        error make --unspanned {
            msg: ("Failed to paste from the clipboard. Is the clipboard empty?" + (char newline) + $result.stderr)
        }
    }

    let key = $result.stdout | str trim
    if ($key | str starts-with "sk-") {
        $env.LANGCHAIN_PLAYGROUND_OPENAI_API_KEY = $key
    } else {
        error make --unspanned {
            msg: "The pasted content does not appear to be a valid OpenAI API key. It does not start with 'sk-'. Check it, and try again."
        }
    }
}

def delete_index [] {
    print $"Vector directory: ($env.LANGCHAIN_PLAYGROUND_VECTOR_STORE_DIR)"
    rm --recursive --force --interactive-once $env.LANGCHAIN_PLAYGROUND_VECTOR_STORE_DIR
}

def index [] {
    python -m semantic_search index
}

def search [$query] {
    python -m semantic_search search $query
}
