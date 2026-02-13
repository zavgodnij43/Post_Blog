from flask import Flask, render_template, request, redirect, url_for
from db import *

app = Flask(__name__, template_folder="templates")

# Ініціалізація бази даних
init_db()

# Перевірка: якщо немає розділів, заповнюємо тестовими даними
if len(get_blog_sections()) == 0:
    seed_data()
    print("✅ Додано тестові розділи")


@app.route("/")
def index():
    sections = get_blog_sections()

    # Отримуємо всі пости з усіх розділів
    all_posts = []
    for section in sections:
        posts = get_section_posts(section["id"])
        # Конвертуємо кожен пост у словник і додаємо інформацію про розділ
        for post in posts:
            post_dict = dict(post)  # Конвертуємо Row в dict
            post_dict["section_name"] = section["name"]
            post_dict["section_slug"] = section["slug"]
            all_posts.append(post_dict)

    # Сортуємо пости за датою (найновіші першими)
    all_posts.sort(key=lambda x: x.get("id", 0), reverse=True)

    return render_template("index.html", sections=sections, posts=all_posts)


@app.route("/<section_slug>")
def section_page(section_slug):
    sections = get_blog_sections()
    section = get_section_by_slug(section_slug)

    if not section:
        return "Розділ не знайдено!", 404

    posts = get_section_posts(section["id"])

    return render_template("section.html", sections=sections, section=section, posts=posts)


@app.route("/add", methods=["GET", "POST"])
def add_post():
    sections = get_blog_sections()

    if request.method == "POST":
        # Отримуємо дані з форми
        text = request.form.get("text")  # Текст поста
        image = request.form.get("image")  # Шлях до зображення (або None)
        section_id = request.form.get("section")

        # Зберігаємо пост у базу даних
        create_new_post(text, image, section_id)

        # Перенаправляємо на сторінку розділу
        section = get_section_by_id(section_id)
        if section:
            return redirect(url_for("section_page", section_slug=section["slug"]))
        else:
            return redirect(url_for("index"))

    return render_template("add_post.html", sections=sections)


if __name__ == "__main__":
    app.run(debug=True)
