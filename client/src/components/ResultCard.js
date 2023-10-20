import { useContext, useState } from "react";
import { Link } from "react-router-dom";
import Card from "./Card";
import { AuthContext } from "../context/AuthContext";
import datetime from "../utils/datetime";
import capitalize from "../utils/capitalize";

function ResultCard({ product, addremovetrack }) {
    const {
        userData: { isLoggedIn },
    } = useContext(AuthContext);

    let {
        id,
        title,
        price,
        website,
        tracked,
        timestamp,
        link: prodlink,
    } = product;
    const [trackedItem, setTrackedItem] = useState(tracked);

    const toggleTracking = () => {
        addremovetrack(id);
        setTrackedItem((prev) => !prev);
    };

    const { month, dtdd, dtyy, timehh, timemm } = datetime(timestamp);

    return (
        <Card result>
            <div className="result-card-title">
                <p className="cardtext">{title}</p>
                {isLoggedIn && (
                    <>
                        {trackedItem ? (
                            <p className="cp" onClick={() => toggleTracking(id)}>
                                &#9733;
                            </p>
                        ) : (
                            <p className="cp" onClick={() => toggleTracking(id)}>
                                &#9734;
                            </p>
                        )}
                    </>
                )}
            </div>
            <div className="result-card-body">
                <div className="imgcontainer">
                    <img
                        className="img"
                        alt="Product"
                        src="https://placehold.co/150x150"
                    />
                </div>
                <div>
                    <p className="cardtext">{capitalize(website)}</p>
                    <p className="cardtext">{price}</p>
                    <p className="cardtext">
                        {dtdd} {month}, {dtyy}
                    </p>
                    <p className="cardtext">
                        {timehh}:{timemm}
                    </p>
                </div>
            </div>
            {trackedItem ? (
                <button>
                    <Link to={`../tracking/${id}`}>See tracking data</Link>
                </button>
            ) : (
                <button>
                    <a
                        href={"https://" + prodlink}
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        Go to grab the deal
                    </a>
                </button>
            )}
        </Card>
    );
}

export default ResultCard;