import React, { useState } from 'react';
import './App.css';
import pokedexBase from './images/pokedex.png';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [selectedCard, setSelectedCard] = useState(null);
  const [collection, setCollection] = useState([]);
  const [viewCollection, setViewCollection] = useState(false);
  const [showImage, setShowImage] = useState(false);

  const handleSearch = async (e) => {
    if (e.key === 'Enter' && query !== '') {
      const response = await fetch(`http://192.168.86.41:5000/api/cards?name=${query}`);
      const data = await response.json();
      setResults(data);
    }
  };

  const handleCardClick = (card) => {
    setSelectedCard(card);
  };

  const handleBackClick = () => {
    setSelectedCard(null);
    setViewCollection(false);
    setShowImage(false);
  };

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('image', file);

    const response = await fetch('http://192.168.86.41:5000/api/card', {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();
    if (response.ok) {
      setCollection([...collection, data[0]]); // Add the card to the collection
      setSelectedCard(data[0]); // Display the card details
    } else {
      console.error(data.message); // Log error message if any
    }
  };

  const handleInputChange = (e) => {
    setQuery(e.target.value);
    if (e.target.value === '') {
      setResults([]); // Clear the results when the search bar is cleared
    }
  };

  const handleViewCollectionClick = () => {
    setViewCollection(true);
    setSelectedCard(null); // Ensure the selected card view is cleared
  };

  const handleImageClick = () => {
    setShowImage(!showImage);
  };

  return (
    <div className="pokedex-container">
      <img src={pokedexBase} className="pokedex-base" alt="Pokedex Base" />
      {viewCollection ? (
        <div className="collection-box">
          <button className="back-button" onClick={handleBackClick}>Back</button>
          <h2>Card Collection</h2>
          {collection.map((card, index) => (
            <div key={index} className="collection-item">
              <img src={card.images.small} alt={card.name} className="collection-image" />
              <p>{card.name}</p>
            </div>
          ))}
        </div>
      ) : selectedCard ? (
        <div className="card-details-box">
          <button className="back-button" onClick={handleBackClick}>Back</button>
          {showImage ? (
            <div className="expanded-image-box">
              <img
                src={selectedCard.images.large}
                alt={selectedCard.name}
                className="card-image-expanded"
                onClick={handleImageClick}
              />
            </div>
          ) : (
            <>
              <img
                src={selectedCard.images.small}
                alt={selectedCard.name}
                className="card-image-large"
                onClick={handleImageClick}
              />
              <div className="card-details-large">
                <h2>{selectedCard.name}</h2>
                <p>Set: {selectedCard.set_name}</p>
                <p>Rarity: {selectedCard.rarity}</p>
                <p>Artist: {selectedCard.artist}</p>
              </div>
            </>
          )}
        </div>
      ) : (
        <>
          <div className="results-box">
            {results.map((result, index) => (
              <div key={index} className="result-item" onClick={() => handleCardClick(result)}>
                <p className="card-name">{result.name}</p>
                <p className="card-set">Set: {result.set_name}</p>
              </div>
            ))}
          </div>
          <input
            type="text"
            className="search-bar"
            placeholder="Search for a card"
            value={query}
            onChange={handleInputChange}
            onKeyDown={handleSearch}
          />
          <input
            type="file"
            accept="image/*"
            capture="camera"
            className="camera-button"
            onChange={handleImageUpload}
          />
          <button className="collection-button" onClick={handleViewCollectionClick}>VC</button>
        </>
      )}
    </div>
  );
}

export default App;

