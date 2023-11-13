import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { FaHome, FaUser } from "react-icons/fa";
import "./home.css";
import { BookCard } from "../components/bookCard";

function Home({ handleLogout }) {
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [searchType, setSearchType] = useState("");
  const [pagination, setPagination] = useState({});

  async function getAllBooks(page, perPage) {
    try {
      const response = await fetch(`/books?page=${page}&per_page=${perPage}`);
      const data = await response.json();
      setPagination(data.pagination);
      return data.books;
    } catch (error) {
      console.error(error);
    }
  }

  useEffect(() => {
    async function fetchBooks() {
      const books = await getAllBooks(1, 10);
      setSearchResults(books);
    }
    fetchBooks();
  }, []);

  const handleSearch = async (event) => {
    const searchTerm = event.target.value;
    const searchType = event.target.name;
    const page = event.page;
    const perPage = 10;

    setSearchType(searchType);
    setSearchTerm(searchTerm);

    if (searchTerm === "") {
      const books = await getAllBooks(1, 10);
      setSearchResults(books);
      return;
    }
    if (searchTerm.length < 3) {
      return;
    }

    try {
      const response = await fetch(`/books/search?${searchType}=${searchTerm}&page=${page}&per_page=${perPage}`);
      const results = await response.json();
      setPagination(results.pagination);
      setSearchResults(results.books);
    } catch (error) {
      console.error(error);
    }
  };

  const handleRating = (event) => {
    const rating = event.target.value;
    // Perform book rating here and update book rating state
    // Rating should be from 1 to 5
  };

  const handlePageChange = async (event) => {
    //make this function work for both getAllBooks and handleSearch
    const page = event.target.value;
    if (searchTerm === "") {
      const books = await getAllBooks(page, pagination.per_page);
      setSearchResults(books);
      return;
    }
    if (searchTerm.length < 3) {
      return;
    }
    const response = await fetch(`/books/search?${searchType}=${searchTerm}&page=${page}&per_page=${pagination.per_page}`);
    const results = await response.json();
    setPagination(results.pagination);
    setSearchResults(results.books);

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
      <div className="main-content">
        <h1>Exploración y Búsqueda de Libros</h1>
        <input
          className="search-bar"
          type="text"
          placeholder="Buscar por nombre, autor, país, categoría, número de página, y rango de fecha de publicación"
          value={searchTerm}
          name="query"
          onChange={(event) => {
            event.page = 1;
            handleSearch(event);
          }}
        />
        <div className="search-results">
        {searchResults.map((book) => (
          <BookCard
            key={book.id}
            book={book}
            handleSearch={handleSearch}
          />
        ))}
        </div>
        {pagination.total_pages > 1 && (
          <div className="pagination">
            <button
              className="page-button"
              value={pagination.page - 1}
              onClick={handlePageChange}
              disabled={pagination.page === 1}
            >
              Previous
            </button>
            <span className="page-info">
              Page {pagination.page} of {pagination.total_pages}
            </span>
            <button
              className="page-button"
              value={pagination.page + 1}
              onClick={handlePageChange}
              disabled={pagination.page === pagination.total_pages}
            >
              Next
            </button>
          </div>
        )}
      </div>
      <button className="logout" onClick={handleLogout}>
        Logout
      </button>
    </div>
  );
}

export default Home;
