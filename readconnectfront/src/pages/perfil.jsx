import React, { useState } from "react";
import BookList from "../components/BookList";
import BookDetails from "../components/BookDetails";
import { Link } from "react-router-dom";
import { FaHome, FaUser, FaUsers } from "react-icons/fa";
import "./perfil.css";

async function uploadProfilePicture(file) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("upload_preset", "readconnect");

  try {
    const response = await fetch(
      "https://api.cloudinary.com/v1_1/readconnect/image/upload",
      {
        method: "POST",
        body: formData,
      }
    );
    const data = await response.json();
    return data.secure_url;
  } catch (err) {
    return console.log(err);
  }
}

function Perfil({ handleLogout }) {
  //The user is logged in, so we can get the user from the local storage
  const user = JSON.parse(localStorage.getItem("user"));
  const [name, setName] = useState(user.username);
  const [profilePicture, setProfilePicture] = useState(null);
  const [booksToRead, setBooksToRead] = useState([]);
  const [booksRead, setBooksRead] = useState([]);
  const [selectedBook, setSelectedBook] = useState(null);

  const handleNameChange = (event) => {
    setName(event.target.value);
  };

  const handleProfilePictureChange = (event) => {
    const file = event.target.files[0];
    uploadProfilePicture(file).then((url) => {
      setProfilePicture(url);
    });
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
          <li>
            <Link to="/usuarios">
              <FaUsers />
              <span>Usuarios</span>
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
            onChange={handleNameChange}
          />
        </div>
        <div className="perfil-picture">
          <label htmlFor="profile-picture">Imagen de Perfil:</label>
          <input
            type="file"
            id="profile-picture"
            onChange={handleProfilePictureChange}
          />
          {profilePicture && <img src={profilePicture} alt="Profile" />}
        </div>
        <h2>Libros por Leer</h2>
        <BookList
          books={booksToRead}
          onBookAdd={(book) => handleBookAdd(book, "toRead")}
          onBookRemove={(book) => handleBookRemove(book, "toRead")}
          onBookSelect={handleBookSelect}
        />
        <h2>Libros Leídos</h2>
        <BookList
          books={booksRead}
          onBookAdd={(book) => handleBookAdd(book, "read")}
          onBookRemove={(book) => handleBookRemove(book, "read")}
          onBookSelect={handleBookSelect}
        />
        {selectedBook && (
          <BookDetails book={selectedBook} onDeselect={handleBookDeselect} />
        )}
        <h2>Categorías Favoritas</h2>
        {/* Display favorite categories */}
        <h2>Autores Favoritos</h2>
        {/* Display favorite authors */}
      </div>
      <button className="logout" onClick={handleLogout}>
        Logout
      </button>
    </div>
  );
}

export default Perfil;
