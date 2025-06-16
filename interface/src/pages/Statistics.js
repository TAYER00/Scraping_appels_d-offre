import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Box, Paper, Grid, Typography, CircularProgress, Alert } from '@mui/material';
import { Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const Statistics = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await axios.get('/api/tenders/statistics/');
        setStats(response.data);
      } catch (err) {
        setError('Failed to fetch statistics. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>
    );
  }

  const siteData = {
    labels: Object.keys(stats.tenders_by_site),
    datasets: [
      {
        data: Object.values(stats.tenders_by_site),
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF'
        ]
      }
    ]
  };

  const dateData = {
    labels: Object.keys(stats.tenders_by_date),
    datasets: [
      {
        label: 'Tenders by Month',
        data: Object.values(stats.tenders_by_date),
        backgroundColor: '#36A2EB'
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom'
      }
    }
  };

  return (
    <Box>
      <Typography variant="h5" component="h1" gutterBottom>
        Tender Statistics
      </Typography>

      <Typography variant="h6" color="primary" gutterBottom sx={{ mt: 3 }}>
        Total Tenders: {stats.total_tenders}
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Typography variant="h6" gutterBottom>
              Tenders by Site
            </Typography>
            <Box sx={{ height: 300 }}>
              <Pie data={siteData} options={chartOptions} />
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Typography variant="h6" gutterBottom>
              Tenders by Month
            </Typography>
            <Box sx={{ height: 300 }}>
              <Bar data={dateData} options={chartOptions} />
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Statistics;