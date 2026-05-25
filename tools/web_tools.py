import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

def web_search(query: str, max_results: int = 3) -> str:
    """Searches the web and returns titles, URLs, and snippets."""
    try:
        # DDGS provides free, keyless search access
        results = DDGS().text(query, max_results=max_results)
        formatted_results = []
        for res in results:
            formatted_results.append(f"Title: {res['title']}\nURL: {res['href']}\nSnippet: {res['body']}")
        
        return "\n\n".join(formatted_results) if formatted_results else "No results found."
    except Exception as e:
        return f"Search failed: {str(e)}"


def read_url(url: str) -> str:
    """Extract clean readable text from webpage."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted elements
        for tag in soup([
            "script", "style", "nav", "footer",
            "header", "aside", "noscript"
        ]):
            tag.decompose()

        # Prefer article/main content
        main_content = soup.find("article")

        if not main_content:
            main_content = soup.find("main")

        if not main_content:
            main_content = soup.body

        text = main_content.get_text(
            separator=" ",
            strip=True
        )

        # Clean extra spaces
        text = " ".join(text.split())

        # Limit output size
        return (
            text[:2000] + "\n...[Content Truncated]..."
            if len(text) > 2000
            else text
        )

    except Exception as e:
        return f"Failed to read URL: {str(e)}"

if __name__ == "__main__":
    # Test the functions when running this script directly
    print("Testing Web Search:")
    print(web_search("latest changes to GSTR-3B filing rules"))
    print("\nTesting URL Reader:")
    print(read_url("https://en.wikipedia.org/wiki/Artificial_intelligence")[:500])