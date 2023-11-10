import React, { useState } from "react";
import { Link } from "react-router-dom";
import { FaHome, FaUser, FaUsers } from "react-icons/fa";
import "./home.css";

function Home({ handleLogout }) {
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState([]);

  const handleSearch = async (event) => {
    const searchTerm = event.target.value;
    setSearchTerm(searchTerm);
    if (searchTerm === "") {
      setSearchResults([]);
      return;
    }
    if (searchTerm.length < 3) {
      return;
    }

    try {
      const response = await fetch(`/books/search?query=${searchTerm}`);
      const results = await response.json();
      const filteredResults = results.filter((book) => {
        const bookName = book.title.toLowerCase();
        //authors is an array with one or more authors, solve this by using .join()
        const bookAuthor = book.authors.join().toLowerCase();
        //categories is an array with one or more categories, solve this by using .join()
        const bookCategory = book.categories.join().toLowerCase();
        const bookPublicationDate = book.publication_date.toLowerCase();
        const bookPages = book.pages.toString();
        const bookShortDescription = book.short_description.toLowerCase();
        const bookLongDescription = book.long_description.toLowerCase();

        return (
          bookName.includes(searchTerm.toLowerCase()) ||
          bookAuthor.includes(searchTerm.toLowerCase()) ||
          bookCategory.includes(searchTerm.toLowerCase()) ||
          bookPublicationDate.includes(searchTerm.toLowerCase()) ||
          bookPages.includes(searchTerm) ||
          bookShortDescription.includes(searchTerm.toLowerCase()) ||
          bookLongDescription.includes(searchTerm.toLowerCase())
        );
      });
      setSearchResults(filteredResults);
      console.log(filteredResults);
    } catch (error) {
      console.error(error);
    }
  };

  const handleRating = (event) => {
    const rating = event.target.value;
    // Perform book rating here and update book rating state
    // Rating should be from 1 to 5
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
      <div className="main-content">
        <h1>Exploración y Búsqueda de Libros</h1>
        <input
          type="text"
          placeholder="Buscar por nombre, autor, país, categoría, número de página, y rango de fecha de publicación"
          value={searchTerm}
          onChange={handleSearch}
        />
        <div className="search-results">
          {searchResults.map((book) => (
            <div key={book.id}>
              <h2>{book.title}</h2>
              <img src={book.image} alt={book.name} />
              <p>{book.author}</p>
              <p>{book.publicationDate}</p>
              <p>{book.category}</p>
              <p>{book.shortDescription}</p>
              <div className="book-details">
                {/* Display book details here */}
                {/* Include book rating and reviews */}
                <select onChange={handleRating}>
                  <option value="">Calificar libro</option>
                  <option value="1">1</option>
                  <option value="2">2</option>
                  <option value="3">3</option>
                  <option value="4">4</option>
                  <option value="5">5</option>
                </select>
              </div>
            </div>
          ))}
        </div>
      </div>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}

export default Home;
