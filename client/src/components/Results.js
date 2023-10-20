import React, { useContext, useState } from "react";
import ResultCard from "./ResultCard";
import { useEffect } from "react";
import { DataContext } from "../context/DataContext";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import { axiosPost } from "../utils/axios";
import capitalize from "../utils/capitalize";

function Results({ products }) {
  const { productData, searchTerm } = useContext(DataContext);
  const {
    userData: { user_id }
  } = useContext(AuthContext);

  const navigate = useNavigate();

  useEffect(() => {
    if (productData.length === 0) {
      navigate("/");
    }
  }, [productData, navigate]);

  const newproducts = productData;
  const pages = Math.ceil(newproducts.length / 6);

  const [start, setStart] = useState(0);
  const [end, setEnd] = useState(6);
  const [page, setPage] = useState(1);

  const [dispProducts, setDispProducts] = useState(null);

  const addremovetrack = async (price, date, link, site) => {
    // Logic to untrack an item
    price = price.slice(1, -2);

    let prodData = { user_id, price, date, link, site };

    const url = "http://localhost:8000/watchlist/";
    const data = await axiosPost(url, prodData);

    if (data !== undefined) {
      console.log(data);
    } else {
      console.log("Something went wrong");
    }
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
        You have searched for <b>{capitalize(searchTerm)}</b>
      </p>
      <div className="results-grid">
        {dispProducts &&
          dispProducts.map((product, index) => (
            <ResultCard key={index} product={product} addremovetrack={addremovetrack} />
          ))}
      </div>
      <div className="form-footer">
        <div className="button-wrapper">
          <button className="link" onClick={goToPrevPage} disabled={page === 1}>
            Previous
          </button>
        </div>
        <p className="text">
          {" "}
          | {page} / {pages} |{" "}
        </p>
        <div className="button-wrapper">
          <button className="link" onClick={goToNextPage} disabled={page === pages}>
            Next
          </button>
        </div>
      </div>
    </div>
  );
}

export default Results;
