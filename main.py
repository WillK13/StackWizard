import traceback
import sys
import re
import requests
import html2text

def check_e():
    try:
        import ext
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_type = exc_type.__name__
        error_message = str(exc_value)
        traceback_details = traceback.format_tb(exc_traceback)

        print("Traceback Details:")
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
    search_api_url = "https://api.stackexchange.com/2.2/search/advanced"
    query = "python " + query
    print("")
    search_params = {
        "site": "stackoverflow",
        "q": query,
        "sort": "relevance",
        "order": "desc",
    }

    try:
        search_response = requests.get(search_api_url, params=search_params)
        search_response.raise_for_status()
        search_data = search_response.json()

        if "items" in search_data and len(search_data["items"]) > 0:
            most_relevant_answer_id = search_data["items"][0]["question_id"]

            answer_api_url = f"https://api.stackexchange.com/2.2/questions/{most_relevant_answer_id}/answers"

            answer_params = {
                "site": "stackoverflow",
                "sort": "votes",
                "order": "desc",
                "filter": "withbody",
            }

            answer_response = requests.get(answer_api_url, params=answer_params)
            answer_response.raise_for_status()
            answer_data = answer_response.json()

            if "items" in answer_data and len(answer_data["items"]) > 0:
                answer_body = answer_data["items"][0]["body"]
                text_maker = html2text.HTML2Text()
                text_maker.ignore_links = True
                sanitized_answer = text_maker.handle(answer_body)
                sanitized_answer = '\n'.join(line for line in sanitized_answer.splitlines() if line.strip())

                question_id = answer_data["items"][0]["question_id"]

                question_link = f"https://stackoverflow.com/questions/{question_id}"

                answer_with_link = f"For more info, click this line: {question_link}"
                print("Most relevant answer:")
                print(sanitized_answer)
                print("")
                return answer_with_link

        return "No answers found for this error, try debugging yourself."

    except requests.exceptions.RequestException as e:
        return "Error making API request:", str(e)

if __name__ == '__main__':
    #print(check_e())
    print(searchStack(check_e()))