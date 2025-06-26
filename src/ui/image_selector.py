"""UI logic for image selection and preview in the Anki card workflow."""

import os
import tempfile
import webbrowser

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