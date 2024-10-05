class Test:
    def __init__(self):
        """
        should create a new vector store for the purposes of testin
        """
        from chroma import vector_store

        self.collection_name = "test"
        self.store = vector_store(self.collection_name)

        # init data
        self.store.add_new_question(
            "This is a document about pineapples", "Duh", "Pineapple Express"
        )

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

    def add_existing_question(self):
        question = "This is a movie about pineapples"
        review = "Uhhh maybe"
        company = "Panda Express"

        self.store.add_question(question, review, company)

        uid = self.store.question_exists(question)
        try:
            assert uid is not None
        except Exception:
            raise Exception("Question not saved in Add Existing Question test")

        ques, ans = self.store.get_question(question)
        try:
            assert ques and ans
        except Exception:
            raise Exception(
                "Question or Answer Missing from Add Existing Question Test"
            )

        try:
            assert ans[company] is not None
        except Exception:
            raise Exception("Saved answer missing in Add Existing Question test")

    def add_new_question(self):
        question = "Tell me about a time you watched Avatar the Last Airbender"
        answer = "uh wtf"
        company = "M Nigh Shyamalan"

        self.store.add_question(question, answer, company)

        uid = self.store.question_exists(question)
        try:
            assert uid is not None
        except Exception:
            raise Exception("Question not saved in Add New Question test")

        ques, ans = self.store.get_question(question)
        try:
            assert ques and ans
        except Exception:
            raise Exception("Question or Answer Missing from Add New Question Test")

        try:
            assert ans[company] is not None
            assert len(ans.keys()) == 1
        except Exception:
            raise Exception("Saved answer missing in Add New Question test")

    def add_to_existing_question(self, uid: str):
        self.store.add_to_existing_question(
            uid, "The movie was really good", "Hollywood Critque"
        )

        question, answer = self.store.get_question(
            "This is a document about pineapples"
        )

        assert answer["Hollywood Critque"] == "The movie was really good"

    def delete_collection(self):
        """
        delete the instance of the collection we're working with
        """
        client = self.store.get_client()
        client.delete_collection(self.collection_name)


if __name__ == "__main__":
    t = Test()

    t.add_new_question()
    t.add_existing_question()

    uid = t.question_exists()
    t.add_to_existing_question(uid)

    t.get_question()

    t.delete_collection()
