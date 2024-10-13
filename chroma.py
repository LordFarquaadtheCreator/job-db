class vector_store:
    def __init__(self, collection_name: str = "job"):
        """
        must check if `collection_name` collection exists
        "job" collection is default
            if not -> create
            if does -> load into memory
        """

        import chromadb
        import os

        self.CONFIDENCE_THRESHOLD = 0.7
        self.STORE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/vector_store"

        if not os.path.isdir(self.STORE_PATH):
            self.setup(collection_name)
        else:
            self.client = chromadb.PersistentClient(path=self.STORE_PATH)

        try:
            self.collection = self.client.get_collection(collection_name)
        except chromadb.errors.InvalidCollectionException:
            self.collection = self.client.create_collection(collection_name)

    def setup(self, collection_name: str):
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

        self.client = chromadb.PersistentClient(path=self.STORE_PATH)
        self.collection = self.client.create_collection(
            collection_name, metadata="collection of job application questions"
        )

    def add_new_question(self, question: str, answer: str, company: str):
        """
        creates brand new question in database
        stores answer as dictionary in metaldata
        id is company
        """

        metadata = {company: answer}
        self.collection.add(
            ids=[" ".join([company, question])],
            documents=[question],
            metadatas=metadata,
        )

    def question_exists(self, question: str):
        """
        check if the question given is similiar to an existing question
            if not, return None
            else return uid of existing similiar question
        """
        results = self.collection.query(
            query_texts=[question],
            include=["distances"],
            n_results=1,
        )

        distance = results["distances"].pop()
        if len(distance) == 0:
            return None

        distance = distance.pop()
        uid = results["ids"].pop().pop()

        if self.CONFIDENCE_THRESHOLD >= distance:
            return uid
        return None

    def add_to_existing_question(self, uid: str, answer: str, company: str):
        """
        will grab the exisiting question by uid and add the new answer and company to it's metadata
        """
        original_question = self.collection.get(ids=[uid], include=["metadatas"])
        new_metadata = original_question["metadatas"].pop()
        new_metadata[company] = answer

        self.collection.update(ids=[uid], metadatas=new_metadata)

    def add_question(self, question: str, answer: str, company: str):
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

    def get_question(self, question: str) -> (str, dict[str]):
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

    def get_client(self):
        """
        returns reference to client
        """
        return self.client

    def get_collection(self):
        """
        returns reference to collection
        """
        return self.collection
