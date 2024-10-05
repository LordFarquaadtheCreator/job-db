class vector_store:
    def __init__(self):
        """
        must check if collection exists
            if not -> create
            if does -> load into memory
        """

        import chromadb
        import os

        self.CONFIDENCE_THRESHOLD = 0.7

        if not os.path.isdir("vector_store/"):
            self.setup()
        else:
            self.client = chromadb.PersistentClient(path="./vector_store")
            self.collection = self.client.get_collection("job")

    def setup(self):
        """
        creates new client and collection
        default client name "vector_store"
        default collection name "job"
        should only be run once
        """

        print(
            'Chroma Client not detected, creating new vector store with name "vector store" and collection name "job"'
        )

        import chromadb

        self.client = chromadb.PersistentClient(path="./vector_store")
        self.collection = self.client.create_collection(
            "job", metadata="collection of job application questions"
        )

    def add_new_question(self, question: str, answer: str, company: str = None):
        """
        creates brand new question in database
        stores answer and company as dictionary in metaldata
        """

        metadata = {"answer": answer, "company": [company]}
        self.collection.add(embeddings=question, metadatas=metadata)

    def question_exists(self, question: str):
        """
        check if the question given is similiar to an existing question
            if not, return None
            else return similiar question
        """
        results = self.collection.query(
            query_texts=[question],
            include=["distances", "uid"],
            n_results=1,
        )

        distance = results["distances"].pop().pop()
        uid = results["uid"].pop().pop()

        if self.CONFIDENCE_THRESHOLD >= distance:
            return uid
        return None

    def add_to_existing_question(self, uid: str, answer: str, company: str = None):
        """
        will grab the exisiting question and modify it's metadata
        """
        pass

    def add_question(self, question: str, answer: str, company: str = None):
        """
        will check if question similiar to previously answered question
            if yes, add onto the existing question's metadata
            else -> create new question
        """

        new_question = self.question_exists(question)
        if new_question:
            self.add_to_existing_question(new_question, answer, company)
        else:
            self.add_new_question(question, answer, company)

    def get_question(self, question: str) -> list[str]:
        """
        returns tuple representing the question and answer
        (question, answer)
        """
        results = self.collection.query(
            query_texts=[question],
            include=["documents", "metadatas"],
            n_results=1,
        )
        question = results["documents"].pop().pop()
        answer = results["metadatas"].pop().pop()

        return (question, answer)
