import React from "react";

function Book({ book, onAdd, onRemove, onSelect }) {
    return (
        <div>
            <h2>{book.title}</h2>
            <p>{book.author}</p>
            <button onClick={onAdd}>Add</button>
            <button onClick={onRemove}>Remove</button>
            <button onClick={onSelect}>Select</button>
        </div>
    );
}

function BookList({ books, onBookAdd, onBookRemove, onBookSelect }) {
    return (
        <div>
            <ul>
                {books.map((book) => (
                    <li key={book.id}>
                        <Book book={book} onAdd={() => onBookAdd(book)} onRemove={() => onBookRemove(book)} onSelect={() => onBookSelect(book)} />
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default BookList;
