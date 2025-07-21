import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { insertRecordingSchema, clientMetadataSchema, recordingOptionsSchema } from "@shared/schema";
import multer from "multer";
import path from "path";

// Configure multer for file uploads
const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 500 * 1024 * 1024, // 500MB limit
  },
});

export async function registerRoutes(app: Express): Promise<Server> {
  // Get all recordings
  app.get("/api/recordings", async (req, res) => {
    try {
      const recordings = await storage.getAllRecordings();
      res.json(recordings);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch recordings" });
    }
  });

  // Get specific recording
  app.get("/api/recordings/:id", async (req, res) => {
    try {
      const id = parseInt(req.params.id);
      const recording = await storage.getRecording(id);
      if (!recording) {
        return res.status(404).json({ message: "Recording not found" });
      }
      res.json(recording);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch recording" });
    }
  });

  // Create new recording
  app.post("/api/recordings", upload.single("video"), async (req, res) => {
    try {
      if (!req.file) {
        return res.status(400).json({ message: "No video file provided" });
      }

      const recordingData = JSON.parse(req.body.metadata);
      const validatedData = clientMetadataSchema.parse(recordingData);

      // Generate unique filename
      const timestamp = Date.now();
      const extension = path.extname(validatedData.filename);
      const uniqueFilename = `recording_${timestamp}${extension}`;

      // Save file
      await storage.saveRecordingFile(uniqueFilename, req.file.buffer);

      // Create recording record
      const recording = await storage.createRecording({
        ...validatedData,
        filename: uniqueFilename,
        fileSize: req.file.size,
      });

      res.json(recording);
    } catch (error) {
      console.error("Error creating recording:", error);
      res.status(500).json({ message: "Failed to save recording" });
    }
  });

  // Download recording file
  app.get("/api/recordings/:id/download", async (req, res) => {
    try {
      const id = parseInt(req.params.id);
      const recording = await storage.getRecording(id);
      
      if (!recording) {
        return res.status(404).json({ message: "Recording not found" });
      }

      const fileBuffer = await storage.getRecordingFile(recording.filename);
      if (!fileBuffer) {
        return res.status(404).json({ message: "Recording file not found" });
      }

      res.setHeader("Content-Type", `video/${recording.format}`);
      res.setHeader("Content-Disposition", `attachment; filename="${recording.title}.${recording.format}"`);
      res.send(fileBuffer);
    } catch (error) {
      res.status(500).json({ message: "Failed to download recording" });
    }
  });

  // Stream recording file
  app.get("/api/recordings/:id/stream", async (req, res) => {
    try {
      const id = parseInt(req.params.id);
      const recording = await storage.getRecording(id);
      
      if (!recording) {
        return res.status(404).json({ message: "Recording not found" });
      }

      const fileBuffer = await storage.getRecordingFile(recording.filename);
      if (!fileBuffer) {
        return res.status(404).json({ message: "Recording file not found" });
      }

      res.setHeader("Content-Type", `video/${recording.format}`);
      res.send(fileBuffer);
    } catch (error) {
      res.status(500).json({ message: "Failed to stream recording" });
    }
  });

  // Delete recording
  app.delete("/api/recordings/:id", async (req, res) => {
    try {
      const id = parseInt(req.params.id);
      const success = await storage.deleteRecording(id);
      
      if (!success) {
        return res.status(404).json({ message: "Recording not found" });
      }

      res.json({ message: "Recording deleted successfully" });
    } catch (error) {
      res.status(500).json({ message: "Failed to delete recording" });
    }
  });

  // Get storage statistics
  app.get("/api/storage/stats", async (req, res) => {
    try {
      const stats = await storage.getStorageStats();
      res.json(stats);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch storage stats" });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
