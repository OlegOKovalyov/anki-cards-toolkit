"""UI logic for image selection and preview in the Anki card workflow."""

import os
import tempfile
import webbrowser
from src.services.pexels_api import fetch_pexels_images
from docs.messages import DATA_GATHERING_PROCESSING

def create_image_selection_page(images, word):
    """Create HTML page for image selection."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    template_path = os.path.join(project_root, "templates/image_selection.html")
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    image_grid_html = ""
    for i, photo in enumerate(images, 1):
        image_grid_html += f"""
            <div class=\"image-container\">
                <img src=\"{photo['src']['medium']}\" alt=\"Image {i}\">
                <div class=\"image-number\">{i}</div>
            </div>
        """
    html = template.replace('{{word}}', word)
    html = html.replace('{{image_grid}}', image_grid_html)
    return html

def select_image(images, word):
    """Interactive image selection interface with visual preview."""
    if not images:
        print(DATA_GATHERING_PROCESSING["no_images_found"])
        return None
    html_content = create_image_selection_page(images, word)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8') as f:
        f.write(html_content)
        gallery_path = f.name
    webbrowser.open('file://' + os.path.abspath(gallery_path))
    while True:
        try:
            choice = input("\n🔢 Введіть номер зображення (1-16) або натисніть Enter для пропуску: ").strip()
            if not choice:
                os.unlink(gallery_path)
                return None
            choice = int(choice)
            if 1 <= choice <= len(images):
                os.unlink(gallery_path)
                return images[choice - 1]['src']['medium']
            else:
                print(DATA_GATHERING_PROCESSING["image_invalid_number"].format(max=len(images)))
        except ValueError:
            print(DATA_GATHERING_PROCESSING["image_invalid_input"])

def select_image_for_card(word: str) -> str:
    """
    Fetches images for the given word, shows a preview page, and returns the selected image URL.

    Returns:
    - If the user selects a valid image number, return the corresponding image URL.
    - If the user presses Enter or inputs an invalid number, return the first image URL.
    - If the user presses Escape, return an empty string.
    - If no images are found, also return an empty string.
    """
    print(DATA_GATHERING_PROCESSING["image_searching"])
    images = fetch_pexels_images(word)
    if not images:
        print(DATA_GATHERING_PROCESSING["image_none_continue"])
        return ""
    print(DATA_GATHERING_PROCESSING["image_found_count"].format(count=len(images)))
    print(f"Знайдено {len(images)} зображень. Відкриваю попередній перегляд у браузері...")
    html_content = create_image_selection_page(images, word)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8') as f:
        f.write(html_content)
        gallery_path = f.name
    webbrowser.open('file://' + os.path.abspath(gallery_path))
    while True:
        try:
            choice = input(f"\n🔢 Введіть номер (1-{len(images)}) або натисніть Enter: ").strip()
            if choice == "":
                os.unlink(gallery_path)
                print(DATA_GATHERING_PROCESSING["image_default_selected"])
                return images[0]['src']['medium']
            if choice.lower() in {"esc", "escape"}:
                os.unlink(gallery_path)
                print(DATA_GATHERING_PROCESSING["image_skip_notice"])
                return ""
            idx = int(choice)
            if 1 <= idx <= len(images):
                os.unlink(gallery_path)
                print(DATA_GATHERING_PROCESSING["image_selected"])
                return images[idx - 1]['src']['medium']
            else:
                os.unlink(gallery_path)
                print(DATA_GATHERING_PROCESSING["image_out_of_range"])
                return images[0]['src']['medium']
        except ValueError:
            print(DATA_GATHERING_PROCESSING["image_number_full_prompt"].format(max=len(images))) 