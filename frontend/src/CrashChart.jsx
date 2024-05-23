import React, { useEffect, useState } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import "chart.js/auto";
import "./CrashChart.css";

const CrashChart = () => {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: "Crashes",
        data: [],
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.6)",
      },
    ],
  });
  const [filter, setFilter] = useState({
    month: new Date().getMonth() + 1, 
    year: new Date().getFullYear(), 
  });

  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  useEffect(() => {
    const fetchData = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL;
        if (!apiUrl) throw new Error("API URL is not defined");

        const response = await axios.get(apiUrl);
        const filteredData = response.data.crash_dates.filter((date) => {
          const dateObj = new Date(date);
          return (
            dateObj.getMonth() + 1 === filter.month &&
            dateObj.getFullYear() === filter.year
          );
        });
        const crashData = filteredData.reduce((acc, date) => {
          const day = new Date(date).getDate();
          if (!acc[day]) acc[day] = 0;
          acc[day]++;
          return acc;
        }, {});
        setChartData({
          labels: Object.keys(crashData).sort((a, b) => a - b),
          datasets: [
            {
              label: "Crashes",
              data: Object.values(crashData),
              borderColor: "rgba(75, 192, 192, 1)",
              backgroundColor: "rgba(75, 192, 192, 0.6)",
            },
          ],
        });
      } catch (error) {
        console.error("Error fetching crash data:", error);
      }
    };

    fetchData();
  }, [filter]);

  const handleMonthChange = (e) => {
    setFilter({ ...filter, month: parseInt(e.target.value) });
  };

  const handleYearChange = (e) => {
    setFilter({ ...filter, year: parseInt(e.target.value) });
  };

  return (
    <div className="chart-container">
      <h2 className="title">Haven and Hearth Server Tracker</h2>
      <div className="filter-bar">
        <select value={filter.month} onChange={handleMonthChange}>
          {months.map((month, index) => (
            <option key={index} value={index + 1}>
              {month}
            </option>
          ))}
        </select>
        <input
          type="number"
          value={filter.year}
          onChange={handleYearChange}
          min="2000"
          max={new Date().getFullYear()}
        />
      </div>
      <Bar
        data={chartData}
        options={{
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              title: {
                display: true,
                text: "Day of Month",
              },
            },
            y: {
              title: {
                display: true,
                text: "Number of Crashmas",
              },
              beginAtZero: true,
            },
          },
        }}
      />
    </div>
  );
};

export default CrashChart;
