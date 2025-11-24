import wikipediaapi
import random


wiki = wikipediaapi.Wikipedia(
    user_agent="MasterschoolWikiProject/1.0 (mailto:ledodurmishaj@gmail.com)",
    language="en",
    extract_format=wikipediaapi.ExtractFormat.WIKI,
)

def get_categories():
    """
    Fetch top-level categories dynamically from Wikipedia.
    Return a list of categories (strings).
    """
    root_title = "Category:Main topic classifications"
    root = wiki.page(root_title)

    if not root.exists():
        print(f"Page does not exist: {root_title}")
        return []

    categories = []
    for title, member in root.categorymembers.items():
        if member.ns == wikipediaapi.Namespace.CATEGORY:
            categories.append(title.replace("Category:", "", 1))
    return sorted(set(categories))


def get_articles(category, limit=5):
    if not category:
        return []
    full_title = category if category.startswith("Category:") else f"Category:{category}"
    cat_page = wiki.page(full_title)
    if not cat_page.exists():
        print(f"Category does not exist: {full_title}")
        return []

    articles = []
    for title, member in cat_page.categorymembers.items():
        if member.ns == wikipediaapi.Namespace.MAIN:
            articles.append(title)
            if len(articles) >= limit:
                break
    return articles



def get_page(title):
    if not title:
        return None
    page = wiki.page(title)
    if not page.exists():
        print(f"Page does not exist: {title}")
        return None
    else:
        return page



def get_rand_categories(n : int = 1):
    """
    Return N random top-level categories (or all if n >= total).
    """
    cats = get_categories()
    if not cats:
        return []
    if n > len(cats):
        raise ValueError(f"Requested {n} but only {len(cats)} categories available")
    return random.sample(cats, n)


def get_summarized_article(title, sentences=1):
    """
    Get a short summary (first `sentences` sentences) for an article title.
    Returns (title, summary) or None if not found.
    """
    page = get_page(title)
    if not page:
        return None
    text = page.summary or page.text or ""
    parts = text.split(". ")
    clipped = ". ".join(parts[:sentences]).strip()
    if clipped and not clipped.endswith("."):
        clipped += "."
    return page.title, clipped



