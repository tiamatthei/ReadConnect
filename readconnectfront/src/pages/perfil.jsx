import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { FaHome, FaUser, FaUsers } from "react-icons/fa";
import "./perfil.css";

function Perfil({ handleLogout }) {
  //The user is logged in, so we can get the user from the local storage
  const user = JSON.parse(localStorage.getItem("user"));
  const [name, setName] = useState(user.username);
  const [profilePicture, setProfilePicture] = useState(null);
  const [booksToRead, setBooksToRead] = useState([]);
  const [booksRead, setBooksRead] = useState([]);
  const [selectedBook, setSelectedBook] = useState(null);

  //Here goes a function that fetches the user's books to read and books read
  useEffect(() => {
    const getBooks = async () => {
      const result = await fetch(`/read_books/${user.id}`);
      const data = await result.json();
      setBooksRead(data.books);
    };
    getBooks();
  }, []);

  useEffect(() => {
    const getBooks = async () => {
      const result = await fetch(`/wish_books/${user.id}`);
      const data = await result.json();
      setBooksToRead(data.books);
      console.log(data.books);
    };
    getBooks();
  }, []);

  const handleNameChange = async (event) => {
    console.log(user.id);
    const result = await fetch(`/change_name`, {
      method: "PUT",
      body: JSON.stringify({ username: name, id: user.id }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await result.json();
    localStorage.setItem("user", JSON.stringify(data.data));
    setName(data.data.username);
  };

  const handleBookAdd = (book, list) => {
    if (list === "toRead") {
      setBooksToRead([...booksToRead, book]);
    } else if (list === "read") {
      setBooksRead([...booksRead, book]);
    }
  };

  const handleBookRemove = (book, list) => {
    if (list === "toRead") {
      setBooksToRead(booksToRead.filter((b) => b.id !== book.id));
    } else if (list === "read") {
      setBooksRead(booksRead.filter((b) => b.id !== book.id));
    }
  };

  const handleBookSelect = (book) => {
    setSelectedBook(book);
  };

  const handleBookDeselect = () => {
    setSelectedBook(null);
  };

  return (
    <div className="container">
      <nav className="sidebar">
        <ul>
          <li>
            <Link to="/home">
              <FaHome />
              <span>Inicio</span>
            </Link>
          </li>
          <li>
            <Link to="/perfil">
              <FaUser />
              <span>Perfil</span>
            </Link>
          </li>
        </ul>
      </nav>
      <div className="perfil">
        <h1>Perfil de Usuario</h1>
        <div className="perfil-name">
          <label htmlFor="name">Nombre:</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(event) => setName(event.target.value)}
          />
          <button
            className="change-name"
            type="button"
            onClick={handleNameChange}
          >
            Cambiar nombre
          </button>
        </div>
        <h2>Libros por Leer</h2>
        <div className="books-to-read">
          {booksToRead.map((book) => (
            <div key={book.id} className="book-card">
              <h3>{book.title}</h3>
              <img
                className="icon-image"
                src={book.thumbnail_url}
                alt={book.title}
                onClick={() => handleBookSelect(book)}
              />
              <button
                className="removefrom-button"
                onClick={() => handleBookRemove(book, "toRead")}
              >
                Quitar de Lista de lectura
              </button>
            </div>
          ))}
        </div>
        <h2>Libros Leídos</h2>
        <div className="books-read">
          {booksRead.map((book) => (
            <div key={book.id} className="book-card">
              <h3>{book.title}</h3>
              <img
                className="icon-image"
                src={book.thumbnail_url}
                alt={book.title}
                onClick={() => handleBookSelect(book)}
              />
              <button
                className="removefrom-button"
                onClick={() => handleBookRemove(book, "read")}
              >
                Quitar de Lista de lectura
              </button>
            </div>
          ))}
        </div>
      </div>
      <button className="logout" onClick={handleLogout}>
        Logout
      </button>
    </div>
  );
}

export default Perfil;
