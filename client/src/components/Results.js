import React, { useState } from "react";
import ResultCard from "./ResultCard";
import { useEffect } from "react";

function Results({ products }) {
    const newproducts = products;
    const pages = Math.ceil(newproducts.length / 6);

    const [start, setStart] = useState(0);
    const [end, setEnd] = useState(6);
    const [page, setPage] = useState(1);

    const [dispProducts, setDispProducts] = useState(null);

    const addremovetrack = (prodid) => {
        // Logic to untrack an item
    };

    useEffect(() => {
        setDispProducts(newproducts.slice(start, end));
    }, [start, end, page, newproducts]);

    const goToNextPage = () => {
        if (page === pages) {
            return;
        }

        setPage((curr) => curr + 1);

        let offset = page * 6;

        setStart(offset);
        setEnd(() => {
            if (offset + 6 > newproducts.length - 1) return products.length;
            else return offset + 6;
        });

        setDispProducts(newproducts.slice(start, end));
    };

    const goToPrevPage = () => {
        if (page === 1) {
            return;
        }

        setPage((curr) => curr - 1);

        let offset = (page - 2) * 6;

        setStart(offset);
        setEnd(() => {
            if (offset + 6 > newproducts.length - 1) return products.length;
            else return offset + 6;
        });

        setDispProducts(newproducts.slice(start, end));
    };

    return (
        <div className="result-page-grid">
            <p className="pagetitle">
                You have searched for <b>latptops</b>
            </p>
            <div className="results-grid">
                {dispProducts &&
                    dispProducts.map((product) => (
                        <ResultCard
                            key={product.id}
                            product={product}
                            addremovetrack={addremovetrack}
                        />
                    ))}
            </div>
            <div className="form-footer">
                <div class="button-wrapper">
                    <button className="link" onClick={goToPrevPage} disabled={page === 1}>
                        Previous
                    </button>
                </div>
                <p className="text">
                    {" "}
                    | {page} / {pages} |{" "}
                </p>
                <div class="button-wrapper">
                    <button
                        className="link"
                        onClick={goToNextPage}
                        disabled={page === pages}
                    >
                        Next
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Results;