from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = "Verify Cloudinary media storage configuration by uploading a small test file."

    def handle(self, *args, **options):
        if not getattr(settings, "DEFAULT_FILE_STORAGE", "").endswith("MediaCloudinaryStorage"):
            self.stdout.write(
                self.style.WARNING(
                    "Cloudinary no está activo. Verificá que hayas seteado CLOUDINARY_CLOUD_NAME, "
                    "CLOUDINARY_API_KEY y CLOUDINARY_API_SECRET en las variables de entorno."
                )
            )
            return

        test_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
        path = default_storage.save("cloudinary_test.png", ContentFile(test_content))
        url = default_storage.url(path)
        self.stdout.write(self.style.SUCCESS(f"Upload OK: {url}"))
        self.stdout.write("Podés borrar el archivo 'cloudinary_test.png' desde el dashboard de Cloudinary.")
