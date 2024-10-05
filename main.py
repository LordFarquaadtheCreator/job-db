"""
cli that fetches a relevant question's answers
    confidence threshold - 70%
    
cli that has two options
    add question answer
    get question's answer
"""

if __name__ == "__main__":
    import argparse
    from chroma import vector_store
    from color import color

    store = vector_store()

    parser = argparse.ArgumentParser(
        prog="Job Database",
        description="Returns all previously written answers for the same question. Saves time",
        epilog="Fuck workday",
    )

    parser.add_argument(
        "-a",
        "--add-question",
        type=str,
        help="add a question to the database. [QUESTION] [ANSWER] [COMPANY]",
        nargs=3,
    )
    parser.add_argument(
        "-g",
        "--get-question",
        type=str,
        help="get the answers to a question. [QUESTION]",
        nargs=1,
    )

    args = parser.parse_args()

    if args.add_question:
        args = args.add_question
        store.add_question(args[0], args[1], args[2])
        exit(0)

    if args.get_question:
        ques, ans = store.get_question(args.get_question.pop())
        print(color.BOLD, "Question:", color.END, color.GREEN, ques, color.END)
        print(color.BOLD, "Answer(s):", color.END)

        for key, value in ans.items():
            print(color.BOLD, key, color.END)
            print(color.ITALICS, value, color.END)

        exit(0)
