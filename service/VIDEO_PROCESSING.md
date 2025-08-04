# Video Processing with OpenCV

This service provides comprehensive video processing capabilities using OpenCV for videos stored in Google Cloud Storage.

## Features

- **Video Analysis**: Extract video properties (FPS, resolution, duration)
- **Frame Extraction**: Extract key frames from videos
- **Motion Detection**: Detect motion in video sequences
- **Thumbnail Generation**: Generate and upload video thumbnails
- **Content Analysis**: Analyze brightness, contrast, and other visual properties
- **Custom Processing**: Download videos for custom OpenCV processing

## Installation

1. Install the required dependencies:
```bash
pip install opencv-python numpy
```

2. Make sure your environment variables are set:
```bash
export GCS_BUCKET_NAME="your-bucket-name"
export GOOGLE_CLOUD_PROJECT_ID="your-project-id"
```

## API Endpoints

### 1. Process Video with Specific Operations

**POST** `/api/recordings/{recording_id}/process`

Process a video with specified OpenCV operations.

**Request Body:**
```json
{
  "operations": ["extract_frames", "detect_motion", "generate_thumbnail", "analyze_content"]
}
```

**Available Operations:**
- `extract_frames`: Extract key frames from video
- `detect_motion`: Detect motion in video
- `generate_thumbnail`: Generate and upload thumbnail
- `analyze_content`: Analyze video content (brightness, contrast)
- `extract_audio_info`: Extract audio information

**Response:**
```json
{
  "recording_id": 123,
  "filename": "recordings/recording_1234567890.mp4",
  "operations": ["extract_frames", "detect_motion"],
  "results": {
    "video_info": {
      "fps": 30.0,
      "frame_count": 1800,
      "width": 1920,
      "height": 1080,
      "duration": 60.0,
      "resolution": "1920x1080"
    },
    "frames": {
      "total_frames_extracted": 10,
      "frame_interval": 180,
      "frames": [...]
    },
    "motion_detection": {
      "total_motion_frames": 45,
      "motion_threshold": 30,
      "motion_frames": [...]
    }
  }
}
```

### 2. Create Video Summary

**POST** `/api/recordings/{recording_id}/summary`

Create a comprehensive video summary with all available analysis.

**Response:**
```json
{
  "recording_id": 123,
  "filename": "recordings/recording_1234567890.mp4",
  "summary": {
    "video_info": {...},
    "frames": {...},
    "motion_detection": {...},
    "thumbnail": "recordings/recording_1234567890_thumbnail.jpg",
    "content_analysis": {
      "average_brightness": 127.5,
      "average_contrast": 45.2,
      "brightness_range": {"min": 50, "max": 200},
      "frames_analyzed": 100
    }
  }
}
```

### 3. Extract Video Frames

**GET** `/api/recordings/{recording_id}/frames?frame_count=10`

Extract key frames from a video recording.

### 4. Detect Motion

**GET** `/api/recordings/{recording_id}/motion`

Detect motion in a video recording.

## Usage Examples

### Python Script Example

```python
import asyncio
from app.services.video_processor import video_processor
from app.services.gcs_service import gcs_service

async def process_video():
    # Get video for processing
    gcs_filename = "recordings/recording_1234567890.mp4"
    
    # Method 1: Create comprehensive summary
    summary = await video_processor.create_video_summary(gcs_filename)
    print(f"Video duration: {summary['video_info']['duration']} seconds")
    
    # Method 2: Process specific operations
    operations = ['extract_frames', 'detect_motion']
    results = await video_processor.process_video(gcs_filename, operations)
    
    # Method 3: Download for custom processing
    temp_file_path = await gcs_service.get_video_for_processing(gcs_filename, use_temp_file=True)
    
    # Use OpenCV for custom processing
    import cv2
    cap = cv2.VideoCapture(temp_file_path)
    # ... your custom processing code ...
    cap.release()
    
    # Clean up
    import os
    os.unlink(temp_file_path)

# Run the example
asyncio.run(process_video())
```

### Custom OpenCV Processing

```python
import cv2
import numpy as np

async def custom_video_processing(gcs_filename):
    # Download video to temp file
    temp_video_path = await gcs_service.get_video_for_processing(gcs_filename, use_temp_file=True)
    
    # Open video with OpenCV
    cap = cv2.VideoCapture(temp_video_path)
    
    # Process frames
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Your custom processing here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (15, 15), 0)
        
        # Example: Detect circles
        circles = cv2.HoughCircles(
            blur, cv2.HOUGH_GRADIENT, 1, 20,
            param1=50, param2=30, minRadius=0, maxRadius=0
        )
        
        if circles is not None:
            print(f"Detected {len(circles[0])} circles")
    
    cap.release()
    
    # Clean up
    import os
    os.unlink(temp_video_path)
```

## Performance Considerations

1. **Large Videos**: For large videos, use `use_temp_file=True` to avoid loading the entire video into memory.

2. **Processing Time**: Video processing can be time-consuming. Consider implementing background tasks for long-running operations.

3. **Memory Usage**: OpenCV operations can be memory-intensive. Monitor memory usage when processing large videos.

4. **Concurrent Processing**: The service supports concurrent video processing, but be mindful of system resources.

## Error Handling

The service includes comprehensive error handling:

- **File Not Found**: Returns 404 if video file doesn't exist in GCS
- **Processing Errors**: Returns 500 with detailed error messages
- **Invalid Operations**: Validates operation names before processing
- **Memory Errors**: Handles out-of-memory situations gracefully

## Dependencies

- `opencv-python>=4.8.0`: OpenCV for video processing
- `numpy>=1.24.0`: Numerical computing
- `google-cloud-storage>=3.2.0`: GCS integration
- `fastapi[standard]>=0.116.1`: Web framework

## Troubleshooting

### Common Issues

1. **OpenCV Installation**: Make sure OpenCV is properly installed with video codec support.

2. **GCS Permissions**: Ensure your service account has read access to the GCS bucket.

3. **Memory Issues**: For large videos, consider processing in chunks or using streaming.

4. **Codec Support**: Some video formats may require additional codecs. Install `opencv-contrib-python` for extended codec support.

### Debug Mode

Enable debug logging to troubleshoot issues:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Advanced Usage

### Batch Processing

```python
async def batch_process_videos(gcs_filenames):
    tasks = []
    for filename in gcs_filenames:
        task = video_processor.create_video_summary(filename)
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

### Custom Video Filters

```python
async def apply_custom_filter(gcs_filename):
    temp_path = await gcs_service.get_video_for_processing(gcs_filename, use_temp_file=True)
    
    cap = cv2.VideoCapture(temp_path)
    
    # Apply custom filter
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Example: Apply sepia filter
        sepia = cv2.transform(frame, np.array([
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131]
        ]))
        
        # Process filtered frame...
    
    cap.release()
    os.unlink(temp_path)
``` 