# -*- coding: utf-8 -*-
'Quizz module'
import datetime
import os
import random


QUIZZ_DIR = 'quizz'


class Question(object):
    'Represents a question and its possible answers'
    def __init__(self, question, answers, filepath=None):
        self.question = question
        self.answers = answers
        if filepath:
            self.filepath = filepath
        else:
            self.filepath = '{}.quizz'.format(datetime.date.today())


    def save_to_file(self):
        'Writes a question to the corresponding file'
        with open(self.filepath, 'w') as f_question:
            f_question.write('{}\n'.format(self.question))
            f_question.write('\n'.join(self.answers))


    def check_answer(self, answer):
        'Checks if an answer is suitable'
        if answer.lower() in [ans.lower() for ans in self.answers]:
            return True
        return False


class Quizz(object):
    'Quizz handling'
    def __init__(self, quizz_dir=QUIZZ_DIR):
        self.questions = list()
        self.current_question = None
        self.quizz_dir = quizz_dir
        self.load_from_dir()


    def load_from_dir(self):
        'Loads questions from files in the quizz directory'
        for path in [os.path.join(self.quizz_dir, f)
                     for f in os.listdir(self.quizz_dir)
                     if os.path.isfile(os.path.join(self.quizz_dir, f))]:

            with open(path) as f_question:
                lines = f_question.read().splitlines()
                try:
                    self.questions.append(Question(lines[0], lines[1:-1], path))
                except IndexError:
                    continue


    def add_question(self, question, answers, filepath=None):
        'Adds a new question'
        que = Question(question, answers, filepath)
        self.questions.append(que)
        que.save_to_file()


    def delete_question(self, index):
        'Deletes a question'
        try:
            filepath = self.questions[index].filepath
        except IndexError:
            print 'Wrong index'
            return

        if os.path.isfile(filepath):
            os.remove(filepath)
        del self.questions[index]


    def list_questions(self):
        'Lists available questions'
        return '\n'.join(['{}. {}'.format(index, que.question)
                          for index, que in enumerate(self.questions)])


    def ask_question(self):
        'Asks a question'
        index = random.randint(0, len(self.questions) - 1)
        self.current_question = self.questions[index]
        return self.current_question.question


    def check_answer(self, answer):
        'Checks if an answer is suitable'
        self.current_question.check_answer(answer)
