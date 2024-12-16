# **Constitutional Debates Search: A Project on Embeddings and Semantic Search**

This project explores **embeddings**, **vector search**, and **semantic reranking** by experimenting with content from the **Constituent Assembly Debates of India**. I tested this locally with the **first volume** of the debates to see how tools like **OpenAI embeddings**, **Qdrant**, and **Cohere's Rerank API** can provide meaningful and relevant search results.  
I sourced the Constituent Assembly Debates from [constitutionofindia.net](https://www.constitutionofindia.net/constitution-assembly-debates/).

---

## **What This Project Does**

1. **Search with Semantic Embeddings**  
   - A user inputs a query.  
   - The query is converted into a **vector embedding** using **OpenAI's `text-embedding-3-small` model**.  
   - These embeddings are used to retrieve similar results from a local **Qdrant vector database**.

2. **Rerank for Relevance**  
   - Search results can be **reranked** using **Cohere's Rerank API**, which sorts the retrieved content by relevance to the query.

3. **A Simple Interface**  
   - I built a lightweight **HTML frontend** where you can:
     - Enter a query.
     - View the search results.
     - Rerank results with a single click.

---

## **Why I Built This**

I wanted to:  
- Explore **embeddings** and see how text data can be represented as vectors.  
- Experiment with **semantic search** using a vector database like Qdrant.  
- Understand how **reranking models** like Cohere’s can refine search results.  

Using the **Constituent Assembly Debates** as a dataset felt like a meaningful way to ground this exploration in **real content**.

---

## **Tech Stack**

- **FastAPI**: For the backend API.
- **Qdrant**: Local vector search database.
- **OpenAI API**: Generates semantic embeddings for the query.
- **Cohere API**: Reranks search results.
- **HTML + JavaScript**: Simple frontend for user interaction.

---
