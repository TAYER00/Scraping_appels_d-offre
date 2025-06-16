import React, { useState, useEffect } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import axios from 'axios';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
  CardActions,
  CircularProgress,
  Alert,
} from '@mui/material';
import AssignmentIcon from '@mui/icons-material/Assignment';
import BusinessIcon from '@mui/icons-material/Business';
import DateRangeIcon from '@mui/icons-material/DateRange';

const DashboardCard = ({ icon, title, value, color }) => (
  <Card sx={{ height: '100%' }}>
    <CardContent>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        {React.cloneElement(icon, { sx: { fontSize: 40, color } })}
      </Box>
      <Typography variant="h5" component="div">
        {value}
      </Typography>
      <Typography sx={{ mb: 1.5 }} color="text.secondary">
        {title}
      </Typography>
    </CardContent>
  </Card>
);

const TenderPreview = ({ tender }) => (
  <Paper sx={{ p: 2, height: '100%' }}>
    <Typography variant="subtitle2" color="text.secondary" gutterBottom>
      {tender.site.toUpperCase()}
    </Typography>
    <Typography variant="body1" sx={{ mb: 1 }}>
      {tender.objet}
    </Typography>
    <Typography variant="body2" color="text.secondary">
      Deadline: {tender.date_limite}
    </Typography>
  </Paper>
);

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [tendersRes, statsRes] = await Promise.all([
          axios.get('/api/tenders/'),
          axios.get('/api/tenders/statistics/')
        ]);

        setData({
          tenders: tendersRes.data.tenders,
          stats: statsRes.data,
          lastUpdated: tendersRes.data.last_updated
        });
      } catch (err) {
        setError('Failed to fetch dashboard data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  const recentTenders = data.tenders.slice(0, 4);

  return (
    <Box>
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h5" component="h1">
          Dashboard
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Last updated: {new Date(data.lastUpdated).toLocaleString()}
        </Typography>
      </Box>

      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={4}>
          <DashboardCard
            icon={<AssignmentIcon />}
            title="Total Tenders"
            value={data.stats.total_tenders}
            color="#1976d2"
          />
        </Grid>
        <Grid item xs={12} sm={4}>
          <DashboardCard
            icon={<BusinessIcon />}
            title="Active Sites"
            value={Object.keys(data.stats.tenders_by_site).length}
            color="#2e7d32"
          />
        </Grid>
        <Grid item xs={12} sm={4}>
          <DashboardCard
            icon={<DateRangeIcon />}
            title="Months Coverage"
            value={Object.keys(data.stats.tenders_by_date).length}
            color="#ed6c02"
          />
        </Grid>
      </Grid>

      <Box sx={{ mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Recent Tenders
        </Typography>
        <Grid container spacing={2}>
          {recentTenders.map((tender) => (
            <Grid item xs={12} sm={6} key={tender.id}>
              <TenderPreview tender={tender} />
            </Grid>
          ))}
        </Grid>
        <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
          <Button
            component={RouterLink}
            to="/tenders"
            variant="contained"
            color="primary"
          >
            View All Tenders
          </Button>
        </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;