# Import modules and packages
import numpy as np
import pickle

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import Qdrant
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import WikipediaLoader
#from langchain.schema import Document
from transformers import BitsAndBytesConfig

from RAG_inputs import wikipedia_queries, webpage_urls

# Set configuration for quantization
quantization_config = BitsAndBytesConfig(load_in_8bit=True)

def load_chunk_wiki(query, global_doc_number, chunk_size=512, overlap=50):

  wiki_docs = WikipediaLoader(query=query, load_max_docs=4).load()

  for idx, text in enumerate(wiki_docs):
    wiki_docs[idx].metadata['doc_num'] = global_doc_number
    wiki_docs[idx].metadata['doc_source'] = "Wikipedia"

  global_doc_number += 1

  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
  wiki_splits = text_splitter.split_documents(wiki_docs)
  for idx, text in enumerate(wiki_splits):
    wiki_splits[idx].metadata['split_id'] = idx

  return wiki_splits, global_doc_number

def load_chunk_web(query, global_doc_number, chunk_size=512, overlap=50):

  web_docs = WebBaseLoader(query).load()

  for idx, text in enumerate(web_docs):
    web_docs[idx].metadata['doc_num'] = global_doc_number
    web_docs[idx].metadata['doc_source'] = "Webpage"

  global_doc_number += 1

  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
  web_splits = text_splitter.split_documents(web_docs)
  for idx, text in enumerate(web_splits):
    web_splits[idx].metadata['split_id'] = idx

  return web_splits, global_doc_number

base_embeddings = HuggingFaceEmbeddings(model_name="avsolatorio/GIST-Embedding-v0")

# Initialize vectorstore
wiki_splits_0, global_doc_number_0 = load_chunk_wiki(wikipedia_queries[0], global_doc_number=0)
 
qdrant_vectorstore = Qdrant.from_documents(wiki_splits_0,
                                            base_embeddings,
                                            location=":memory:",
                                            collection_name="history_db",
                                            force_recreate=True)
 
global_doc_number = global_doc_number_0
 
 # Vectorize the Wikipedia chunks
for wiki_query in wikipedia_queries[1:]:
  wiki_splits, global_doc_number = load_chunk_wiki(wiki_query, global_doc_number=global_doc_number)
  qdrant_vectorstore.add_documents(documents=wiki_splits)
 
# Vectorize the Webpage chunks
web_splits, global_doc_number = load_chunk_web(webpage_urls, global_doc_number=global_doc_number)
qdrant_vectorstore.add_documents(documents=web_splits)

# Create the retriever
retriever = qdrant_vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 8})

pick_insert = open('retriever.pkl','wb')
pickle.dump(retriever, pick_insert)
pick_insert.close()