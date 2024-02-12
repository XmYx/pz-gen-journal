# HTML template for the newspaper
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Generative Journal</title>
    <style>
        body {
            font-family: 'Times New Roman', Times, serif;
            background-color: #f4f4f4;
            max-width: 800px;
            margin: auto;
            padding: 20px;
        }
        .article {
            background-color: #fff;
            padding: 15px;
            margin-bottom: 20px;
            box-shadow: 0 0 10px #ccc;
        }
        .article h2, .article h3 {
            border-bottom: 1px solid #aaa;
            padding-bottom: 5px;
        }
        .article img {
            max-width: 100%;
            height: auto;
        }
        .category {
            font-weight: bold;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>Generative Journal</h1>
    {% for category, articles in content.items() %}
        <div class="category">{{ category.capitalize() }}</div>
        {% for article in articles %}
            <div class="article">
                <h2>{{ article.title }}</h2>
                <h3>{{ article.subtitle }}</h3>
                <img src="{{ article.image }}" alt="Article image">
                <p>{{ article.text }}</p>
            </div>
        {% endfor %}
    {% endfor %}
</body>
</html>
"""