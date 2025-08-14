# Google Cloud Storage Setup Guide

This guide will help you set up Google Cloud Storage for video uploads in the Delphi Screen Recording Service.

## Prerequisites

1. A Google Cloud Platform account
2. A Google Cloud project
3. Google Cloud Storage enabled in your project

## Setup Steps

### 1. Create a Google Cloud Storage Bucket

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Navigate to **Cloud Storage** > **Buckets**
4. Click **Create Bucket**
5. Choose a unique bucket name (e.g., `themus-screen-recordings`)
6. Configure the bucket settings:
   - **Location**: Choose a region close to your users
   - **Storage class**: Standard (recommended for videos)
   - **Access control**: Uniform (recommended)
   - **Protection tools**: Enable as needed

### 2. Create a Service Account

1. In the Google Cloud Console, go to **IAM & Admin** > **Service Accounts**
2. Click **Create Service Account**
3. Give it a name (e.g., `themus-screen-record-service`)
4. Add a description (e.g., "Service account for Delphi screen recording uploads")
5. Click **Create and Continue**

### 3. Grant Permissions

1. For the service account, add these roles:
   - **Storage Object Admin** (for full read/write access to objects)
   - **Storage Object Viewer** (for read-only access if needed)

2. Click **Done**

### 4. Create and Download Service Account Key

1. Click on the service account you just created
2. Go to the **Keys** tab
3. Click **Add Key** > **Create New Key**
4. Choose **JSON** format
5. Click **Create**
6. The key file will download automatically - keep it secure!

### 5. Configure Environment Variables

Create a `.env` file in the service directory with these variables:

```bash
# Google Cloud Storage Configuration
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GCS_BUCKET_NAME=your-bucket-name

# Google Cloud Authentication
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
```

Replace the values with your actual project ID, bucket name, and path to the service account key file.

### 6. Alternative: Environment Variable Authentication

Instead of using a service account key file, you can set the credentials as environment variables:

```bash
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GCS_BUCKET_NAME=your-bucket-name

# Service account credentials as environment variables
GOOGLE_CLOUD_PRIVATE_KEY_ID=your-private-key-id
GOOGLE_CLOUD_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
GOOGLE_CLOUD_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
GOOGLE_CLOUD_CLIENT_ID=your-client-id
GOOGLE_CLOUD_AUTH_URI=https://accounts.google.com/o/oauth2/auth
GOOGLE_CLOUD_TOKEN_URI=https://oauth2.googleapis.com/token
GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
GOOGLE_CLOUD_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com
```

## Security Best Practices

1. **Never commit service account keys to version control**
2. **Use environment variables or secure secret management**
3. **Grant minimal required permissions**
4. **Regularly rotate service account keys**
5. **Monitor access logs**

## Testing the Setup

1. Start your service with the environment variables set
2. Try uploading a video file using the `/recordings/` endpoint
3. Check that the file appears in your Google Cloud Storage bucket
4. Verify that the download and stream endpoints return valid URLs

## Troubleshooting

### Common Issues

1. **Authentication Error**: Check that your service account key is valid and has the correct permissions
2. **Bucket Not Found**: Verify the bucket name and that it exists in the specified project
3. **Permission Denied**: Ensure the service account has the necessary IAM roles
4. **File Upload Fails**: Check that the bucket allows public access if you're using public URLs

### Debug Commands

```bash
# Test GCS connection
python -c "
from google.cloud import storage
client = storage.Client()
buckets = list(client.list_buckets())
print('Available buckets:', [b.name for b in buckets])
"
```

## Cost Considerations

- **Storage**: Standard storage costs ~$0.02 per GB per month
- **Network**: Egress costs vary by region (~$0.12 per GB)
- **Operations**: Class A operations (uploads) cost ~$0.004 per 10,000 operations
- **Consider using lifecycle policies** to move old videos to cheaper storage classes

## Next Steps

1. Set up monitoring and alerting for storage costs
2. Implement video compression to reduce storage costs
3. Consider using signed URLs for secure access
4. Set up backup and disaster recovery procedures 