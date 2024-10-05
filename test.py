class Test:
    def __init__(self):
        from chroma import vector_store

        self.store = vector_store()

    def question_exists(self):
        res = self.store.question_exists("This is a document about pineapples")

        if not res:
            raise Exception(
                "Question Exists test failed - should have returned the question. Returned None instea"
            )

    def get_question(self):
        res = self.store.get_question("This is a document about pineapples")
        ques, ans = res

        if not ques or not ans:
            raise Exception(
                "Get Question test failed - there was no output for test case"
            )


if __name__ == "__main__":
    t = Test()
    t.question_exists()
    t.get_question()
