from rake_nltk import Rake
import json


with open("job_data.txt", "r") as f:
    jobs = f.readlines()

r = Rake()

for job in jobs:
    job_json = json.loads(job)
    job_desc = job_json.get("job_desc", "")

    r.extract_keywords_from_text(job_desc)
    keywordList           = []
    rankedList            = r.get_ranked_phrases_with_scores()
    for keyword in rankedList:
        keyword_updated       = keyword[1].split()
        keyword_updated_string    = " ".join(keyword_updated[:2])
        keywordList.append(keyword_updated_string)
        # if(len(keywordList)>9):
        #     break
    print(job_desc)
    print(rankedList)
    