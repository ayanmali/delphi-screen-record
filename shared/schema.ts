import { pgTable, text, serial, integer, timestamp, boolean } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const recordings = pgTable("recordings", {
  id: serial("id").primaryKey(),
  title: text("title").notNull(),
  filename: text("filename").notNull(),
  fileSize: integer("file_size").notNull(),
  duration: integer("duration").notNull(), // in seconds
  format: text("format").notNull(), // mp4, webm
  createdAt: timestamp("created_at").defaultNow().notNull(),
  hasAudio: boolean("has_audio").notNull().default(true),
  thumbnailUrl: text("thumbnail_url"),
});

export const insertRecordingSchema = createInsertSchema(recordings).omit({
  id: true,
  createdAt: true,
});

// Client-side metadata schema (excludes fileSize since it's determined server-side)
export const clientMetadataSchema = insertRecordingSchema.omit({
  fileSize: true,
});

export type InsertRecording = z.infer<typeof insertRecordingSchema>;
export type ClientMetadata = z.infer<typeof clientMetadataSchema>;
export type Recording = typeof recordings.$inferSelect;

// Recording options schema
export const recordingOptionsSchema = z.object({
  screenSource: z.enum(["entire", "window", "tab"]),
  includeMicrophone: z.boolean(),
  includeSystemAudio: z.boolean(),
  microphoneVolume: z.number().min(0).max(100),
  format: z.enum(["mp4", "webm"]),
});

export type RecordingOptions = z.infer<typeof recordingOptionsSchema>;
