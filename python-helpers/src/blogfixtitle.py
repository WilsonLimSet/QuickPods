import os
import re

# Directory containing your blog files
BLOG_DIR = os.path.join(os.path.dirname(__file__), "../../content")


# Function to extract metadata from the content
def extract_metadata(content):
    title_match = re.search(r'^title:\s*"(.*?)"', content, re.MULTILINE)
    date_match = re.search(r'^date:\s*"(.*?)"', content, re.MULTILINE)
    tags_match = re.search(r"^tags:\s*\[(.*?)\]", content, re.MULTILINE)

    title = title_match.group(1) if title_match else "Untitled"
    date = date_match.group(1) if date_match else "Unknown Date"
    tags = tags_match.group(1) if tags_match else ""

    # Remove metadata lines from content
    content = re.sub(r'^title:\s*".*?"\s*$', "", content, flags=re.MULTILINE)
    content = re.sub(r'^date:\s*".*?"\s*$', "", content, flags=re.MULTILINE)
    content = re.sub(r"^tags:\s*\[.*?\]\s*$", "", content, flags=re.MULTILINE)

    return title, date, tags, content


# Function to remove existing front matter
def remove_existing_front_matter(content):
    front_matter_pattern = re.compile(
        r"^---\s*\ntitle:.*?\ntags:.*?\n---\s*\n", re.DOTALL
    )
    return front_matter_pattern.sub("", content)


# Function to add front matter to the content
def add_front_matter(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Remove existing front matter if present
    content = remove_existing_front_matter(content)

    title, date, tags, content = extract_metadata(content)

    front_matter = f'---\ntitle: "{title}"\ndate: "{date}"\ntags: [{tags}]\n---\n\n'
    new_content = front_matter + content.strip()  # Strip leading/trailing whitespace

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(new_content)


# Process all Markdown files in the directory
for filename in os.listdir(BLOG_DIR):
    if filename.endswith(".md"):
        file_path = os.path.join(BLOG_DIR, filename)
        add_front_matter(file_path)
        print(f"Processed {filename}")

print("All blog files have been updated with front matter.")
