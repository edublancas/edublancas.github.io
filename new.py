import sys
import argparse
from datetime import datetime
from pathlib import Path


def create_post_file(slug):
    # Get the current date in YYYY-MM-DD format
    current_date = datetime.now().strftime("%Y-%m-%d")
    # Create the filename
    filename = f"{current_date}-{slug}.md"
    # Define the path to the _posts directory
    posts_dir = Path("_posts")
    # Ensure the _posts directory exists
    posts_dir.mkdir(exist_ok=True)
    # Create the full file path
    file_path = posts_dir / filename

    if file_path.exists():
        print(f"File {file_path} already exists")
        sys.exit(1)

    # Write the front matter to the file
    with file_path.open("w") as f:
        f.write("---\n")
        f.write(f"layout: post\n")
        f.write(f"title: \"{slug.replace('-', ' ').title()}\"\n")
        f.write("comments: false\n")
        f.write("---\n\n")
        f.write("# Your content here...\n")

    print(f"Created {file_path}")


def main():
    parser = argparse.ArgumentParser(description="Create a new post file.")
    parser.add_argument("slug", type=str, help="The slug for the post")
    args = parser.parse_args()

    create_post_file(args.slug)


if __name__ == "__main__":
    main()
