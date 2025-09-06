import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)
    with pytest.raises(Exception):
        Question(title='q1', points=-5)

def test_add_multiple_choices():
    question = Question(title='q1')
    
    choice1 = question.add_choice('Option A')
    choice2 = question.add_choice('Option B', True)
    
    assert len(question.choices) == 2
    assert choice1.id == 1
    assert choice2.id == 2
    assert not choice1.is_correct
    assert choice2.is_correct

def test_add_choice_with_invalid_text():
    question = Question(title='q1')
    
    with pytest.raises(Exception):
        question.add_choice('')
    with pytest.raises(Exception):
        question.add_choice('a' * 101)

def test_remove_choice_by_id():
    question = Question(title='q1')
    choice1 = question.add_choice('Option A')
    choice2 = question.add_choice('Option B')
    
    question.remove_choice_by_id(choice1.id)
    
    assert len(question.choices) == 1
    assert question.choices[0].text == 'Option B'

def test_remove_choice_with_invalid_id():
    question = Question(title='q1')
    question.add_choice('Option A')
    
    with pytest.raises(Exception):
        question.remove_choice_by_id(999)

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('Option A')
    question.add_choice('Option B')
    question.add_choice('Option C')
    
    question.remove_all_choices()
    
    assert len(question.choices) == 0

def test_set_correct_choices():
    question = Question(title='q1')
    choice1 = question.add_choice('Option A')
    choice2 = question.add_choice('Option B')
    choice3 = question.add_choice('Option C')
    
    question.set_correct_choices([choice1.id, choice3.id])
    
    assert choice1.is_correct
    assert not choice2.is_correct
    assert choice3.is_correct

def test_set_correct_choices_with_invalid_id():
    question = Question(title='q1')
    question.add_choice('Option A')
    
    with pytest.raises(Exception):
        question.set_correct_choices([999])

def test_correct_selected_choices_returns_correct_matches():
    question = Question(title='q1', max_selections=3)
    choice1 = question.add_choice('Option A', True)
    choice2 = question.add_choice('Option B', False)
    choice3 = question.add_choice('Option C', True)
    
    correct_selections = question.correct_selected_choices([choice1.id, choice2.id, choice3.id])
    
    assert len(correct_selections) == 2
    assert choice1.id in correct_selections
    assert choice3.id in correct_selections
    assert choice2.id not in correct_selections

def test_correct_selected_choices_exceeds_max_selections():
    question = Question(title='q1', max_selections=1)
    choice1 = question.add_choice('Option A')
    choice2 = question.add_choice('Option B')
    
    with pytest.raises(Exception):
        question.correct_selected_choices([choice1.id, choice2.id])


## Testes com fixture 

@pytest.fixture
def question_with_choices():
    question = Question(title='Sample Question', points=10, max_selections=2)
    question.add_choice('Option A', True)
    question.add_choice('Option B', False)
    question.add_choice('Option C', True)
    return question

def test_question_identifies_correct_answers(question_with_choices):
    correct_ids = [choice.id for choice in question_with_choices.choices if choice.is_correct]
    selected_correct = question_with_choices.correct_selected_choices(correct_ids)
    
    assert len(selected_correct) == 2
    assert question_with_choices.choices[0].id in selected_correct  # Option A
    assert question_with_choices.choices[2].id in selected_correct  # Option C

def test_question_rejects_too_many_selections(question_with_choices):
    all_choice_ids = [choice.id for choice in question_with_choices.choices]
    
    with pytest.raises(Exception):
        question_with_choices.correct_selected_choices(all_choice_ids)