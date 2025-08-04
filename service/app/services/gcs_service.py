import mimetypes
import os
import logging
from typing import Optional
from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class GoogleCloudStorageService:
    """
    Service for handling Google Cloud Storage operations
    """
    
    def __init__(self):
        self.bucket_name = os.getenv("GCS_BUCKET_NAME")
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        
        if not self.bucket_name:
            raise ValueError("GCS_BUCKET_NAME environment variable is required")
        
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable is required")
        
        # Initialize the GCS client
        try:
            self.client = storage.Client(project=self.project_id)
            self.bucket = self.client.bucket(self.bucket_name)
            
            # Verify bucket exists
            if not self.bucket.exists():
                raise ValueError(f"Bucket {self.bucket_name} does not exist")
                
        except Exception as e:
            logger.error(f"Failed to initialize Google Cloud Storage client: {e}")
            raise HTTPException(
                status_code=500, 
                detail="Failed to initialize cloud storage service"
            )
    
    # async def upload_file(
    #     self, 
    #     file_content: bytes, 
    #     filename: str, 
    #     content_type: Optional[str] = None,
    #     make_public: bool = True
    # ) -> Tuple[str, str]:
    #     """
    #     Upload a file to Google Cloud Storage
        
    #     Args:
    #         file_content: The file content as bytes
    #         filename: The name to give the file in GCS
    #         content_type: Optional content type for the file
    #         make_public: Whether to make the file publicly accessible
            
    #     Returns:
    #         Tuple of (public_url, gcs_path)
    #     """
    #     try:
    #         # Create blob
    #         blob = self.bucket.blob(filename)
            
    #         # Set content type if provided
    #         if content_type:
    #             blob.content_type = content_type
            
    #         # Upload the file
    #         blob.upload_from_string(
    #             file_content,
    #             content_type=content_type or 'application/octet-stream'
    #         )
            
    #         # Make the blob publicly readable if requested
    #         if make_public:
    #             # When uniform bucket-level access is enabled, we can't use make_public()
    #             # Instead, we'll construct the public URL manually
    #             public_url = f"https://storage.googleapis.com/{self.bucket_name}/{filename}"
    #         else:
    #             public_url = None
                
    #         gcs_path = f"gs://{self.bucket_name}/{filename}"
            
    #         logger.info(f"Successfully uploaded {filename} to GCS")
    #         return public_url, gcs_path
            
    #     except GoogleCloudError as e:
    #         logger.error(f"Google Cloud Storage error uploading {filename}: {e}")
    #         raise HTTPException(
    #             status_code=500,
    #             detail=f"Failed to upload file to cloud storage: {str(e)}"
    #         )
    #     except Exception as e:
    #         logger.error(f"Unexpected error uploading {filename}: {e}")
    #         raise HTTPException(
    #             status_code=500,
    #             detail=f"Failed to upload file: {str(e)}"
    #         )
    
    # async def generate_signed_url(
    #     self, 
    #     filename: str, 
    #     expiration_minutes: int = 60,
    #     method: str = "GET"
    # ) -> Optional[str]:
    #     """
    #     Generate a signed URL for secure access to a file
        
    #     Args:
    #         filename: The name of the file
    #         expiration_minutes: How long the URL should be valid (default: 60 minutes)
    #         method: HTTP method allowed (GET, PUT, DELETE, etc.)
            
    #     Returns:
    #         Signed URL if successful, None otherwise
    #     """
    #     try:
    #         blob = self.bucket.blob(filename)
            
    #         if not blob.exists():
    #             logger.warning(f"File {filename} does not exist in GCS")
    #             return None
            
    #         # Generate signed URL
    #         expiration = datetime.now() + timedelta(minutes=expiration_minutes)
    #         signed_url = blob.generate_signed_url(
    #             version="v4",
    #             expiration=expiration,
    #             method=method
    #         )
            
    #         logger.info(f"Generated signed URL for {filename} (expires in {expiration_minutes} minutes)")
    #         return signed_url
            
    #     except GoogleCloudError as e:
    #         logger.error(f"Google Cloud Storage error generating signed URL for {filename}: {e}")
    #         return None
    #     except Exception as e:
    #         logger.error(f"Unexpected error generating signed URL for {filename}: {e}")
    #         return None

    async def upload_file(self, file_content: bytes, filename: str, content_type: Optional[str] = None) -> str:
        """
        Upload a file to Google Cloud Storage bucket
        
        Args:
            file_content: The file content as bytes
            filename: The name of the file to store in GCS
            content_type: Optional content type. If not provided, will be auto-detected
            
        Returns:
            str: The public URL of the uploaded file
            
        Raises:
            HTTPException: If upload fails
        """
        try:
            # Auto-detect content type if not provided
            if not content_type:
                content_type, _ = mimetypes.guess_type(filename)
                if not content_type:
                    # Default to application/octet-stream for unknown types
                    content_type = "application/octet-stream"
            
            # Create a blob object
            blob = self.bucket.blob(filename)
            
            # Set content type
            blob.content_type = content_type
            
            # Upload the file content
            blob.upload_from_string(
                file_content,
                content_type=content_type,
                timeout=300  # 5 minutes timeout for large video files
            )
            
            # Make the blob publicly readable (optional - remove if you want private files)
            # blob.make_public()
            
            logger.info(f"Successfully uploaded {filename} to bucket {self.bucket_name}")
            
            # Return the public URL or signed URL
            return f"gs://{self.bucket_name}/{filename}"
            
        except GoogleCloudError as e:
            logger.error(f"Google Cloud Storage error uploading {filename}: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload file to cloud storage: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error uploading {filename}: {e}")
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred during file upload"
            )
    
    async def upload_video_file(self, file_content: bytes, filename: str) -> str:
        """
        Specialized method for uploading video files with appropriate settings
        
        Args:
            file_content: The video file content as bytes
            filename: The name of the video file
            
        Returns:
            str: The GCS URL of the uploaded video
        """
        # Common video MIME types
        video_extensions = {
            '.mp4': 'video/mp4',
            '.avi': 'video/x-msvideo',
            '.mov': 'video/quicktime',
            '.wmv': 'video/x-ms-wmv',
            '.flv': 'video/x-flv',
            '.webm': 'video/webm',
            '.mkv': 'video/x-matroska',
            '.m4v': 'video/x-m4v'
        }
        
        # Get file extension
        file_ext = os.path.splitext(filename.lower())[1]
        content_type = video_extensions.get(file_ext, 'video/mp4')
        
        return await self.upload_file(file_content, filename, content_type)
    
    def get_signed_url(self, filename: str, expiration_minutes: int = 60) -> str:
        """
        Generate a signed URL for accessing a private file
        
        Args:
            filename: Name of the file in the bucket
            expiration_minutes: URL expiration time in minutes
            
        Returns:
            str: Signed URL for the file
        """
        try:
            blob = self.bucket.blob(filename)
            
            # Generate signed URL
            url = blob.generate_signed_url(
                expiration=expiration_minutes * 60,  # Convert to seconds
                method='GET'
            )
            
            return url
            
        except Exception as e:
            logger.error(f"Error generating signed URL for {filename}: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate access URL"
            )
    
    async def delete_file(self, filename: str) -> bool:
        """
        Delete a file from Google Cloud Storage
        
        Args:
            filename: The name of the file to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        try:
            blob = self.bucket.blob(filename)
            
            if blob.exists():
                blob.delete()
                logger.info(f"Successfully deleted {filename} from GCS")
                return True
            else:
                logger.warning(f"File {filename} does not exist in GCS")
                return False
                
        except GoogleCloudError as e:
            logger.error(f"Google Cloud Storage error deleting {filename}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting {filename}: {e}")
            return False
    
    async def get_file_url(self, filename: str) -> Optional[str]:
        """
        Get the public URL of a file in Google Cloud Storage
        
        Args:
            filename: The name of the file
            
        Returns:
            The public URL if the file exists, None otherwise
        """
        try:
            blob = self.bucket.blob(filename)
            
            if blob.exists():
                # When uniform bucket-level access is enabled, construct URL manually
                return f"https://storage.googleapis.com/{self.bucket_name}/{filename}"
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error getting URL for {filename}: {e}")
            return None

# Global instance
gcs_service = GoogleCloudStorageService() 