
import React from "react";

function BookDetails({ book, onDeselect }) {
  return (
    <div>
      <h2>{book.title}</h2>
      <p>{book.author}</p>
      <p>{book.description}</p>
      <button onClick={onDeselect}>Deselect</button>
    </div>
  );
}

export default BookDetails;
