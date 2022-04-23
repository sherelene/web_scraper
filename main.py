from newspaper import Article
import nltk

# download nltk packages for tokenization
# nltk.download('punkt')


url = "https://www.opensourceforu.com/2016/02/ionic-a-ui-framework-to-simplify-hybrid-mobile-app-development/"

article = Article(url)

# 1 . Download the article
article.download()

# 2. Parse the article
article.parse()

# 3. Fetch Author Name(s)
print(article.authors)

# 4. Fetch Publication Date
print('Article Publication Date:')
print(article.publish_date)
# 5. The URL of the Major Image
print('Major Image in the article:')
print(article.top_image)

# 6. Natural Language Processing on Article to fetch Keywords
article.nlp()
print('Keywords in the article')
print(article.keywords)

# 7. Generate Summary of the article
print('Article Summary')
print(article.summary)