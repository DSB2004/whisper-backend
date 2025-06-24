from imagekitio import ImageKit
from whisper import settings
import os
from urllib.parse import urlparse


class Storage:
    imagekit = ImageKit(
        private_key=settings.CLOUD_PRIVATE_KEY,
        public_key=settings.CLOUD_PUBLIC_KEY,
        url_endpoint = settings.CLOUD_URL
    )
    @classmethod
    def uploadFile(cls, file):
        file_name = getattr(file, 'name', 'upload.jpg')
        try:
            result = cls.imagekit.upload_file(
                file=file,
                file_name=file_name,
                options={
                    "folder": "/uploads/",
                    "use_unique_file_name": True
                }
            )

            if result.get("response") and result["response"].get("url"):
                return result["response"]["url"]
            else:
                print("Upload failed:", result.get("error"))
                return None

        except Exception:
            return None
        
    @classmethod
    def deleteFile(cls, fileUrl):
        fileName = os.path.basename(urlparse(fileUrl).path)
        result = cls.imagekit.list_files({"name": fileName})

        if result.get("response") and len(result["response"]) > 0:
            fileId = result["response"][0]["fileId"]
            delete_result = cls.imagekit.delete_file(fileId)

            if delete_result.get("response"):
                    return True
            else:
                    return False
        else:
                return False