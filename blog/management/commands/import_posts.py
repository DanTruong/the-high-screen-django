import json

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime

from blog.models import Post, Category


AUTHOR_MAP = {
    "Alain Pierre-Lys": "alain_pierre_lys",
    "Celina Bonifacio": "celina_bonifacio",
    "Cole Frederick": "cole_frederick",
    "Daniliz Capellán Pichardo": "daniliz_capellan_pichardo",
    "Elliott Altland": "elliott_altland",
    "Joe Mags": "joe_mags",
    "Kwame Belle": "kwame_belle",
    "Moraima Capellán Pichardo": "moraima_capellan_pichardo",
    "Navzad Dabu": "navzad_dabu",
    "Ross Bentley": "ross_bentley",
    "Stuart Seidel": "stuart_seidel",
    "THS Staff": "ths_staff",
    "Taylor Nigrelli": "taylor_nigrelli",
    "Taylor Pangman": "taylor_pangman",
    "Tim Mullhaupt": "tim_mullhaupt",
    "Zach Tennen": "zach_tennen",
}


class Command(BaseCommand):
    help = "Import blog posts from a JSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            "json_file",
            type=str,
            help="Path to the JSON file containing posts",
        )

    def handle(self, *args, **options):
        User = get_user_model()
        json_file = options["json_file"]

        with open(json_file, "r", encoding="utf-8") as file:
            posts = json.load(file)

        imported_count = 0
        skipped_count = 0
        author_count = 0
        category_count = 0

        for item in posts:
            author_name = item["author"]

            # Make sure the author exists in our mapping.
            if author_name not in AUTHOR_MAP:
                self.stdout.write(
                    self.style.ERROR(
                        f'Unknown author "{author_name}" '
                        f'for post "{item["title"]}". Skipping.'
                    )
                )
                skipped_count += 1
                continue

            username = AUTHOR_MAP[author_name]

            # Split the author's name into first/last name.
            if author_name == "THS Staff":
                first_name = "THS"
                last_name = "Staff"
            else:
                name_parts = author_name.split(" ", 1)
                first_name = name_parts[0]
                last_name = (
                    name_parts[1]
                    if len(name_parts) > 1
                    else ""
                )

            # Create author if the Django user does not exist.
            author, author_created = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                },
            )

            if author_created:
                # Historical author accounts do not need login access.
                author.set_unusable_password()
                author.save()

                author_count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created author: "{author_name}" '
                        f'({username})'
                    )
                )

            # Create the post.
            post, post_created = Post.objects.get_or_create(
                slug=item["slug"],
                defaults={
                    "title": item["title"],
                    "body": item["body"],
                    "author": author,
                    "published_on": parse_datetime(item["date"]),
                },
            )

            if not post_created:
                self.stdout.write(
                    self.style.WARNING(
                        f'Skipped existing post: "{post.title}"'
                    )
                )

                skipped_count += 1
                continue

            # Add categories.
            for category_name in item.get("categories", []):
                category, category_created = (
                    Category.objects.get_or_create(
                        name=category_name
                    )
                )

                if category_created:
                    category_count += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Created category: "{category_name}"'
                        )
                    )

                post.categories.add(category)

            imported_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'Imported: "{post.title}"'
                )
            )

        # Final summary
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS("Import complete.")
        )
        self.stdout.write(
            f"Posts imported: {imported_count}"
        )
        self.stdout.write(
            f"Posts skipped: {skipped_count}"
        )
        self.stdout.write(
            f"Authors created: {author_count}"
        )
        self.stdout.write(
            f"Categories created: {category_count}"
        )