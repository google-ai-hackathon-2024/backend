import prompt_template as ptemp
import vertexai_summary as summ

CREDENTIALS_FILE = "../gcp-credential/key_new.json"

def read_txt(filepath:str) -> str:
    with open(filepath) as f:
        lines = f.readlines()
    return lines

# TRANSCRIPT = read_txt('../speech2text/results/biz-meeting/biz-result-oup-brainstorming-meeting_16k/transcript.txt')
# CONV_TYPE = 0
# CONV_TITLE = 'Brainstorming the company slogan'

# TRANSCRIPT = read_txt('../speech2text/results/debating/2012-first-debate-biden-ryan_16k/transcript.txt')
# CONV_TYPE = 1
# CONV_TITLE = '2012 US President debate: Biden vs. Ryan'

# TRANSCRIPT = read_txt('../speech2text/results/interview/Dalia_Mogahed_16k/transcript.txt')
# CONV_TYPE = 2
# CONV_TITLE = 'Interview Dalia Mogahed by TED'

TRANSCRIPT = read_txt('../speech2text/results/monologue/DJ_221_ban-gambling_con_opening_YBA_16k/transcript.txt')
CONV_TYPE = 3
TEMPLATE = ptemp.get_template(CONV_TYPE)
CONV_TITLE = 'Opinion about gambling'

if __name__ == "__main__":

    summary = summ.generate_summary(CREDENTIALS_FILE, TEMPLATE, TRANSCRIPT, CONV_TITLE)

    filename = './test.txt'
    with open(filename, "w") as f:
        f.write(summary)