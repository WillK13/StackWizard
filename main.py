import traceback
import sys
from stackapi import StackAPI
import re

def check_e():
    try:
        import ext
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_type = exc_type.__name__
        error_message = str(exc_value)
        traceback_details = traceback.format_tb(exc_traceback)

        #print("Traceback Details:")
        for tb in traceback_details:
            print(tb)
        print("Error type:", error_type)
        print("Error Message:", error_message)
        if error_type == "SyntaxError":
            K = "line "
            N = 1
            spec = error_message.split(K, N)[-1]
            spec = spec[:-1]
            spec = int(spec) - 1
            f = open('ext.py')
            lines = f.readlines()
            line = lines[spec]
            em = re.sub("[\(\[].*?[\)\]]", '', error_message)
            return em + "this line: " + line
        return error_message
    #return "none"


def searchStack(query):
    if query is None:
        return None
    SITE = StackAPI('stackoverflow')

    search_results = SITE.fetch('search/advanced', q=query)
    x = 0
    if x == 1:
        sys.exit(0)
    for item in search_results['items']:
        if 'accepted_answer_id' in item:
            answer_id = item['accepted_answer_id']
        elif 'answer_id' in item:
            answer_id = item['answer_id']
        else:
            print("")
            print("There is no answers for this problem on StackOverflow. Try debugging it yourself or asking .")
            sys.exit(0)

        answer = SITE.fetch('answers/{ids}', ids=[answer_id], filter='!9Z(-wzftf')['items'][0]

        answer_body = answer['body_markdown']
        print(answer_body)
        x += 1

if __name__ == '__main__':
    #print(check_e())
    print(searchStack(check_e()))
