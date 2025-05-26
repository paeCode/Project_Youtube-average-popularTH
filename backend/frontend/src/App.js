import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [videos, setVideos] = useState([]);

  useEffect(() => {
    fetch('http://localhost:3000/api/videos')
      .then((res) => res.json())
      .then((data) => setVideos(data));
  }, []);

  return (
    <div className="container">
      <h1>🔥 วิดีโอยอดนิยมบน YouTube</h1>
      <table>
        <thead>
          <tr>
            <th>ลำดับ</th>
            <th>ชื่อวิดีโอ</th>
            <th>ช่อง</th>
            <th>ยอดวิว</th>
            <th>เวลาโพสต์</th>
            <th>หมวดหมู่</th>
          </tr>
        </thead>
        <tbody>
          {videos.map((v, index) => (
            <tr
              key={index}
              style={{
                color: index < 10 ? 'red' : 'black',
              }}
            >
              <td>{v['ลำดับ']}</td>
              <td>{v['ชื่อวิดีโอ']}</td>
              <td>{v['ช่อง']}</td>
              <td>{v['ยอดวิว']}</td>
              <td>{v['เวลาโพสต์']}</td>
              <td>{v['หมวดหมู่']}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
