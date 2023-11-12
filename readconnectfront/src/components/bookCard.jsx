import React, { useState } from "react";
//from "react-icons/fa"; import the down and up chevron icons
import { FaChevronDown, FaChevronUp } from "react-icons/fa";

const BookCard = ({ book, handleSearch }) => {
  
  const addToWishlist = async (id) => {
    const result = await fetch(`/books/${id}/wish`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await result.json();
  };
  const addToRead = async (id) => {
    const result = await fetch(`/books/${id}/read`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await result.json();
  };

  const [showDetails, setShowDetails] = useState(false);
  const [rating, setRating] = useState("");
  const [longDescription, setLongDescription] = useState(false);

  const handleRating = (e) => {
    setRating(e.target.value);
  };

  const handleDescription = () => {
    setLongDescription(!longDescription);
  };

  return (
    <div
      className={`book-card ${showDetails ? "showing-details" : ""}`}
      key={book.id}
    >
      <div>
        <img src={book.thumbnail_url} alt={book.title} />
        <div>
          {book.authors.map((author) => (
            <p key={author}>{author}</p>
          ))}
        </div>
      </div>
      <div className="middle-section">
        <h2
          className="title"
          onClick={() => {
            setShowDetails(!showDetails);
          }}
        >
          {book.title}
          <span>
            {showDetails ? (
              <FaChevronUp
                size={18}
                onClick={() => setShowDetails(!showDetails)}
              />
            ) : (
              <FaChevronDown
                size={18}
                onClick={() => setShowDetails(!showDetails)}
              />
            )}
          </span>
        </h2>
        <p className="short-description">
          {showDetails ? book.long_description : book.short_description}
        </p>
        {
          //show buttons to allow to add to reading list, already read list, and wishlist
          showDetails ? (
            <div>
              <button
                className="addto-button"
                onClick={() => addToWishlist(book.id)}
              >
                Añadir a Lista de lectura
              </button>
              <button
                className="addto-button"
                onClick={() => addToRead(book.id)}
              >
                Añadir a leídos
              </button>
            </div>
          ) : null
        }
        <hr />
        <div className="middle-section">
          <div>
            {book.authors.map((author) => (
              <button
                key={author}
                onClick={() =>
                  handleSearch({
                    target: { value: author, name: "author" },
                  })
                }
                className="author-btn"
              >
                {author}
              </button>
            ))}
          </div>
        </div>
      </div>
      {showDetails && (
        <div className="book-details">
          <p>{book.publication_date}</p>
          <div>
            {book.categories.map((category) => (
              <button
                key={category}
                onClick={() =>
                  handleSearch({
                    target: { value: category, name: "category" },
                  })
                }
                className="author-btn"
              >
                {category}
              </button>
            ))}
          </div>
          <p>Rating: {rating}</p>
          <select onChange={handleRating}>
            <option value="">Calificar libro</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
          </select>
          {/* Include book reviews */}
        </div>
      )}
    </div>
  );
};

export { BookCard };
