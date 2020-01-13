import React, { useState, useEffect } from "react";
import { Button, Row, Col } from "react-bootstrap";
import {
  persistJson,
  savePictureWithClass,
  getUnclassifiedImageUrl
} from "util";
import "./App.css";

function App() {
  const [currentUserEmail, setCurrentUserEmail] = useState("default@gmail.com");
  const [currentImageUrl, setCurrentImageUrl] = useState("");
  // Identifier for a valid/invalid pull, or if photo not even a pullup
  const VALID_PULLUP = "1";
  const INVALID_PULLUP = "0";
  const INVALID_IMAGE = "-1";

  const setNewImageUrl = () => {
    fetch(getUnclassifiedImageUrl)
      .then(response => response.json())
      .then(data => {
        console.log(data);
        setCurrentImageUrl(data.url);
      });
  };

  const saveImageWithClass = classType => {
    fetch(savePictureWithClass, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        userEmail: currentUserEmail,
        url: currentImageUrl,
        class: classType
      })
    });
  };

  useEffect(() => setNewImageUrl(), []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={currentImageUrl} className="App-logo" alt="logo" />
        <Row>
          <Col>
            <Button
              onClick={() => {
                saveImageWithClass(VALID_PULLUP);
                setNewImageUrl();
              }}
            >
              Valid Pullup
            </Button>
          </Col>
          <Col>
            <Button
              onClick={() => {
                saveImageWithClass(INVALID_PULLUP);
                setNewImageUrl();
              }}
            >
              Invalid Pullup
            </Button>
          </Col>
          <Col>
            <Button
              onClick={() => {
                saveImageWithClass(INVALID_IMAGE);
                setNewImageUrl();
              }}
            >
              Not a Pullup
            </Button>
          </Col>
        </Row>
      </header>
    </div>
  );
}

// Persist data once the user closes window
window.addEventListener("beforeunload", ev => {
  fetch(persistJson);
});

export default App;
