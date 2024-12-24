import json
import os
from groq import Groq
from dotenv import load_dotenv



load_dotenv(verbose=True)



client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

#
# article_content = {
#                 "uri": "2024-12-582651403",
#                 "lang": "eng",
#                 "isDuplicate": False,
#                 "date": "2024-12-21",
#                 "time": "17:26:24",
#                 "dateTime": "2024-12-21T17:26:24Z",
#                 "dateTimePub": "2024-12-21T17:25:16Z",
#                 "dataType": "news",
#                 "sim": 0.4235294163227081,
#                 "url": "https://www.infowars.com/posts/christmas-market-attack-suspect-was-saudi-arabian-leftist-asylum-activist-promoted-by-bbc",
#                 "title": "Christmas Market Attack Suspect Was Saudi 'Leftist' Asylum Activist Promoted By BBC",
#                 "body": "Suspect was also reportedly a Zionist who supported \"Greater Israel.\"\n\nThe suspect behind the Christmas Market terror attack in Germany that left multiple people dead and hundreds injured was a leftist Saudi national who was promoted by the BBC for his efforts to help asylum seekers into Germany.\n\nThe suspect, identified by German authorities as 50-year-old Taleb Al Abdulmohsen, was taken into custody Friday after driving a rented car into a crowd gathered for a Christmas market in Magdeburg that killed 5 and injured over 200.\n\nTaleb was an asylum seeker who arrived in Germany in 2006 after allegedly fleeing Saudi Arabia for fear of persecution for being an atheist.\n\nHe was granted asylum in Germany in 2016 and had been living in the town of Bernburg as a psychiatrist.\n\nThe BBC in 2019 featured Taleb describing how he ran a refugee program to help ex-Muslim women flee Sharia Law and the Saudi government's human rights abuses.\n\nThat same year, in an interview with FAZ, Taleb claimed he was \"the most aggressive critic of Islam in history,\" and that he was ostracized from the Muslim community in Germany over his atheism.\n\nHe also detailed his move to become a pro-asylum activist in Germany in the interview.\n\nFollowing his identification as the suspect behind the Christmas market attack, FAZ added an editor's note saying, \"This interview with Taleb Al A. was published in June 2019. Entries of the alleged assassin in the social media indicate that he has also been increasingly quarreling with Germany and its migration policy over the five and a half years since then. There are also signs of persecution delusions. Nothing of this was felt in 2019. Here is the unchanged wording of the conversation.\"\n\nAlthough the legacy media has focused on statements Taleb made in support of the populist right-wing Alternative for Germany (AfD) party over its critiques of mass immigration, he apparently considered himself to be a leftist.\n\n\"Taleb A. said in the interview that he was not a right-winger and described himself as a leftist,\" Der Spiegel reported.\n\nThe German government repeatedly ignored warnings from Saudi Arabia about Taleb as well as requests for his extradition last year.\n\nTaleb told German authorities that his motive for the attack was related to \"dissatisfaction with the way Saudi Arabian refugees are treated\" in Germany.\n\nDespite his purported atheism, Taleb also appears to be a Zionist who expressed his support for \"Greater Israel\" on social media.\n\nWhen Taleb's background was still unclear, the media was perfectly content reporting that a car was responsible for the horrific attack at the Christmas market.",
#                 "source": {
#                     "uri": "infowars.com",
#                     "dataType": "news",
#                     "title": "Infowars"
#                 },
#                 "authors": [],
#                 "image": "https://imagedelivery.net/aeJ6ID7yrMczwy3WKNnwxg/225c1d6f-6756-49ef-3fe8-2569b7300a00/w=800,h=450",
#                 "eventUri": "eng-10192203",
#                 "sentiment": -0.2705882352941177,
#                 "wgt": 92884,
#                 "relevance": 1
#             }

def get_json_from_groq_api(article_content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content":  (
                    f"{json.dumps(article_content)}\n\n"
                    "This is an article. I want to analyze a few things:\n"
                    "1. In what country did it happen?\n"
                    "2. Classify the article into one of the following categories: general news, historical terror attack, or nowadays terror attack.\n\n"
                    "After analyzing, provide a JSON with the following structure:\n"
                    "{\n"
                    "    \"category\": \"str\",\n"
                    "    \"country\": \"str\",\n"
                    "    \"city\": \"str\",\n"
                    "    \"continent\": \"str\",\n"
                    "    \"country_longitude\": \"int\",\n"
                    "    \"country_latitude\": \"int\",\n"                    
                    "}\n\n"
                    "Respond with the JSON only, without any extra text."
                ),
            }
        ],
        model="llama3-8b-8192",
    )




    data = json.loads(chat_completion.choices[0].message.content)
    return data
#
# if __name__ == '__main__':
#     data = get_json_from_groq_api(article_content)
#     print(data)