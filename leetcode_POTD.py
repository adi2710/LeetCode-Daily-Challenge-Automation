""" leetcode_POTD.py:
To fetch and submit Daily LeetCoding Challenge if forgot

Settings-
1. Add cookies value in cred.yml
2. Update LEETCODE_SESSION value, in case of failure.

Suggestion - Use Task Scheduler/ Cron Job to run this script daily
"""
import requests
import base64
from config import CONFIG, Logger

CONFIG = CONFIG["leetcode"]
logger = Logger("leet_POTD")


def get_daily_leetcoding_challenge_question():
    cookies = CONFIG["cookies"]
    url_query = "https://leetcode.com/graphql/"
    payload = {
        "query": "\n query questionOfToday {\n activeDailyCodingChallengeQuestion {\n date\n userStatus\n question "
        "{\n frontendQuestionId: questionFrontendId\n questionId\n titleSlug\n difficulty\n \n }\n }\n}\n",
        "variables": {},
    }

    page = requests.post(url_query, cookies=cookies, json=payload)
    result = page.json()["data"]["activeDailyCodingChallengeQuestion"]
    logger.log(f"{result['date']} : ")
    is_submitted = result["userStatus"] == "Finish"
    question = result["question"]
    question.update({'userStatus': is_submitted})

    return question.values()  # order as in payload["query"]


def get_solution(title_slug):
    lang = CONFIG["global_lang"]
    github_token = CONFIG["github_token"]
    headers = {}
    if github_token:
        headers['Authorization'] = f"token {github_token}"
    folder = {'cpp': 'C++', 'python': 'Python'}
    extension = {'cpp': 'cpp', 'python': 'py'}

    url = f"https://api.github.com/repos/kamyu104/LeetCode-Solutions/contents/{folder[lang]}/{title_slug}.{extension[lang]}"
    response = requests.get(url, headers=headers).json()

    solution, solution_encoding = response['content'], response['encoding']

    if solution_encoding == 'base64':
        solution = base64.b64decode(solution).decode()

    return solution


def submit_solution(qid, title_slug, solution):
    cookies = CONFIG["cookies"]
    lang = CONFIG["global_lang"]

    new_submission = f"https://leetcode.com/problems/{title_slug}/submit/"
    headers = {
        "referer": f"https://leetcode.com/problems/{title_slug}/submissions/",
        "x-csrftoken": cookies["csrftoken"],
    }
    payload = {"lang": lang, "question_id": qid, "typed_code": solution}
    page = requests.post(
        new_submission, headers=headers, cookies=cookies, json=payload, timeout=60
    )

    return page.status_code, page.text


if __name__ == "__main__":
    display_qid, qid, title_slug, question_difficulty, is_submitted = get_daily_leetcoding_challenge_question()
    if not is_submitted:
        solution = get_solution(title_slug)
        status_code, response_text = submit_solution(qid, title_slug, solution)

        if status_code == 200:
            result = f"{status_code} {response_text}"
        elif status_code == 404:
            result = f"No old solution found for {qid=}. [{display_qid}: {title_slug}]"
        else:
            result = f"{status_code} - Try changing LEETCODE_SESSION value using cookies"
    else:
        result = f"Solution already submitted for {qid=}. [{display_qid}: {title_slug}]"
    logger.log(f"{result} ({question_difficulty}) \n")