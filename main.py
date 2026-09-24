from app.loaders.github_loader import GitHubRepositoryLoader
from app.loaders.repository_scanner import RepositoryScanner
from app.loaders import code_loader
from app.processors.code_chunker import CodeChunker
from app.vector_stores.chroma_store import ChromaStore
from app.agents.code_reviewer import CodeReviewer
from app.agents.repository_reviewer import RepositoryReviewer
from app.agents.review_aggregator import ReviewAgentAggregator
from dotenv import load_dotenv
from app.agents.semantic_reviewer import SemanticReviewer


load_dotenv()


# ============================================================
# 1. Clone repository
# ============================================================

loader = GitHubRepositoryLoader()

repo_path = loader.clone(
    "https://github.com/PrateekK-coder/Wish_List-App.git"
)


# ============================================================
# 2. Scan repository and find code files
# ============================================================

scanner = RepositoryScanner()

files = scanner.scan(repo_path)

print("Code files found:", len(files))


# ============================================================
# 3. Load all code files
# ============================================================

code_files = []

for file in files:
    code_file = code_loader.load_code(file)
    code_files.append(code_file)

print("CodeFiles loaded:", len(code_files))


# ============================================================
# 4. Chunk all code files
# ============================================================

chunker = CodeChunker()

all_chunks = []

for code_file in code_files:

    document = chunker.convert_to_document(code_file)

    chunks = chunker.code_splitter(document)

    all_chunks.extend(chunks)

print("Total chunks:", len(all_chunks))


# ============================================================
# 5. Store chunks in ChromaDB
# ============================================================

store = ChromaStore()

store.add_documents(all_chunks)

print("Stored documents:", store.count())

#semantic search code 

# code_reviewer = CodeReviewer()

# semantic_reviewer = SemanticReviewer(
#     code_reviewer=code_reviewer,
#     vector_store=store,
#     code_files=code_files
# )

# query = "Find potential null-safety and crash risks"

# reviews = semantic_reviewer.review(
#     query=query,
#     k=5
# )

# for review in reviews:
#     print("=" * 80)
#     print(review)


# whole repo level code review code


code_reviewer = CodeReviewer()

repository_reviewer = RepositoryReviewer(
    code_reviewer=code_reviewer,
    vector_store=store,
    code_files=code_files
)

reviews = repository_reviewer.review_repository(
    code_files=code_files,
    chunks=all_chunks
)



aggregator = ReviewAgentAggregator()

final_result = aggregator.aggregate(reviews)

print("\n" + "=" * 80)
print("FINAL REPOSITORY REVIEW")
print("=" * 80)

print("Files reviewed:", final_result["files_reviewed"])
print("Total issues:", final_result["total_issues"])
print("Severity counts:", final_result["severity_counts"])

for issue in final_result["issues"]:

    print("\n" + "-" * 80)

    print("Category:", issue.category)
    print("Severity:", issue.severity)
    print("File:", issue.file)
    print("Line:", issue.line)
    print("Description:", issue.description)
    print("Recommendation:", issue.recommendation)




































# code_reviewer=CodeReviewer()
# repository_reviewer= RepositoryReviewer(
#     code_reviewer= code_reviewer,
#     vector_store=store
# )

# test_file_paths = list({
#     chunk.metadata["file_path"]
#     for chunk in all_chunks
# })[:3]

# test_chunks = [
#     chunk
#     for chunk in all_chunks
#     if chunk.metadata["file_path"] in test_file_paths
# ]


# reviews= repository_reviewer.review_repository(code_files=code_files,chunks=test_chunks)

# aggregator = ReviewAgentAggregator()

# repository_report = aggregator.aggregate(reviews)

# print("\nREPOSITORY REPORT")
# print(repository_report)

# for review in reviews:
#         print("=" * 80)
#         print(review)


























































# file_path= "app/data/sample_code/bad_code.py"

# code_file = code_loader.load_code(file_path)

# chunker= CodeChunker()
# document=chunker.convert_to_document(code_file)


# chunks = chunker.code_splitter(document)

# print(f"Total chunks: {len(chunks)}")

# # for i, chunk in enumerate(chunks):
# #     print(f"\n--- Chunk {i + 1} ---")
# #     print(chunk.page_content)
# #     print("Metadata:", chunk.metadata)

# store=ChromaStore()

# # store.add_documents(chunks)
# # print("Indexing completed!")
# print("Stored documents:", store.count())


# results= store.search("Find SQL injection vulnerabilities",k=2)

# # for result in results:
# #     print("=" * 80)
# #    # print("Score:", score)
# #     print(result.page_content)
# #     print(result.metadata)

# def convert_docs_to_string_list(docs):
#         return [doc.page_content for doc in docs]




# code_chunks = convert_docs_to_string_list(results)

# # for chunk in code_chunks:
# #     print("=" * 80)
# #     print(chunk)

# context = "\n\n".join(code_chunks)

# chunk = chunks[0]

# reviewer = CodeReviewer()

# result = reviewer.review(
#     code_file=code_file,
#     code=chunk.page_content,
#     context=""
# )

# print(result)






# code_reviewer= CodeReviewer()
# repository_reviewer=RepositoryReviewer(code_reviewer)

# reviews = repository_reviewer.review_repository(
#     code_file=code_file,
#     chunks=chunks
# )

# for review in reviews:
#     print("=" * 80)
#     print(review)



































































































# embedder=CodeEmbedding()

# embedding=embedder.docs_to_vec(chunks)



# reviewer = CodeReviewer()
# 
# result = reviewer.review(code_file)
# 
# 
# 
# print(result)
# 
# 
# loader= GitHubRepositoryLoader()
# 
# repo_path=loader.clone('https://github.com/ghanteyyy/StockVault.git')
# 
# 
# 
# scanner=RepositoryScanner()
# 
# files=scanner.scan(repo_path)
# 
# 
# 
# code_file=[]
# 
# 
# for file in files:
#    print(file)
#    code=code_loader.load_code(file)
#    code_file.append(code)
# 
