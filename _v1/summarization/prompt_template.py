from string import Template 

biz_meeting = Template(
    'Imagine you are a minute taker in the business meeting talking about \'${conv_title}\' \n'\
    '\n'\
    'It is transcripted like below\n'\
    '\n'\
    '${transcript}\n'\
    '\n'\
    'Using the following question,\n'\
    '- what has been accomplished so far?\n'\
    '- what needs to be done?\n'\
    '- Are there any problems we are facing?\n'\
    '- Are there any major wins?\n'\
    '\n'\
    'Summarize this business meeting conversation in the following format:\n'\
    '===============================================================\n'\
    'TITLE : (business meeting title)\n'\
    '\n'\
    'ACCOMPLISHMENTS :\n'\
    '- (accomplishment 1)\n'\
    '- (accomplishment 2)\n'\
    '- (accomplishment 3)\n'\
    '(or other accomplishments)\n'\
    '\n'\
    'TO DO LIST :\n'\
    '- (item 1)\n'\
    '- (item 2)\n'\
    '- (item 3)\n'\
    '(or more todo items)\n'\
    '\n'\
    'PROBLEMS :\n'\
    '- (problem 1)\n'\
    '- (problem 2)\n'\
    '- (problem 3)\n'\
    '(or other problems)\n'\
    '\n'\
    'WINS :\n'\
    '- (win 1)\n'\
    '- (win 2)\n'\
    '- (win 3)\n'\
    '(or other wins)\n'\
    '===============================================================\n'\
    '\n'\
    'The summary is...\n'
) 
debating = Template(
    'Imagine you are a minute taker in the debate about \'${conv_title}\' \n'\
    '\n'\
    'It is transcripted like below\n'\
    '\n'\
    '${transcript}\n'\
    '\n'\
    'Using the following question,\n'\
    '- what is the topic?\n'\
    '- what is the main arguments from each side?\n'\
    '\n'\
    'Summarize this debate in the following format:\n'\
    '===============================================================\n'\
    'TITLE : (debate title)\n'\
    '\n'\
    'TOPIC : (debate topic 1)\n'\
    '\n'\
    'DEBATOR 1: (debater 1 name)\n'\
    '- (argument 1)\n'\
    '- (argument 2)\n'\
    '- (argument 3)\n'\
    '(or other arguemnts)\n'\
    '\n'\
    'DEBATOR 2: (debater 2 name)\n'\
    '- (argument 1)\n'\
    '- (argument 2)\n'\
    '- (argument 3)\n'\
    '(or other arguemnts)\n'\
    '\n'\
    '(or other sets of topic & debator arguement)'
    '===============================================================\n'\
    '\n'\
    'The summary is...\n'
) 
interview = Template(
    'Imagine you are a minute taker in the interview about \'${conv_title}\' \n'\
    '\n'\
    'It is transcripted like below\n'\
    '\n'\
    '${transcript}\n'\
    '\n'\
    'Using the following question,\n'\
    '- what is the question asked?\n'\
    '- what is the main point of the response of the interviewee\n'\
    '\n'\
    'Summarize this interview in the following format:\n'\
    '===============================================================\n'\
    'TITLE : (interview title)\n'\
    '\n'\
    'INTERVIEWEE : (description of interviewee)\n'\
    '\n'\
    'Q. (question)\n'\
    'A.\n'\
    '- (main point 1)\n'\
    '- (main point 2)\n'\
    '- (main point 3)\n'\
    '(or more main points)\n'\
    '\n'\
    '(or other sets of Q&A)\n'\
    '===============================================================\n'\
    '\n'\
    'The summary is...\n'
) 
monologue = Template(
    'Imagine you are a minute taker in the monologue about \'${conv_title}\' \n'\
    '\n'\
    'It is transcripted like below\n'\
    '\n'\
    '${transcript}\n'\
    '\n'\
    'Using the following question,\n'\
    '- what are the topics?\n'\
    '- what are the main argument of each topic from the speaker?\n'\
    '\n'\
    'Summarize this monologue in the following format:\n'\
    '===============================================================\n'\
    'TITLE : (monologue title)\n'\
    '\n'\
    'TOPIC : (short topic description)\n'\
    '- (argument 1)\n'\
    '- (argument 2)\n'\
    '- (argument 3)\n'\
    '(or more arguments)\n'\
    '\n'\
    '(or other set of topic & arguments )\n'\
    '===============================================================\n'\
    '\n'\
    'The summary is...\n'
) 

template_set = [biz_meeting, debating, interview, monologue]

def get_template(conv_type:int):
    print("Get Prompt Template!")
    return template_set[conv_type]