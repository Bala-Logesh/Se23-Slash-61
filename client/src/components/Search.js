import React, { useContext, useState } from "react";
import Card from "./Card";
import { DataContext } from "../context/DataContext";
import { axiosGet } from "../utils/axios";
import { useNavigate } from "react-router-dom";

function Search() {
  const navigate = useNavigate();

  let [msg, setMsg] = useState("");

  const { setProductData, setSearchTerm } = useContext(DataContext);

  const [formData, setFormData] = useState({
    item: "",
    website: "",
  });

  const handleSubmit = async (e) => {
    e.preventDefault();

    let { item: item_name, website: site } = formData;
    if (item_name === "" || site === "") {
      setMsg("Please fill in all the fields");
      return;
    }
    setSearchTerm(item_name);

    const url = `http://localhost:8000/${site}/${item_name}`;
    setMsg("Loading data...");
    const data = await axiosGet(url);

    if (data !== undefined) {
      // data fetch successful, you can redirect to the results page
      setProductData(data);

      setMsg("");
      setFormData({
        item: "",
        website: "",
      });

      navigate("/results");
    } else {
      setMsg("Something went wrong");
    }
  };

  return (
    <Card>
      <p className="form-header">Search to your heart's content</p>
      <br />
      {msg === "" && <p className="placeholder">Placeholder for messages</p>}
      {msg !== "" && <p className="error">{msg}</p>}
      <br />
      <form onSubmit={handleSubmit} className="form">
        <input
          type="text"
          placeholder="Product"
          value={formData.item}
          onChange={(e) => setFormData({ ...formData, item: e.target.value })}
        />
        <br />
        <select
          value={formData.website}
          onChange={(e) =>
            setFormData({ ...formData, website: e.target.value })
          }
        >
          <option defaultChecked>Select a website</option>
          <option key="az" value="az">
            Amazon
          </option>
          <option key="wm" value="wm">
            Walmart
          </option>
          <option key="eb" value="eb">
            Ebay
          </option>
          <option key="cc" value="cc">
            Costco
          </option>
          <option key="tg" value="tg">
            Target
          </option>
          <option key="bb" value="bb">
            BestBuy
          </option>
          <option key="all" value="all">
            All
          </option>
        </select>
        <br />
        <button className="buttonmb20" type="submit">
          Search for awesome deals
        </button>
      </form>
    </Card>
  );
}

export default Search;
