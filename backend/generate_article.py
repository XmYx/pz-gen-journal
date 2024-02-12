import json

from openai import OpenAI
client = OpenAI()


def generate_article(TOD="morning", level="main", category="News", history=["Zombies", "Outbreak", "Death of a McWalk", "Forest Adventures"]):

    response = client.chat.completions.create(
      model="gpt-4-turbo-preview",
      messages=[
        {
          "role": "system",
          "content": "You are a post apocalyptic journalist with a grime sense of humour,"
                     " and a bit of gore hidden between the pages,"
                     " but with very sophisticated taste for food, wines, fishing, outdoor activities, and cars."
                     " You will be presented with a few keywords from the previous articles in the topic,"
                     " and the category you are writing for, then you must answer with a Json containing the headline,"
                     " the article, and the image_prompt if an illustration image is required. There may be references to"
                     " old stories, but mainly, the articles have to be new, and unique."
        },
        {
          "role": "user",
          "content": f"Let's write today {TOD}'s {level} article in {category} category. History: f{[f'{item}, ' for item in history]}"
        },
      ],
      temperature=1,
      max_tokens=2048,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      response_format={"type": "json_object"},
    )
    return response


def parse_article(completion):
  try:
    # Extract the JSON string from the completion object
    json_str = completion.choices[0].message.content
    # Parse the JSON string to a Python dictionary
    article_data = json.loads(json_str)
    # Safely extract the required fields
    return {
      "category": article_data.get('category', 'Unknown'),
      "headline": article_data.get('headline', 'No headline provided'),
      "article": article_data.get('article', 'No article content provided'),
      "prompt": article_data.get('image_prompt', 'No image prompt provided')
    }
  except Exception as e:
    print(f"Error parsing article completion: {e}")
    return None
