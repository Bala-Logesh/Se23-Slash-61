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
    return (
      <div className="chart-page-grid">
        <p className="pagetitle">
          Prices of <b>latptops</b> in all the websites
        </p>
        <div className="chart-container">
          <Line
            data={{
              labels: [...trends.map((trend) => trend.website)],
              datasets: [
                {
                  label: "Min Values",
                  data: [...trends.map((trend) => trend.min)],
                  backgroundColor: "rgb(239, 236, 242)",
                  borderColor: "rgb(184, 176, 203)",
                  borderWidth: 2,
                  fill: false,
                },
                {
                  label: "Max Values",
                  data: [...trends.map((trend) => trend.max)],
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