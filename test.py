class Test:
    def __init__(self):
        """
        should create a new vector store for the purposes of testin
        """
        from chroma import vector_store

        self.store = vector_store()

    def question_exists(self):
        uid = self.store.question_exists("This is a document about pineapples")

        if not uid:
            raise Exception(
                "Question Exists test failed - should have returned the question. Returned None instead"
            )
        return uid

    def get_question(self):
        res = self.store.get_question("This is a document about pineapples")
        ques, ans = res

        if not ques or not ans:
            raise Exception(
                "Get Question test failed - there was no output for test case"
            )

    def add_question(self):
        try:
            self.store.add_new_question(
                "This is a movie about pineapples", "True!", "Pineapple Express"
            )
        except Exception as e:
            raise Exception("Add Question test failed", e)

    def add_to_existing_question(self, uid: str):
        self.store.add_to_existing_question(
            uid, "The movie was really good", "Hollywood Critque"
        )

        question, answer = self.store.get_question(
            "This is a document about pineapples"
        )

        assert answer["Hollywood Critque"] == "The movie was really good"


if __name__ == "__main__":
    t = Test()
    t.add_question()
    uid = t.question_exists()
    t.add_to_existing_question(uid)
    t.get_question()
