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

import { trends } from "../data/chartdata";
import { useNavigate } from "react-router-dom";
import { useContext, useEffect, useState } from "react";
import { DataContext } from "../context/DataContext";
import capitalize from "../utils/capitalize";
import { axiosGet } from "../utils/axios";

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

function Trends() {
  const navigate = useNavigate();

  const { searchTerm } = useContext(DataContext);
  const [isLoading, setIsLoading] = useState(false);
  const [lowestPrices, setLowestPrices] = useState([]);
  const [highestPrices, setHighestPrices] = useState([]);

  useEffect(() => {
    if (searchTerm === "") {
      navigate("/");
    }
  }, [searchTerm, navigate]);

  const fetchMinMaxPrice = async () => {
    setIsLoading(true);
    let item_name = searchTerm;
    const url = `http://localhost:8000/analysis/topCost/all/${item_name}`;
    const data = await axiosGet(url);

    if (data !== undefined) {
      setLowestPrices(data.map((d) => d.lowest_price));
      setHighestPrices(data.map((d) => d.highest_price));
    }
    setIsLoading(false);
  };

  useEffect(() => {
    fetchMinMaxPrice();
  }, []);

  return (
    <div className="chart-page-grid">
      {isLoading && <p className="pagetitle">Loading data...</p>}
      {!isLoading && (
        <p className="pagetitle">
          Prices of <b>{capitalize(searchTerm)}</b> in all the websites
        </p>
      )}
      <div className="chart-container">
        <Line
          data={{
            labels: [...trends.map((trend) => trend.website)],
            datasets: [
              {
                label: "Lowest Prices",
                data: lowestPrices,
                backgroundColor: "rgb(239, 236, 242)",
                borderColor: "rgb(184, 176, 203)",
                borderWidth: 2,
                fill: false,
              },
              {
                label: "Highest Prices",
                data: highestPrices,
                backgroundColor: "rgb(239, 236, 242)",
                borderColor: "rgb(184, 176, 203)",
                borderWidth: 2,
                fill: false,
              },
            ],
          }}
          options={{
            responsive: true,
            maintainAspectRatio: false,
            title: {
              display: true,
              text: "Highest and lowest prices on each website",
              fontSize: 20,
            },
            legend: {
              display: false,
            },
          }}
        />
      </div>
    </div>
  );
}

export default Trends;
