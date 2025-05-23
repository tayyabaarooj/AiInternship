from langchain.utils.math import cosine_similarity
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama

car_template="""You are an expert in automobile. You have extensive knowlegde about car mechanics, \
    models, and automobile technology.You provide clear and helpful answers about cars.
    Here is a question :
    {query}
    """

restaurant_template=""" You are a knowlegeable food critic and restauart reviewer. You have a deep understanding of a differnet cuisines, \
    dining experinece, and what makes a great restsurant. You answer questions about restaurants insight and food.
    Here is a question:
    {query}"""
technology_template="""You are a tech expert wiht in-depth knowledge of latest gadegts , softwraes, \
    and technological trends. You answer questions related to technology.
     Here is a question:
    {query}"""

car_questions = [
    "What is the difference between a sedan and an SUV?",
    "How does a hybrid car save fuel?",
    "What should I look for when buying a used car?",
]

restaurant_questions = [
    "What makes a five-star restaurant exceptional?",
    "How do I choose a good wine pairing for my meal?",
    "What are the key elements of French cuisine?",
]

technology_questions = [
    "What are the latest advancements in AI?",
    "How do I secure my home network against cyber threats?",
    "What should I consider when buying a new smartphone?",
]



embeddings = OllamaEmbeddings(
    model="llama3",
)

car_questions_embeddings=embeddings.embed_documents(car_questions)
restaurant_questions_embeddings= embeddings.embed_documents(restaurant_questions)
technology_questions_embeddings= embeddings.embed_documents(technology_questions)

def prompt_router(input):
    query_embedding= embeddings.embed_query(input["query"])
    car_similarity=cosine_similarity([query_embedding],car_questions_embeddings)[0]
    restaurant_similarity= cosine_similarity([query_embedding],restaurant_questions_embeddings)[0]
    technology_similarity=cosine_similarity([query_embedding],technology_questions_embeddings)[0]

    max_similarity=max(max(car_similarity),max(restaurant_similarity),max(technology_similarity))

    if max_similarity == max(car_similarity):
        print('usoing Car ')
        return PromptTemplate.from_template(car_template)
    elif max_similarity == max(restaurant_similarity):
        print("using Restaurant similarity")
        return PromptTemplate.from_template(restaurant_template)
    else:
        print("using tech similarity")
        return PromptTemplate.from_template(technology_template)


chain = (
    {"query": RunnablePassthrough()}
    | RunnableLambda(prompt_router)
    | ChatOllama(model="llama3")
    | StrOutputParser()
)
response= chain.invoke("How do i identify the italian pasta in a restaurant")
print(response)
