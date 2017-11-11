"""Quizz module"""
import random

from botibal.models import Answer, Question


class ScoreDict(dict):
    """Stores the game's scores"""

    def add_score(self, username, score):
        """Adds a new score for a given user"""
        score = int(score)

        if username in self:
            self[username] += score
        else:
            self[username] = score

    def reset(self):
        """Resets the scores for all users"""
        for username in self:
            self[username] = 0

    def results(self):
        """Displays the scores"""
        return '\n'.join([
            '{}: {}'.format(user, score)
            for user, score in sorted(self.items())
        ])


class Quizz():
    """Quizz handling"""

    def __init__(self, session):
        self.question = None
        self.session = session

    def __repr__(self):
        return '\n'.join([
            '{} - {}'.format(question.id, question.text)
            for question in self.questions.all()
        ])

    @property
    def questions(self):
        """Get Question items from the database"""
        return self.session.query(Question)

    @property
    def answers(self):
        """Get Answer items from the database"""
        return self.session.query(Answer)

    def add_question(self, text, answers):
        """Adds a new question"""
        if not text:
            raise ValueError('Empty question')

        if text in [que.text for que in self.questions.all()]:
            raise ValueError('Duplicate question')

        if not answers or answers == ['']:
            raise ValueError('No answers specified')

        question = Question(text=text)
        self.session.add(question)
        self.session.commit()

        for answer_text in answers:
            answer = Answer(text=answer_text, question_id=question.id)
            self.session.add(answer)
            self.session.commit()

    def delete_question(self, index):
        """Deletes a question and its answers"""
        question = self.questions.get(index)
        self.session.delete(question)
        return "The question #{} has been deleted".format(index)

    def ask_next_question(self):
        """Asks a question"""
        index = random.randint(1, self.questions.count())
        self.question = self.questions.get(index)
        return self.question.text

    def check_answer(self, answer):
        """Checks if an answer is suitable"""
        answers = [ans.text.lower() for ans in self.question.answers]
        return answer.lower() in answers
