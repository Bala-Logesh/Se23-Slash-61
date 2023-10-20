import React, { useState } from "react";
import Card from "./Card";

function Search() {
    let [msg, setMsg] = useState("");

    const [formData, setFormData] = useState({
        item: "",
        website: "",
    });

    const handleSubmit = async (e) => {
        e.preventDefault();

        let { item, website } = formData;
        if (item === "" || website === "") {
            setMsg("Please fill in all the fields");
            return;
        }

        console.log(formData);
        return;
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
                    <option className="links" key="Amazon">
                        Amazon
                    </option>
                    <option key="Walmart">Walmart</option>
                    <option key="Ebay">Ebay</option>
                    <option key="Costco">Costco</option>
                    <option key="Target">Target</option>
                    <option key="BestBuy">BestBuy</option>
                    <option key="All">All</option>
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