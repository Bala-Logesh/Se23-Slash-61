import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    ArcElement,
    Tooltip,
    Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";
import { useNavigate, useParams } from "react-router-dom";
import { useContext, useEffect } from "react";
import { AuthContext } from "../context/AuthContext";

import { dates, prices } from "../data/chartdata";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    ArcElement,
    Tooltip,
    Legend
);

function IndTracking() {
    const navigate = useNavigate();

    const {
        userData: { isLoggedIn },
    } = useContext(AuthContext);

    useEffect(() => {
        if (!isLoggedIn) {
            navigate("/");
        }
    }, [isLoggedIn, navigate]);

    const { id } = useParams();

    return (
        <div className="chart-page-grid">
            <p className="pagetitle">
                Price of <b>product {id}</b> over the period
            </p>
            <div className="chart-container">
                <Line
                    data={{
                        labels: dates,
                        datasets: [
                            {
                                label: "Min Values",
                                data: prices,
                                backgroundColor: "rgb(239, 236, 242)",
                                borderColor: "rgb(184, 176, 203)",
                                borderWidth: 2,
                                fill: false,
                            },
                        ],
                    }}
                    options={{
                        title: {
                            display: true,
                            text: "Price tracking over few days",
                            fontSize: 20,
                        },
                        legend: {
                            display: false,
                        },
                        maintainAspectRatio: false,
                        responsive: true,
                    }}
                />
            </div>
        </div>
    );
}

export default IndTracking;