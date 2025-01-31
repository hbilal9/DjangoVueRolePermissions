from storages.backends.s3boto3 import S3Boto3Storage

class CustomS3Storage(S3Boto3Storage):
    def url(self, name):
        url = super().url(name)
        return url 
    def delete(self, name):
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=name)
        except Exception as e:
            print(e)
        super().delete(name)