import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Paper, Table, TableBody, TableCell, TableContainer, TableHead, 
  TableRow, TablePagination, TextField, Box, Chip, IconButton,
  Typography, CircularProgress, Alert
} from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import SearchIcon from '@mui/icons-material/Search';

const TenderList = () => {
  const [tenders, setTenders] = useState([]);
  const [filteredTenders, setFilteredTenders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSite, setSelectedSite] = useState('all');

  const fetchTenders = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get('/api/tenders/');
      setTenders(response.data.tenders);
      setFilteredTenders(response.data.tenders);
    } catch (err) {
      setError('Failed to fetch tenders. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTenders();
  }, []);

  useEffect(() => {
    const filtered = tenders.filter(tender => {
      const matchesSearch = tender.objet.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesSite = selectedSite === 'all' || tender.site === selectedSite;
      return matchesSearch && matchesSite;
    });
    setFilteredTenders(filtered);
    setPage(0);
  }, [searchTerm, selectedSite, tenders]);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const uniqueSites = [...new Set(tenders.map(tender => tender.site))];

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

  return (
    <Box>
      <Box sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 2 }}>
        <Typography variant="h5" component="h1">
          Tenders
        </Typography>
        <IconButton onClick={fetchTenders} size="small">
          <RefreshIcon />
        </IconButton>
      </Box>

      <Box sx={{ mb: 3, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
        <TextField
          placeholder="Search tenders..."
          variant="outlined"
          size="small"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          InputProps={{
            startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
          }}
          sx={{ minWidth: 300 }}
        />
        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          <Chip
            label="All Sites"
            onClick={() => setSelectedSite('all')}
            color={selectedSite === 'all' ? 'primary' : 'default'}
          />
          {uniqueSites.map(site => (
            <Chip
              key={site}
              label={site}
              onClick={() => setSelectedSite(site)}
              color={selectedSite === site ? 'primary' : 'default'}
            />
          ))}
        </Box>
      </Box>

      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }}>
          <TableHead>
            <TableRow>
              <TableCell>Site</TableCell>
              <TableCell>Object</TableCell>
              <TableCell>Deadline</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredTenders
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((tender) => (
                <TableRow key={tender.id}>
                  <TableCell>
                    <Chip label={tender.site} size="small" />
                  </TableCell>
                  <TableCell>{tender.objet}</TableCell>
                  <TableCell>{tender.date_limite}</TableCell>
                </TableRow>
              ))}
          </TableBody>
        </Table>
      </TableContainer>

      <TablePagination
        rowsPerPageOptions={[10, 25, 50]}
        component="div"
        count={filteredTenders.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </Box>
  );
};

export default TenderList;