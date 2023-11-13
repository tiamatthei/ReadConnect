import React, { useState } from "react";
//from "react-icons/fa"; import the down and up chevron icons
import { FaChevronDown, FaChevronUp } from "react-icons/fa";

const BookCard = ({ book, handleSearch }) => {
  const [showDetails, setShowDetails] = useState(false);
  const [rating, setRating] = useState("");
  const [longDescription, setLongDescription] = useState(false);
  const [isRead, setIsRead] = useState(false);
  const [isWish, setIsWish] = useState(false);

  const addToWishlist = async (id) => {
    const userData = JSON.parse(localStorage.getItem("user"));
    const result = await fetch(`/books/${id}/wish`, {
      method: "POST",
      body: JSON.stringify({ user_id: userData.id }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await result.json();
    setIsWish(true);
  };

  const removeFromWishlist = async (id) => {
    const userData = JSON.parse(localStorage.getItem("user"));
    const result = await fetch(`/books/${id}/wish`, {
      method: "DELETE",
      body: JSON.stringify({ user_id: userData.id }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await result.json();
    setIsWish(false);
  };

  const addToRead = async (id) => {
    const userData = JSON.parse(localStorage.getItem("user"));
    const result = await fetch(`/books/${id}/read`, {
      method: "POST",
      body: JSON.stringify({ user_id: userData.id }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await result.json();
    setIsRead(true);
  };

  const removeFromRead = async (id) => {
    const userData = JSON.parse(localStorage.getItem("user"));
    const result = await fetch(`/books/${id}/read`, {
      method: "DELETE",
      body: JSON.stringify({ user_id: userData.id }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await result.json();
    setIsRead(false);
  };

  const checkReadAndWish = async (id) => {
    const userData = JSON.parse(localStorage.getItem("user"));
    const result = await fetch(`/books/${id}/check`, {
      method: "POST",
      body: JSON.stringify({ user_id: userData.id }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await result.json();
    setIsRead(data.read);
    setIsWish(data.wish);
    console.log(data);
  };

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
            checkReadAndWish(book.id).then(() => setShowDetails(!showDetails));
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
              {!isWish ? (
                <button
                  className="addto-button"
                  onClick={() => addToWishlist(book.id)}
                >
                  Añadir a Lista de lectura
                </button>
              ) : (
                //This book is already in your wishlist, show a button to remove it
                <button
                  className="removefrom-button"
                  onClick={() => removeFromWishlist(book.id)}
                >
                  Quitar de Lista de lectura
                </button>
              )}
              {!isRead ? (
                <button
                  className="addto-button"
                  onClick={() => addToRead(book.id)}
                >
                  Añadir a leídos
                </button>
              ) : (
                //This book is already in your read list, show a button to remove it
                <button
                  className="removefrom-button"
                  onClick={() => removeFromRead(book.id)}
                >
                  Quitar de leídos
                </button>
              )}
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
