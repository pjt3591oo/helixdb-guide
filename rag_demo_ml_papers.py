from chonkie import RecursiveChunker, RecursiveRules, RecursiveLevel
from docling.document_converter import DocumentConverter
from transformers import AutoTokenizer, AutoModel
from rich.console import Console
from rich.text import Text
from typing import List, Tuple
import numpy as np
import os
import torch
from tqdm import tqdm
import requests

import helix
from helix.client import Query
from helix.types import Payload

console = Console()

# A wrapper to pretty print
def rprint(text: str, console: Console=console, width: int = 80) -> None:
  richtext = Text(text)
  console.print(richtext.wrap(console, width=width))


tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModel.from_pretrained("microsoft/codebert-base")

rust_docs_endpoints = [
    (1, "Getting Started", "https://doc.rust-lang.org/book/ch01-00-getting-started.html"),
    (1, "Installation", "https://doc.rust-lang.org/book/ch01-01-installation.html"),
    (1, "Hello, World!", "https://doc.rust-lang.org/book/ch01-02-hello-world.html"),
    (1, "Hello, Cargo!", "https://doc.rust-lang.org/book/ch01-03-hello-cargo.html"),
    (2, "Guessing Game Tutorial", "https://doc.rust-lang.org/book/ch02-00-guessing-game-tutorial.html"),
    (3, "Common Programming Concepts", "https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html"),
    (3, "Variables and Mutability", "https://doc.rust-lang.org/book/ch03-01-variables-and-mutability.html"),
    (3, "Data Types", "https://doc.rust-lang.org/book/ch03-02-data-types.html"),
    (3, "How Functions Work", "https://doc.rust-lang.org/book/ch03-03-how-functions-work.html"),
    (3, "Comments", "https://doc.rust-lang.org/book/ch03-04-comments.html"),
    (3, "Control Flow", "https://doc.rust-lang.org/book/ch03-05-control-flow.html"),
    (4, "Understanding Ownership", "https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html"),
    (4, "What is Ownership?", "https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html"),
    (4, "References and Borrowing", "https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html"),
    (4, "Slices", "https://doc.rust-lang.org/book/ch04-03-slices.html"),
    (5, "Structs", "https://doc.rust-lang.org/book/ch05-00-structs.html"),
    (5, "Defining Structs", "https://doc.rust-lang.org/book/ch05-01-defining-structs.html"),
    (5, "Example Structs", "https://doc.rust-lang.org/book/ch05-02-example-structs.html"),
    (5, "Method Syntax", "https://doc.rust-lang.org/book/ch05-03-method-syntax.html"),
    (6, "Enums", "https://doc.rust-lang.org/book/ch06-00-enums.html"),
    (6, "Defining an Enum", "https://doc.rust-lang.org/book/ch06-01-defining-an-enum.html"),
    (6, "Match", "https://doc.rust-lang.org/book/ch06-02-match.html"),
    (6, "If Let", "https://doc.rust-lang.org/book/ch06-03-if-let.html"),
    (7, "Managing Growing Projects with Packages, Crates, and Modules", "https://doc.rust-lang.org/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html"),
    (7, "Packages and Crates", "https://doc.rust-lang.org/book/ch07-01-packages-and-crates.html"),
    (7, "Defining Modules to Control Scope and Privacy", "https://doc.rust-lang.org/book/ch07-02-defining-modules-to-control-scope-and-privacy.html"),
    (7, "Paths for Referring to an Item in the Module Tree", "https://doc.rust-lang.org/book/ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html"),
    (8, "Common Collections", "https://doc.rust-lang.org/book/ch08-00-common-collections.html"),
    (8, "Vectors", "https://doc.rust-lang.org/book/ch08-01-vectors.html"),
    (8, "Strings", "https://doc.rust-lang.org/book/ch08-02-strings.html"),
    (8, "Hash Maps", "https://doc.rust-lang.org/book/ch08-03-hash-maps.html"),
    (9, "Error Handling", "https://doc.rust-lang.org/book/ch09-00-error-handling.html"),
    (9, "Unrecoverable Errors with Panic", "https://doc.rust-lang.org/book/ch09-01-unrecoverable-errors-with-panic.html"),
    (9, "Recoverable Errors with Result", "https://doc.rust-lang.org/book/ch09-02-recoverable-errors-with-result.html"),
    (9, "To Panic or Not to Panic", "https://doc.rust-lang.org/book/ch09-03-to-panic-or-not-to-panic.html"),
    (10, "Generics", "https://doc.rust-lang.org/book/ch10-00-generics.html"),
    (10, "Syntax", "https://doc.rust-lang.org/book/ch10-01-syntax.html"),
    (10, "Traits", "https://doc.rust-lang.org/book/ch10-02-traits.html"),
    (10, "Lifetime Syntax", "https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html"),
    (11, "Testing", "https://doc.rust-lang.org/book/ch11-00-testing.html"),
    (11, "Writing Tests", "https://doc.rust-lang.org/book/ch11-01-writing-tests.html"),
    (11, "Running Tests", "https://doc.rust-lang.org/book/ch11-02-running-tests.html"),
    (11, "Test Organization", "https://doc.rust-lang.org/book/ch11-03-test-organization.html"),
    (12, "An I/O Project", "https://doc.rust-lang.org/book/ch12-00-an-io-project.html"),
    (12, "Accepting Command Line Arguments", "https://doc.rust-lang.org/book/ch12-01-accepting-command-line-arguments.html"),
    (12, "Reading a File", "https://doc.rust-lang.org/book/ch12-02-reading-a-file.html"),
    (12, "Improving Error Handling and Modularity", "https://doc.rust-lang.org/book/ch12-03-improving-error-handling-and-modularity.html"),
    (12, "Testing the Library's Functionality", "https://doc.rust-lang.org/book/ch12-04-testing-the-librarys-functionality.html"),
    (12, "Working with Environment Variables", "https://doc.rust-lang.org/book/ch12-05-working-with-environment-variables.html"),
    (12, "Writing to stderr Instead of stdout", "https://doc.rust-lang.org/book/ch12-06-writing-to-stderr-instead-of-stdout.html"),
    (13, "Functional Features", "https://doc.rust-lang.org/book/ch13-00-functional-features.html"),
    (13, "Closures", "https://doc.rust-lang.org/book/ch13-01-closures.html"),
    (13, "Iterators", "https://doc.rust-lang.org/book/ch13-02-iterators.html"),
    (13, "Improving Our I/O Project", "https://doc.rust-lang.org/book/ch13-03-improving-our-io-project.html"),
    (14, "More About Cargo", "https://doc.rust-lang.org/book/ch14-00-more-about-cargo.html"),
    (14, "Release Profiles", "https://doc.rust-lang.org/book/ch14-01-release-profiles.html"),
    (14, "Publishing to Crates.io", "https://doc.rust-lang.org/book/ch14-02-publishing-to-crates-io.html"),
    (14, "Cargo Workspaces", "https://doc.rust-lang.org/book/ch14-03-cargo-workspaces.html"),
    (14, "Installing Binaries", "https://doc.rust-lang.org/book/ch14-04-installing-binaries.html"),
    (14, "Extending Cargo", "https://doc.rust-lang.org/book/ch14-05-extending-cargo.html"),
    (15, "Smart Pointers", "https://doc.rust-lang.org/book/ch15-00-smart-pointers.html"),
    (15, "Box", "https://doc.rust-lang.org/book/ch15-01-box.html"),
    (15, "Deref", "https://doc.rust-lang.org/book/ch15-02-deref.html"),
    (15, "Drop", "https://doc.rust-lang.org/book/ch15-03-drop.html"),
    (15, "Rc", "https://doc.rust-lang.org/book/ch15-04-rc.html"),
    (15, "Interior Mutability", "https://doc.rust-lang.org/book/ch15-05-interior-mutability.html"),
    (15, "Reference Cycles", "https://doc.rust-lang.org/book/ch15-06-reference-cycles.html"),
    (16, "Concurrency", "https://doc.rust-lang.org/book/ch16-00-concurrency.html"),
    (16, "Threads", "https://doc.rust-lang.org/book/ch16-01-threads.html"),
    (16, "Message Passing", "https://doc.rust-lang.org/book/ch16-02-message-passing.html"),
    (16, "Shared State", "https://doc.rust-lang.org/book/ch16-03-shared-state.html"),
    (16, "Extensible Concurrency: Sync and Send", "https://doc.rust-lang.org/book/ch16-04-extensible-concurrency-sync-and-send.html"),
    (17, "Object-Oriented Programming", "https://doc.rust-lang.org/book/ch17-00-oop.html"),
    (17, "What is OO?", "https://doc.rust-lang.org/book/ch17-01-what-is-oo.html"),
    (17, "Trait Objects", "https://doc.rust-lang.org/book/ch17-02-trait-objects.html"),
    (17, "OO Design Patterns", "https://doc.rust-lang.org/book/ch17-03-oo-design-patterns.html"),
    (18, "Patterns", "https://doc.rust-lang.org/book/ch18-00-patterns.html"),
    (18, "All the Places for Patterns", "https://doc.rust-lang.org/book/ch18-01-all-the-places-for-patterns.html"),
    (18, "Refutability", "https://doc.rust-lang.org/book/ch18-02-refutability.html"),
    (18, "Pattern Syntax", "https://doc.rust-lang.org/book/ch18-03-pattern-syntax.html"),
    (19, "Advanced Patterns", "https://doc.rust-lang.org/book/ch19-00-patterns.html"),
    (19, "All the Places for Patterns", "https://doc.rust-lang.org/book/ch19-01-all-the-places-for-patterns.html"),
    (19, "Refutability", "https://doc.rust-lang.org/book/ch19-02-refutability.html"),
    (19, "Pattern Syntax", "https://doc.rust-lang.org/book/ch19-03-pattern-syntax.html"),
    (20, "Advanced Features", "https://doc.rust-lang.org/book/ch20-00-advanced-features.html"),
    (20, "Unsafe Rust", "https://doc.rust-lang.org/book/ch20-01-unsafe-rust.html"),
    (20, "Advanced Traits", "https://doc.rust-lang.org/book/ch20-02-advanced-traits.html"),
    (20, "Advanced Types", "https://doc.rust-lang.org/book/ch20-03-advanced-types.html"),
    (20, "Advanced Functions and Closures", "https://doc.rust-lang.org/book/ch20-04-advanced-functions-and-closures.html"),
    (20, "Macros", "https://doc.rust-lang.org/book/ch20-05-macros.html"),
]

converter = DocumentConverter()
results = [(ch, sch, converter.convert(doc)) for ch, sch, doc in rust_docs_endpoints]
text_results = [(ch, sch, res.document.export_to_markdown()) for ch, sch, res in results]

rules = RecursiveRules(
    levels=[
        RecursiveLevel(delimiters=['######', '#####', '####', '###', '##', '#']),
        RecursiveLevel(delimiters=['\n\n', '\n', '\r\n', '\r']),
        RecursiveLevel(delimiters='.?!;:'),
        RecursiveLevel()
    ]
)
chunker = RecursiveChunker(rules=rules, chunk_size=250)

list_of_chunks = [(ch, sch, content, chunker(content)) for ch, sch, content in text_results]

def vectorize_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        embedding = outputs.last_hidden_state[:, 0, :].squeeze().tolist()
    return embedding

def vectorize_chunked(chunked: List[str]) -> List[List[float]]:
    # embedding dims: 768
    vectorized = []
    for chunk in tqdm(chunked):
        embedding = vectorize_text(chunk)
        vectorized.append(embedding)
    return vectorized

db = helix.Client(local=True)

class LoaddocsRag(Query):
    def __init__(
        self,
        chapters: List[Tuple[int, List[Tuple[str, str, List[Tuple[str, List[float]]]]]]],
    ):
        super().__init__()
        self.chapters = chapters

    def query(self) -> List[Payload]:
        chapters_payload = []
        for id, subchapters in self.chapters:
            for title, content, chunks in subchapters:
                chunks_l = []
                for chunk, vector in chunks:
                    chunks_l.append({ "chunk": chunk, "vector": vector })
                subchapter_payload = [{ "title": title, "content": content, "chunks": chunks_l }]
            chapters_payload.append({ "id": id, "subchapters": subchapter_payload })
        return [{ "chapters": chapters_payload }]

    def response(self, response):
        return response

class SearchdocsRag(Query):
    def __init__(self, query_vector: List[float], k: int=3):
        super().__init__()
        self.query_vector = query_vector
        self.k = k

    def query(self) -> List[Payload]:
        return [{ "query": self.query_vector, "k": self.k }]

    def response(self, response):
        return response
    
if __name__ == "__main__":
    items = [(ch, [(sch, content, [(chunk.text, vectorize_text(chunk.text)) for chunk in clist])]) for ch, sch, content, clist in tqdm(list_of_chunks)]
    
    res0 = db.query(LoaddocsRag(items))
    print('inserted docs')
    print('*' * 80)

    user_prompt = "what is ownership in rust and how does it relate to lifetimes"
    query_embedding = vectorize_text(user_prompt)
    
    contexts = db.query(SearchdocsRag(query_embedding))[0]['subchapters']
    
    for i in contexts:
        print(i)
        print()
        print()
        print()
        print()
        print()
        print('-' * 80)
    print(len(contexts))

    prompts = f"""
    You are a helpful assistant that can answer questions about the following context:
    
    context:
    {contexts}

    question: {user_prompt}

    answer:
    """

    print(prompts)

    # llm call
    # llm.invoke(prompts)