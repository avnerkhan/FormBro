import React, { useState, useEffect } from "react";
import { Button, Row, Col } from "react-bootstrap";
import {
  persistJson,
  savePictureWithClass,
  getUnclassifiedImageUrl,
  getClassifiedImageUrl
} from "./util";
import "./App.css";

function App() {
  // Identifier for a valid/invalid pull, or if photo not even a pullup
  const VALID_PULLUP = 1;
  const INVALID_PULLUP = 0;
  const INVALID_IMAGE = -1;
  const UNCLASSIFIED_MODE = 0
  const CLASSIFIED_MODE = 1
  const [currentLabel, setCurrentLabel] = useState(INVALID_PULLUP)
  const [currentMode, setCurrentMode] = useState(UNCLASSIFIED_MODE)
  const [currentUserEmail, setCurrentUserEmail] = useState("default@gmail.com");
  const [currentUnclassifiedImageUrl, setCurrentUnclassifiedImageUrl] = useState("");
  const [currentClassifiedImageUrl, setCurrentClassifiedImageUrl] = useState("")

  const setNewImageUrl = () => {
    const currentUrl = currentMode === UNCLASSIFIED_MODE ? getUnclassifiedImageUrl : getClassifiedImageUrl
    fetch(currentUrl)
      .then(response => response.json())
      .then(data => {
        if (currentMode === CLASSIFIED_MODE) {
          setCurrentClassifiedImageUrl(data[2])
          setCurrentLabel(data[3])
        } else {
          setCurrentUnclassifiedImageUrl(data.url)
        }
      })
      .catch(error => console.log(error));
  };

  const saveImageWithClass = classType => {
    fetch(savePictureWithClass, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        userEmail: currentUserEmail,
        url: currentUnclassifiedImageUrl,
        class: classType
      })
    });
  };

  useEffect(() => setNewImageUrl(), []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={currentMode === UNCLASSIFIED_MODE ? currentUnclassifiedImageUrl : currentClassifiedImageUrl} className="App-logo" alt="logo" />
        <Row>
          {currentMode === UNCLASSIFIED_MODE ? (
            <div>
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

            </div>
          ) :
            <div>
              <div>{currentLabel}</div>
              <Button onClick={() => setNewImageUrl()}>Next </Button>
            </div>}
        </Row>
        <Button onClick={() => {
          setCurrentMode(currentMode === UNCLASSIFIED_MODE ? CLASSIFIED_MODE : UNCLASSIFIED_MODE)
          setNewImageUrl()
        }}>
          Toggle Mode
        </Button>
      </header>
    </div>
  );
}

//Persist data once the user closes window
window.addEventListener("beforeunload", ev => {
  fetch(persistJson);
});

export default App;
