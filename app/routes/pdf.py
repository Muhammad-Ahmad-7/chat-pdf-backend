from fastapi import APIRouter, File, UploadFile
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from app.validators.pdf import ChatBody
from langchain_core.prompts import PromptTemplate
router = APIRouter()

retriever = None


@router.post('/upload')
async def upload_pdf(file: UploadFile=File(...)):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    await process_pdf(file_path)
    return {"message": "File processed"}


@router.post('/chat')
async def chat_pdf(body:ChatBody):
    res = get_answer(body.query)
    return {'message': 'Question:', 'Result': res}


async def process_pdf(file_path):
    global retriever
    data = load_pdf(file_path)
    chunks = chunker(data)
    retriever = generate_store_retriever(chunks)


# 1. Loading the pdf
def load_pdf(file_path):
    loader = PyPDFLoader(file_path=file_path)
    return loader.load()


# 2. Using RecursiveCharacterSplitter to split the text
def chunker(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    chunks = splitter.split_documents(docs)
    return chunks


# 3. Generate Embedding and store in Vector Store, Create Retriever using that vector store
def generate_store_retriever(chunks):
    store = FAISS.from_documents(chunks, embedding=OpenAIEmbeddings())
    return store.as_retriever(search_type='similarity')


def get_answer(question:str):
    prompt = PromptTemplate(
        template="""
            You are an intelligent and reliable AI assistant that helps users understand documents by answering questions based **only** on the provided context.

        📄 **Document Context**:
        {context}

        ❓ **User Question**:
        {question}

        ✅ **Instructions**:
        - Use only the content in the context above to answer.
        - If the answer is unclear :
            Make sure to explain it with your own data
        - If the answer is not available, say:
            "I'm sorry, I couldn't find that information in the document."
        - **Include a relevant source reference**, such as a short quote, sentence, or page number from metadata if available.
        - **Always give your answer in a presentable manner**
        🧠 **Your Answer**:
        """,
        input_variables=["context", "question"],
    )
    global retriever
    if retriever is None:
        return "Please upload a document first."
    llm = ChatOpenAI()
    retrieved_docs = retriever.invoke(question)
    final_prompt = prompt.invoke({'context': retrieved_docs, 'question': question})
    res = llm.invoke(final_prompt)
    return res.content
