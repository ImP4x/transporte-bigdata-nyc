import boto3

BUCKET_NAME = 'bigdatataxi'

s3 = boto3.client('s3')

# Subir archivos
s3.upload_file('../data/final_data.csv', BUCKET_NAME, 'final_data.csv')
s3.upload_file('../visualizations/heatmap.png', BUCKET_NAME, 'heatmap.png')

print("Archivos subidos exitosamente a S3.")