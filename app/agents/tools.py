
from app.data.sample_documents import MEDICAL_DOCUMENTS


def search_medical_library(query: str) -> str:
    """
    Search the local medical reference library
    using keywords from the user's question.
    """

    # Convert the question into lowercase words
    query_words = query.lower().split()

    # Store matching documents here
    results = []

    # Examine every document in the library
    for document in MEDICAL_DOCUMENTS:

        # Combine title, topic and content for searching
        searchable_text = (
            document["title"] + " " +
            document["topic"] + " " +
            document["content"]
        ).lower()

        # Count how many query words appear in the document
        score = 0

        for word in query_words:
            if len(word) > 2 and word in searchable_text:
                score += 1

        # Keep documents that contain matching keywords
        if score > 0:
            results.append((score, document))

    # If no matching documents are found
    if not results:
        return (
            "No matching information was found in the medical "
            "reference library. Do not invent a source or claim "
            "that the library supports an answer."
        )

    # Sort documents by relevance score (highest first)
    results.sort(key=lambda item: item[0], reverse=True)

    # Prepare the search results
    output = "MEDICAL REFERENCE SEARCH RESULTS:\n\n"

    for score, document in results[:3]:
        output += f"Document ID: {document['id']}\n"
        output += f"Title: {document['title']}\n"
        output += f"Source: {document['source']}\n"
        output += f"Reference URL: {document['url']}\n"
        output += f"Information: {document['content'].strip()}\n"
        output += "\n-------------------------\n\n"

    return output
