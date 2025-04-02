"use client";
import { useState } from "react";
import CourseSelector from "./components/CourseSelector";
import FileSelector from "./components/FileSelector";
import ChatBox from "./components/ChatBox";

export default function Home() {
  const [courseId, setCourseId] = useState(null);
  const [selectedFiles, setSelectedFiles] = useState([]);

  return (
    <main className="min-h-screen p-6 bg-gray-50">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-6 text-center text-black">Canvas RAG Chat</h1>
        <CourseSelector onSelect={(id) => setCourseId(id)} />
        {courseId && (
          <>
            <FileSelector
              courseId={courseId}
              onSelectionChange={(files) => setSelectedFiles(files)}
            />
            <ChatBox courseId={courseId} selectedFiles={selectedFiles} />
          </>
        )}
      </div>
    </main>
  );
}