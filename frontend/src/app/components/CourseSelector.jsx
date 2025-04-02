"use client";
import { useEffect, useState } from "react";

export default function CourseSelector({ onSelect }) {
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/canvas/courses")
      .then((res) => res.json())
      .then((data) => setCourses(data));
  }, []);

  return (
    <div className="mb-4">
      <label style = {{color:"black", backgroundColor: "white"}} className="block mb-2 font-semibold text-black">Select a Course:</label>
      <select
        style = {{color:"black", backgroundColor:"white"}}
        className="p-2 border rounded w-full text-black"
        onChange={(e) => onSelect(Number(e.target.value))}
      >
        <option value="">-- Choose --</option>
        {courses.map((course) => (
          <option key={course.id} value={course.id}>
            {course.name}
          </option>
        ))}
      </select>
    </div>
  );
}
