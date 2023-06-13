from blog.gcloud import GoogleCloudMediaFileStorage
storage = GoogleCloudMediaFileStorage()


class Upload:

    @staticmethod
    def upload_image(file, filename):
        try:
            path = storage.save(filename, file)
            return storage.url(path)
        except Exception as e:
            print("Failed to upload image!", e)
