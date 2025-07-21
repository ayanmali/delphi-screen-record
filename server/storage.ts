import { recordings, type Recording, type InsertRecording } from "@shared/schema";
import fs from "fs";
import path from "path";

export interface IStorage {
  getRecording(id: number): Promise<Recording | undefined>;
  getAllRecordings(): Promise<Recording[]>;
  createRecording(recording: InsertRecording): Promise<Recording>;
  deleteRecording(id: number): Promise<boolean>;
  saveRecordingFile(filename: string, buffer: Buffer): Promise<string>;
  getRecordingFile(filename: string): Promise<Buffer | null>;
  deleteRecordingFile(filename: string): Promise<boolean>;
  getStorageStats(): Promise<{ used: number; total: number }>;
}

export class MemStorage implements IStorage {
  private recordings: Map<number, Recording>;
  private currentId: number;
  private recordingsDir: string;

  constructor() {
    this.recordings = new Map();
    this.currentId = 1;
    this.recordingsDir = path.join(process.cwd(), "recordings");
    
    // Ensure recordings directory exists
    if (!fs.existsSync(this.recordingsDir)) {
      fs.mkdirSync(this.recordingsDir, { recursive: true });
    }
  }

  async getRecording(id: number): Promise<Recording | undefined> {
    return this.recordings.get(id);
  }

  async getAllRecordings(): Promise<Recording[]> {
    return Array.from(this.recordings.values()).sort(
      (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    );
  }

  async createRecording(insertRecording: InsertRecording): Promise<Recording> {
    const id = this.currentId++;
    const recording: Recording = {
      ...insertRecording,
      id,
      createdAt: new Date(),
      hasAudio: insertRecording.hasAudio ?? true,
      thumbnailUrl: insertRecording.thumbnailUrl || null,
    };
    this.recordings.set(id, recording);
    return recording;
  }

  async deleteRecording(id: number): Promise<boolean> {
    const recording = this.recordings.get(id);
    if (recording) {
      // Delete the file
      await this.deleteRecordingFile(recording.filename);
      // Remove from memory
      this.recordings.delete(id);
      return true;
    }
    return false;
  }

  async saveRecordingFile(filename: string, buffer: Buffer): Promise<string> {
    const filePath = path.join(this.recordingsDir, filename);
    await fs.promises.writeFile(filePath, buffer);
    return filePath;
  }

  async getRecordingFile(filename: string): Promise<Buffer | null> {
    try {
      const filePath = path.join(this.recordingsDir, filename);
      return await fs.promises.readFile(filePath);
    } catch (error) {
      return null;
    }
  }

  async deleteRecordingFile(filename: string): Promise<boolean> {
    try {
      const filePath = path.join(this.recordingsDir, filename);
      await fs.promises.unlink(filePath);
      return true;
    } catch (error) {
      return false;
    }
  }

  async getStorageStats(): Promise<{ used: number; total: number }> {
    let totalSize = 0;
    const recordingArray = Array.from(this.recordings.values());
    for (const recording of recordingArray) {
      totalSize += recording.fileSize;
    }
    
    // Mock total storage limit (10GB)
    const totalLimit = 10 * 1024 * 1024 * 1024;
    
    return {
      used: totalSize,
      total: totalLimit,
    };
  }
}

export const storage = new MemStorage();
