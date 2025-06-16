import React from 'react';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import DashboardIcon from '@mui/icons-material/Dashboard';
import ListAltIcon from '@mui/icons-material/ListAlt';
import BarChartIcon from '@mui/icons-material/BarChart';

const Navbar = () => {
  const location = useLocation();

  const navItems = [
    { text: 'Dashboard', path: '/', icon: <DashboardIcon /> },
    { text: 'Tenders', path: '/tenders', icon: <ListAltIcon /> },
    { text: 'Statistics', path: '/statistics', icon: <BarChartIcon /> },
  ];

  return (
    <AppBar position="static" color="primary" elevation={0}>
      <Toolbar>
        <Typography
          variant="h6"
          component="div"
          sx={{ flexGrow: 0, display: { xs: 'none', sm: 'block' }, mr: 4 }}
        >
          Tender Monitor
        </Typography>
        <Box sx={{ flexGrow: 1, display: 'flex', gap: 2 }}>
          {navItems.map((item) => (
            <Button
              key={item.path}
              component={RouterLink}
              to={item.path}
              color="inherit"
              startIcon={item.icon}
              sx={{
                textTransform: 'none',
                borderRadius: 2,
                px: 2,
                backgroundColor: location.pathname === item.path ? 'rgba(255, 255, 255, 0.12)' : 'transparent',
                '&:hover': {
                  backgroundColor: 'rgba(255, 255, 255, 0.2)'
                }
              }}
            >
              {item.text}
            </Button>
          ))}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;