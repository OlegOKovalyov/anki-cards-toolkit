"""UI logic for image selection and preview in the Anki card workflow."""

import os
import tempfile
import webbrowser
from src.services.pexels_api import fetch_pexels_images

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
        print("Зображень не знайдено.")
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
                print(f"❌ Будь ласка, введіть число від 1 до {len(images)}")
        except ValueError:
            print("❌ Будь ласка, введіть правильне число")

def select_image_for_card(word: str) -> str:
    """
    Fetches images for the given word, shows a preview page, and returns the selected image URL.

    Returns:
    - If the user selects a valid image number, return the corresponding image URL.
    - If the user presses Enter or inputs an invalid number, return the first image URL.
    - If the user presses Escape, return an empty string.
    - If no images are found, also return an empty string.
    """
    print("\n🔍 Пошук відповідних зображень...")
    images = fetch_pexels_images(word)
    if not images:
        print("⚠️ Зображень не знайдено. Продовжую без зображення.")
        return ""
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
                print("✅ Вибрано перше зображення за замовчуванням.")
                return images[0]['src']['medium']
            if choice.lower() in {"esc", "escape"}:
                os.unlink(gallery_path)
                print("⚠️ Зображення не вибрано. Продовжую без зображення.")
                return ""
            idx = int(choice)
            if 1 <= idx <= len(images):
                os.unlink(gallery_path)
                print("✅ Зображення успішно вибрано.")
                return images[idx - 1]['src']['medium']
            else:
                os.unlink(gallery_path)
                print("⚠️ Номер поза діапазоном. Вибрано перше зображення за замовчуванням.")
                return images[0]['src']['medium']
        except ValueError:
            print(f"❌ Будь ласка, введіть число від 1 до {len(images)}, Enter для першого, або Esc для пропуску.") 