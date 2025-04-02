import { useEffect, useState } from "react";

export default function FileSelector({ courseId, onSelectionChange }) {
  const [files, setFiles] = useState([]);
  const [selected, setSelected] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:8000/canvas/courses/${courseId}/files`)
      .then((res) => res.json())
      .then((data) => setFiles(data));
  }, [courseId]);

  const handleToggle = (url) => {
    const updated = selected.includes(url)
      ? selected.filter((u) => u !== url)
      : [...selected, url];
    setSelected(updated);
    onSelectionChange(updated);
  };

  return (
    <div className="p-4">
      {/* Tabs (Lectures, Homework, etc.) can go here based on file categories */}
      {files.map((file) => (
        <div key={file.id} className="text-black">
          <input
            type="checkbox"
            onChange={() => handleToggle(file.url)}
            className="text-black"
          />
          {file.name}
        </div>
      ))}
    </div>
  );
}