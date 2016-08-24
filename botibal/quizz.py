# -*- coding: utf-8 -*-
"""
Quizz module
"""
import random


class ScoreDict(dict):
    """
    Stores the game's scores
    """

    def add_score(self, username, score):
        """
        Adds a new score for a given user
        """
        score = int(score)

        if username in self:
            self[username] += score
        else:
            self[username] = score

    def reset(self):
        """
        Resets the scores for all users
        """
        for username in self:
            self[username] = 0

    def results(self):
        """
        Displays the scores
        """
        return '\n'.join(['{}: {}'.format(user, score)
                          for user, score in sorted(self.items())])


class Quizz(object):
    """
    Quizz handling
    """

    def __init__(self, database_connection):
        self.questions = {}
        self.current_question = None
        self.db_conn = database_connection
        self.db_cur = self.db_conn.cursor()
        self.init_db()

    def __repr__(self):
        return '\n'.join(['{} - {}'.format(index, que['text'])
                          for index, que in self.questions.items()])

    def init_db(self):
        """
        Initializes DB interaction

        Actions:
        - create tables if necessary,
        - load data.
        """
        self.db_cur.execute(
            '''CREATE TABLE IF NOT EXISTS question (
            id INTEGER PRIMARY KEY,
            text TEXT)''')
        self.db_cur.execute(
            '''CREATE TABLE IF NOT EXISTS answer (
            id INTEGER PRIMARY KEY,
            question_id INTEGER,
            text TEXT,
            FOREIGN KEY(question_id) REFERENCES question(id))''')
        self.db_conn.commit()
        self.load_from_db()

    def load_from_db(self):
        """
        Loads questions and answers from the database
        """
        for q_id, q_text in self.db_cur.execute(
                'SELECT id, text FROM question').fetchall():
            ans = self.db_cur.execute(
                'SELECT id, text FROM answer WHERE question_id=?', (q_id,)
            ).fetchall()
            self.questions[q_id] = {'text': q_text, 'answers': ans}

    def add_question(self, question, answers):
        """
        Adds a new question
        """
        if question is None or question == '':
            raise ValueError('Empty question')

        if question in [que['text'] for _, que in self.questions.items()]:
            raise ValueError('Duplicate question')

        if answers is None or answers == [] or answers == ['']:
            raise ValueError('No answers specified')

        self.db_cur.execute('INSERT INTO question VALUES(NULL,?)', (question,))
        self.db_conn.commit()
        q_id, = self.db_cur.execute(
            'SELECT id FROM question ORDER BY id DESC LIMIT 1').fetchone()
        for ans in answers:
            self.db_cur.execute('INSERT INTO answer VALUES(NULL,?,?)',
                                (q_id, ans))
        self.db_conn.commit()
        self.load_from_db()

    def delete_question(self, index):
        """
        Deletes a question and its answers
        """
        self.db_cur.execute('DELETE FROM answer WHERE question_id=?', (index,))
        self.db_cur.execute('DELETE FROM question WHERE id=?', (index,))
        self.db_conn.commit()
        del self.questions[index]
        return 'The question #{} has been deleted'.format(index)

    def ask_next_question(self):
        """
        Asks a question
        """
        index = random.randint(0, len(self.questions) - 1)
        self.current_question = self.questions[list(self.questions)[index]]
        return self.current_question['text']

    def check_answer(self, answer):
        """
        Checks if an answer is suitable
        """
        return answer.lower() in [ans[1].lower()
                                  for ans in self.current_question['answers']]
