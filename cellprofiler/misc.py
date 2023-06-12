import re
import boto3  #Amazon Web Services (AWS) 的 Python SDK，用於與 AWS 服務交互。

def generate_presigned_url(url):
    """
    Generate a presigned URL, if necessary (e.g., s3).
    :param url: An unsigned URL.
    :return: The presigned URL.
    """
    if url.startswith("s3"): #url 是否以 “s3” 開頭
        client = boto3.client("s3")  #創建一個 類型為 S3 的客戶端對象
        bucket_name, filename = (
            re.compile("s3://([\w\d\-.]+)/(.*)").search(url).groups()  #在 url 中搜索，並返回所有捕獲組
        )
        url = client.generate_presigned_url(  #生成預先簽名的 URL
            "get_object", #操作名稱
            Params={"Bucket": bucket_name, "Key": filename.replace("+", " ")},
        )
    return url
