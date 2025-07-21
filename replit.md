# Screen Recording Application

## Overview

This is a full-stack screen recording application built with React, TypeScript, Express.js, and Drizzle ORM. The application allows users to record their screen, manage recordings, and provides a clean interface for viewing and organizing recorded content. It follows a modern monorepo structure with shared schemas and clear separation between client and server code.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application uses a full-stack TypeScript architecture with the following main components:

### Frontend Architecture
- **Framework**: React with TypeScript
- **Build Tool**: Vite for fast development and optimized production builds
- **Styling**: Tailwind CSS with shadcn/ui component library
- **State Management**: TanStack Query for server state management
- **Routing**: Wouter for lightweight client-side routing
- **UI Components**: Radix UI primitives with custom styling

### Backend Architecture
- **Server Framework**: Express.js with TypeScript
- **Database ORM**: Drizzle ORM with PostgreSQL dialect
- **File Upload**: Multer for handling multipart/form-data
- **Database Provider**: Neon Database (serverless PostgreSQL)
- **Session Management**: PostgreSQL-based session storage

### Project Structure
The application follows a monorepo pattern with three main directories:
- `client/`: React frontend application
- `server/`: Express.js backend API
- `shared/`: Common schemas and types used by both client and server

## Key Components

### Database Schema
The application uses a single `recordings` table with the following structure:
- `id`: Serial primary key
- `title`: Recording title
- `filename`: Original filename
- `fileSize`: File size in bytes
- `duration`: Recording duration in seconds
- `format`: Video format (mp4, webm)
- `createdAt`: Creation timestamp
- `hasAudio`: Boolean indicating audio presence
- `thumbnailUrl`: Optional thumbnail URL

### API Endpoints
- `GET /api/recordings`: Retrieve all recordings
- `GET /api/recordings/:id`: Get specific recording
- `POST /api/recordings`: Create new recording with file upload
- `DELETE /api/recordings/:id`: Delete recording
- `GET /api/recordings/:id/download`: Download recording file
- `GET /api/storage/stats`: Get storage usage statistics

### Screen Recording Features
- Multiple screen capture options (entire screen, window, tab)
- Audio recording from microphone and system audio
- Recording controls (start/stop/pause/resume)
- Real-time recording preview
- Configurable recording format (MP4, WebM)
- File size validation (500MB limit)

### Storage Management
- In-memory storage implementation for development
- File storage in local `recordings` directory
- Storage statistics tracking
- File validation and error handling

## Data Flow

1. **Recording Process**:
   - User configures recording options
   - Browser requests screen capture permissions
   - MediaRecorder API captures screen/audio
   - Recording data is accumulated in chunks
   - On stop, data is packaged and uploaded to server

2. **File Upload**:
   - Client sends multipart form data with video file and metadata
   - Server validates file size and type
   - File is saved to local storage
   - Recording metadata is stored in database

3. **Playback & Management**:
   - Client fetches recordings list from API
   - Users can preview, download, or delete recordings
   - Storage statistics are displayed in sidebar

## External Dependencies

### Frontend Dependencies
- **UI Framework**: React with comprehensive Radix UI components
- **State Management**: TanStack Query for server state
- **Styling**: Tailwind CSS with CSS variables for theming
- **Form Handling**: React Hook Form with Zod validation
- **Icons**: Lucide React icon library

### Backend Dependencies
- **Database**: Drizzle ORM with Neon Database serverless PostgreSQL
- **File Upload**: Multer for handling multipart uploads
- **Session Storage**: PostgreSQL-based session management
- **Date Handling**: date-fns for date manipulation

### Development Tools
- **Build System**: Vite with hot module replacement
- **Type Checking**: TypeScript with strict mode enabled
- **Code Quality**: ESBuild for production bundling
- **Development Server**: Express with Vite middleware integration

## Deployment Strategy

The application is configured for deployment with the following approach:

### Build Process
1. **Client Build**: Vite builds the React application to `dist/public`
2. **Server Build**: ESBuild bundles the Express server to `dist/index.js`
3. **Database**: Drizzle migrations handle schema changes

### Environment Configuration
- Development uses Vite dev server with Express API proxy
- Production serves static files through Express
- Database connection configured via `DATABASE_URL` environment variable
- File storage uses local filesystem with configurable directory

### Production Considerations
- Static file serving through Express in production
- Error handling middleware for API endpoints
- Request logging for API routes
- File size limits and validation
- CORS configuration for cross-origin requests

The application is designed to be easily deployable to platforms like Replit, with built-in support for development banners and runtime error overlays in development mode.