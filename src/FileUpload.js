// src/components/FileUpload.js
import React, { useState } from 'react';
import axios from 'axios';
import './FileUpload.css';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [dataTypes, setDataTypes] = useState([]);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://127.0.0.1:8000/data/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setDataTypes(response.data);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  const friendlyDataType = (inferredType) => {
    switch (inferredType) {
      case 'object':
        return 'Text';
      case 'int64':
        return 'Integer';
      case 'float64':
        return 'Floating Point Number';
      case 'datetime64[ns]':
        return 'Date';
      default:
        return inferredType;
    }
  };

  return (
    <div className="file-upload-container">
      <h2 className="title">Upload a CSV or Excel File</h2>
      <form onSubmit={handleSubmit} className="upload-form">
        <input type="file" onChange={handleFileChange} className="file-input" />
        <button type="submit" className="upload-button">Upload</button>
      </form>

      {dataTypes.length > 0 && (
        <ul className="data-types-list">
          {dataTypes.map((col, index) => (
            <li key={index} className="data-type-item">
              <span className="column-name">{col.column_name}</span>: <span className="data-type">{friendlyDataType(col.inferred_data_type)}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default FileUpload;
