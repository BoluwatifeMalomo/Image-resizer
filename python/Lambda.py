import os
import io
import boto3
from PIL import Image

s3 = boto3.client('s3')

RESIZED_BUCKET = os.environ['RESIZED_BUCKET']
WIDTH = int(os.environ.get('RESIZE_WIDTH', '300'))
HEIGHT = int(os.environ.get('RESIZE_HEIGHT', '300'))

def _derive_output_key(src_key: str) -> str:
    if '/' in src_key:
        path, filename = src_key.rsplit('/', 1)
        name, _ext = os.path.splitext(filename)
        return f"{path}/resized-{name}.jpg"
    else:
        name, _ext = os.path.splitext(src_key)
        return f"resized-{name}.jpg"

def lambda_handler(event, context):
    bucket = event.get('bucket')
    key = event.get('key')
    print(f"[INFO] Start resize: s3://{bucket}/{key} -> bucket={RESIZED_BUCKET} size={WIDTH}x{HEIGHT}")

    try:
        # 1) Download source
        obj = s3.get_object(Bucket=bucket, Key=key)
        data = obj['Body'].read()

        # 2) Open with Pillow
        img = Image.open(io.BytesIO(data))
        # Convert to RGB so we can always save JPEG (handles PNG with alpha)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # 3) Resize quickly with good quality (preserves aspect ratio)
        img.thumbnail((WIDTH, HEIGHT), Image.LANCZOS)

        # 4) Save to memory
        out_buf = io.BytesIO()
        img.save(out_buf, format='JPEG', quality=85)
        out_buf.seek(0)

        # 5) Upload
        resized_key = _derive_output_key(key)
        s3.put_object(
            Bucket=RESIZED_BUCKET,
            Key=resized_key,
            Body=out_buf,
            ContentType='image/jpeg'
        )

        print(f"[SUCCESS] Wrote s3://{RESIZED_BUCKET}/{resized_key}")
        return {"status": "success", "resized_key": resized_key, "destination_bucket": RESIZED_BUCKET}

    except s3.exceptions.NoSuchKey:
        msg = f"Object not found: s3://{bucket}/{key}"
        print(f"[ERROR] {msg}")
        return {"status": "failed", "error": msg}
    except Exception as e:
        print(f"[ERROR] {e}")
        return {"status": "failed", "error": str(e)}

