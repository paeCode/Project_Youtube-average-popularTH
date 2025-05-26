const express = require('express');
const cors = require('cors');
const fs = require('fs');
const csv = require('fast-csv');
const bodyParser = require('body-parser');
const path = require('path');
import fs from 'fs';
import csv from 'csv-parser';
const app = express();
const PORT = 3000;
const CSV_FILE = path.join(__dirname, 'data', 'youtube_trending_categorized.csv');

app.use(cors());
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public'))); // สำหรับเสิร์ฟรูป mock

app.get('/api/videos', (req, res) => {
  const results = [];
  fs.createReadStream('./data/youtube_trending_categorized.csv')
    .pipe(csv())
    .on('data', (data) => results.push(data))
    .on('end', () => {
      res.json(results);
    });
});

// ✅ เพิ่ม route หลัก
app.get('/', (req, res) => {
  res.send('API ทำงานปกติแล้ว ✅');
});

app.listen(PORT, () => {
  console.log(`Server is running at http://localhost:${PORT}`);
});

// ✅ อ่าน CSV ทั้งหมด
app.get('/videos', (req, res) => {
  const results = [];
  fs.createReadStream(CSV_FILE)
    .pipe(csv.parse({ headers: true }))
    .on('data', (row) => {
      // เพิ่ม URL รูปภาพจำลอง
      row.image = `/images/default_thumbnail.jpg`;
      results.push(row);
    })
    .on('end', () => {
      res.json(results);
    });
});

// ✅ เพิ่มวิดีโอใหม่
app.post('/videos', (req, res) => {
  const newVideo = req.body;

  const ws = fs.createWriteStream(CSV_FILE, { flags: 'a' });
  csv
    .writeToStream(ws, [newVideo], { headers: false })
    .on('finish', () => res.json({ status: 'เพิ่มเรียบร้อย' }));
});

// ✅ แก้ไขวิดีโอ (ตามลำดับ index)
app.put('/videos/:index', (req, res) => {
  const indexToEdit = parseInt(req.params.index);
  const updatedVideo = req.body;
  const rows = [];

  fs.createReadStream(CSV_FILE)
    .pipe(csv.parse({ headers: true }))
    .on('data', (row) => rows.push(row))
    .on('end', () => {
      if (indexToEdit >= 0 && indexToEdit < rows.length) {
        rows[indexToEdit] = updatedVideo;
        const ws = fs.createWriteStream(CSV_FILE);
        csv.write(rows, { headers: true }).pipe(ws);
        res.json({ status: 'แก้ไขสำเร็จ' });
      } else {
        res.status(404).json({ error: 'ไม่พบลำดับนี้' });
      }
    });
});

// ✅ ลบวิดีโอ (ตาม index)
app.delete('/videos/:index', (req, res) => {
  const indexToDelete = parseInt(req.params.index);
  const rows = [];

  fs.createReadStream(CSV_FILE)
    .pipe(csv.parse({ headers: true }))
    .on('data', (row) => rows.push(row))
    .on('end', () => {
      if (indexToDelete >= 0 && indexToDelete < rows.length) {
        rows.splice(indexToDelete, 1);
        const ws = fs.createWriteStream(CSV_FILE);
        csv.write(rows, { headers: true }).pipe(ws);
        res.json({ status: 'ลบเรียบร้อย' });
      } else {
        res.status(404).json({ error: 'ไม่พบลำดับนี้' });
      }
    });
});

app.listen(PORT, () => {
  console.log(`🚀 Server started at http://localhost:${PORT}`);
});
