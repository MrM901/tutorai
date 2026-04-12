from rag_engine import extract_text, chunk_text, create_index, retrieve

pdf_path = "sample.pdf"

text = extract_text(pdf_path)
print("TEXT LENGTH:", len(text))
chunks = chunk_text(text)
print("NUMBER OF CHUNKS:", len(chunks))

index, chunks = create_index(chunks)

query = "What is the main topic?"
results = retrieve(query, index, chunks)

print("\n--- Retrieved Context ---\n")
for r in results:
    print(r[:300])
    print("\n---\n")
    from llm import generate_quiz

context = " ".join(results)

quiz = generate_quiz(context)

print("\n--- QUIZ ---\n")
print(quiz)
