from django.conf import settings
from minio import Minio
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.response import *

def process_file_upload(file_object: InMemoryUploadedFile, client, image_name):
    try:
        client.put_object('mininglogo', image_name, file_object, file_object.size)
        return f"http://localhost:9000/mininglogo/{image_name}"
    except Exception as e:
        return {"error": str(e)}

def add_pic(new_miningService, mining_pic):
    client = Minio(           
            endpoint=settings.AWS_S3_ENDPOINT_URL,
           access_key=settings.AWS_ACCESS_KEY_ID,
           secret_key=settings.AWS_SECRET_ACCESS_KEY,
           secure=settings.MINIO_USE_SSL
    )
    i = new_miningService.mining_service_id
    img_obj_name = f"{i}.png"

    if not mining_pic:
        return Response({"error": "Нет файла для изображения логотипа."})
    result = process_file_upload(mining_pic, client, img_obj_name)

    if 'error' in result:
        return Response(result)

    new_miningService.url = result
    new_miningService.save()

    return Response({"message": "success"})

def process_file_delete(client, mining_image_name):
    try:
        client.remove_object('mininglogo', mining_image_name)
        return {'status':'success'}
    except Exception as e:
        return {'ERROR': str(e)}

def del_pic(Mining_service):
    client = Minio(           
        endpoint=settings.AWS_S3_ENDPOINT_URL,
        access_key=settings.AWS_ACCESS_KEY_ID,
        secret_key=settings.AWS_SECRET_ACCESS_KEY,
        secure=settings.MINIO_USE_SSL
    )
    mining_pic_url = Mining_service.url
    if mining_pic_url:
        mining_pic_url = '/'.join(mining_pic_url.split('/')[4:])

    result = process_file_delete(client, mining_pic_url)
    if 'error' in result:
        return Response(result)
    return Response({"message":"success"})

