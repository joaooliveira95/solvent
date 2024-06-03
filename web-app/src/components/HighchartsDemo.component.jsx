import { useEffect } from "react";
import Highcharts from "highcharts/highstock";
import { Box } from "@chakra-ui/react";

const FinancialChart = () => {
  useEffect(() => {
    // Sample financial data
    const data = [
      [1557504000000, 185.17, 188.39, 184.73, 188.31],
      [1557590400000, 189.91, 192.47, 188.84, 190.78],
      [1557676800000, 191.24, 192.21, 186.43, 189.95],
      [1557936000000, 187.41, 189.7, 184.99, 185.72],
      [1558022400000, 184.66, 185.71, 181.37, 182.54],
      [1558108800000, 180.73, 182.14, 178.62, 180.23],
      [1558195200000, 180.29, 184.2, 180.05, 183.08],
      [1558281600000, 183.52, 184.35, 181.03, 183.51],
      [1558540800000, 183.08, 185.47, 182.15, 185.22],
      [1558627200000, 184.66, 184.8, 180.91, 182.78],
      // Add more data points here
    ];

    // Here you can customize your chart options
    const options = {
      rangeSelector: {
        selected: 1,
      },
      title: {
        text: "Financial Chart",
      },
      series: [
        {
          type: "candlestick",
          name: "AAPL Stock Price",
          data: data,
          tooltip: {
            valueDecimals: 2,
          },
        },
      ],
    };

    // Create the chart
    Highcharts.stockChart("financial-chart", options);
  }, []);

  return (
    <Box>
      {/* Container for the chart */}
      <Box id="financial-chart" w="100%" h="600px" minW={"7xl"}></Box>
    </Box>
  );
};

export default FinancialChart;
